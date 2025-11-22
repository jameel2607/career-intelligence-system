from sqlalchemy.orm import Session
# Models imported inside functions to avoid circular dependency
from app.services.kb_service import load_kb
from app.services.document_service import list_documents
from app.core.exceptions import ScoringError, ProfileNotFoundError, KnowledgeBaseError
import pandas as pd
import re
import logging
from typing import List, Dict, Tuple, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('scoring_error.log')
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def _norm(x: float) -> float:
    """Normalize value between 0 and 1"""
    return max(0.0, min(1.0, x))

def _extract_skills_from_text(text: str) -> List[str]:
    """Extract skills from text using common patterns"""
    if not text:
        return []
    
    # Common technical skills patterns
    skills_patterns = [
        r'\b(python|java|javascript|react|angular|vue|node\.?js|sql|mysql|postgresql|mongodb|docker|kubernetes|aws|azure|gcp|git|github|html|css|bootstrap|tailwind)\b',
        r'\b(machine learning|ml|artificial intelligence|ai|data science|data analysis|deep learning|tensorflow|pytorch|pandas|numpy|scikit-learn)\b',
        r'\b(project management|agile|scrum|kanban|jira|confluence|slack|teams|communication|leadership|problem solving)\b'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for pattern in skills_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        found_skills.extend(matches)
    
    return list(set(found_skills))

def calculate_degree_score(education_level: str) -> float:
    """Calculate degree score based on education level"""
    if not education_level:
        return 0.2
    
    level = education_level.lower().strip()
    degree_mapping = {
        'phd': 1.0, 'doctorate': 1.0, 'ph.d': 1.0, 'md': 1.0, 'ms': 1.0,
        'master': 0.8, 'masters': 0.8, 'msc': 0.8, 'mba': 0.8, 'ma': 0.8, 'mca': 0.8, 'mtech': 0.8, 'me': 0.8, 'mcom': 0.8,
        'bachelor': 0.6, 'bachelors': 0.6, 'bsc': 0.6, 'ba': 0.6, 'btech': 0.6, 'be': 0.6, 'bcom': 0.6, 'bba': 0.6, 'bca': 0.6, 'bcs': 0.6, 'bds': 0.6, 'mbbs': 0.6,
        'diploma': 0.4, 'associate': 0.4,
        'certificate': 0.3, 'high school': 0.2, 'secondary': 0.2
    }
    
    for key, score in degree_mapping.items():
        if key in level:
            return score
    
    return 0.3  # Default for unrecognized degrees

def calculate_experience_score(experience_years: float) -> float:
    """Calculate experience score based on years of experience"""
    if experience_years is None:
        return 0.1
    
    if experience_years >= 10:
        return 1.0
    elif experience_years >= 5:
        return 0.8
    elif experience_years >= 2:
        return 0.6
    elif experience_years >= 1:
        return 0.4
    elif experience_years > 0:
        return 0.2
    else:
        return 0.1

def calculate_domain_score(profile: Any, target_role_skills: List[str]) -> float:
    """Calculate Domain/Technical Score (DS)"""
    if not target_role_skills:
        return 0.3
    
    # Extract skills from profile
    profile_skills = []
    if profile.skills:
        profile_skills.extend(_extract_skills_from_text(profile.skills))
    if profile.interests:
        profile_skills.extend(_extract_skills_from_text(profile.interests))
    if profile.bio:
        profile_skills.extend(_extract_skills_from_text(profile.bio))
    
    profile_skills = [skill.lower().strip() for skill in profile_skills]
    target_skills = [skill.lower().strip() for skill in target_role_skills]
    
    if not target_skills:
        return 0.3
    
    # Calculate overlap
    matched_skills = sum(1 for skill in target_skills if any(ps in skill or skill in ps for ps in profile_skills))
    coverage = matched_skills / len(target_skills)
    
    return _norm(coverage)

def calculate_practical_score(profile: Any) -> float:
    """Calculate Practical Evidence Score (P)"""
    evidence_score = 0.0
    
    # Check bio for practical experience indicators
    if profile.bio:
        bio_lower = profile.bio.lower()
        practical_keywords = [
            'project', 'internship', 'work experience', 'freelance', 'portfolio',
            'github', 'deployed', 'built', 'developed', 'created', 'implemented'
        ]
        
        for keyword in practical_keywords:
            if keyword in bio_lower:
                evidence_score += 0.1
    
    # Check skills for practical tools
    if profile.skills:
        skills_lower = profile.skills.lower()
        practical_tools = ['git', 'github', 'docker', 'aws', 'deployment', 'production']
        
        for tool in practical_tools:
            if tool in skills_lower:
                evidence_score += 0.1
                
    # Check for URLs
    if profile.github_url:
        evidence_score += 0.2
    if profile.linkedin_url:
        evidence_score += 0.1
        
    # Check experience years
    if profile.experience_years and profile.experience_years > 0:
        evidence_score += 0.2
    
    return _norm(evidence_score)

def calculate_soft_skills_score(db: Session, profile: Any) -> float:
    """Calculate Soft Skill Score (SS) = Base + Course Boost"""
    from app.models.course import Course
    from app.models.user_course import UserCourse
    
    # 1. Base Soft Skill Score (SS_base) - Max 0.7
    ss_base = 0.0
    
    # Check for soft skills mentions in profile
    text_to_check = f"{profile.bio or ''} {profile.skills or ''} {profile.interests or ''}".lower()
    
    soft_skills_keywords = [
        'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking',
        'creativity', 'adaptability', 'time management', 'collaboration', 'presentation'
    ]
    
    for skill in soft_skills_keywords:
        if skill in text_to_check:
            ss_base += 0.05
            
    # Cap base score at 0.7
    ss_base = min(0.7, ss_base)
    
    # 2. Soft Skill Course Boost (SS_course)
    # Count completed soft skill courses
    completed_courses = db.query(UserCourse).join(Course).filter(
        UserCourse.user_id == profile.user_id,
        UserCourse.status == 'completed',
        Course.category == 'soft_skill'
    ).count()
    
    # Each course contributes ~0.03 (to reach ~0.3 with 10 courses)
    ss_course = (completed_courses / 10) * 0.29
    
    # Final SS = min(SS_base + SS_course, 0.99)
    ss_final = min(0.99, ss_base + ss_course)
    
    return _norm(ss_final)

def calculate_market_factors(profile: Any, target_role: Dict) -> Tuple[float, float, float, float]:
    """Calculate Market Factor = (0.6 * RD) + (0.4 * (1 - RDf))"""
    # Role Demand (RD)
    role_demand = 0.5  # Default
    if target_role:
        role_name = target_role.get('job_role', '').lower()
        high_demand_roles = ['data scientist', 'software engineer', 'ai engineer', 'cloud engineer', 'devops', 'full stack']
        if any(role in role_name for role in high_demand_roles):
            role_demand = 0.8
        elif 'analyst' in role_name:
            role_demand = 0.7
    
    # Role Difficulty (RDf)
    role_difficulty = 0.3  # Default
    if target_role:
        level = target_role.get('level', '').lower()
        if 'senior' in level:
            role_difficulty = 0.8
        elif 'mid' in level:
            role_difficulty = 0.6
        elif 'entry' in level or 'junior' in level:
            role_difficulty = 0.4
            
    # Salary Fit (SF) - kept for reference
    salary_fit = 0.6
    
    # Market Factor Formula: (0.6 * RD) + (0.4 * (1 - RDf))
    market_factor = (0.6 * role_demand) + (0.4 * (1.0 - role_difficulty))
    
    return _norm(market_factor), role_demand, role_difficulty, salary_fit

def calculate_meta_factors(db: Session, user_id: int, profile: Any) -> Tuple[float, float, float]:
    """Calculate Meta Factor = (0.8 * EC) + (0.2 * DC)"""
    # Evidence Confidence (EC)
    documents = list_documents(db, user_id)
    avg_confidence = 0.5  # Default start
    
    if documents:
        confidences = [doc.ocr_confidence for doc in documents if doc.ocr_confidence is not None]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            # Boost if verified
            verified_count = sum(1 for doc in documents if doc.verification_status == 'verified')
            if verified_count > 0:
                avg_confidence += 0.2
    
    evidence_confidence = _norm(avg_confidence)
    
    # Data Completeness (DC)
    completeness_score = 0.0
    if profile.education_level: completeness_score += 0.1
    if profile.skills and len(profile.skills) > 10: completeness_score += 0.1
    if profile.interests: completeness_score += 0.1
    if profile.bio and len(profile.bio) > 50: completeness_score += 0.1
    if profile.name: completeness_score += 0.1
    if profile.contact_email: completeness_score += 0.1
    if profile.career_direction: completeness_score += 0.1
    if profile.linkedin_url: completeness_score += 0.1
    if documents: completeness_score += 0.2
    
    data_completeness = _norm(completeness_score)
    
    # Meta Factor Formula: (0.8 * EC) + (0.2 * DC)
    meta_factor = (0.8 * evidence_confidence) + (0.2 * data_completeness)
    
    return _norm(meta_factor), evidence_confidence, data_completeness

def get_target_role_for_profile(profile: Any) -> Dict:
    """Get the most suitable target role based on profile"""
    kb = load_kb()
    
    # Simple matching based on skills and interests
    profile_text = f"{profile.skills or ''} {profile.interests or ''} {profile.bio or ''}".lower()
    
    best_match = None
    best_score = 0
    
    for _, row in kb.iterrows():
        role_text = f"{row.get('technical_skills', '')} {row.get('domain_skills', '')} {row.get('job_role', '')}".lower()
        
        # Simple word overlap scoring
        profile_words = set(profile_text.split())
        role_words = set(role_text.split())
        
        overlap = len(profile_words & role_words)
        score = overlap / max(len(role_words), 1)
        
        if score > best_score:
            best_score = score
            best_match = row.to_dict()
    
    return best_match or {}

def calculate_metrics(db: Session, profile: Any) -> dict:
    """Calculate all metrics according to Updated Framework"""
    # Get target role
    target_role = get_target_role_for_profile(profile)
    target_skills = []
    
    if target_role and 'technical_skills' in target_role:
        tech_skills = str(target_role['technical_skills'])
        target_skills = [skill.strip() for skill in tech_skills.split(',') if skill.strip()]
    
    # Calculate Layer 1: Core Readiness Factors
    soft_skills = calculate_soft_skills_score(db, profile)  # SS
    domain_score = calculate_domain_score(profile, target_skills)  # DS
    practical_score = calculate_practical_score(profile)  # P
    
    # Calculate Layer 2: Market Factors
    market_factor, role_demand, role_difficulty, salary_fit = calculate_market_factors(profile, target_role)
    
    # Calculate Layer 3: Meta Factors
    meta_factor, evidence_confidence, data_completeness = calculate_meta_factors(db, profile.user_id, profile)
    
    # Legacy metrics for backward compatibility
    degree_score = calculate_degree_score(profile.education_level)
    experience_score = calculate_experience_score(getattr(profile, 'experience_years', 0))
    certificate_quality = 0.0 # Deprecated in new formula, but kept for structure
    
    return {
        'SS': soft_skills,
        'DS': domain_score,
        'P': practical_score,
        'MarketFactor': market_factor,
        'MetaFactor': meta_factor,
        'RD': role_demand,
        'RDf': role_difficulty,
        'EC': evidence_confidence,
        'DC': data_completeness,
        'SF': salary_fit,
        'D': degree_score,
        'E': experience_score,
        'CQ': certificate_quality,
        'target_role': target_role
    }

def compute_score(db: Session, profile: Any) -> tuple[int, list[str], list[str], dict, float]:
    """Compute career readiness score according to Updated Framework"""
    try:
        if not profile:
            raise ProfileNotFoundError("Student profile not found")
        
        logger.info(f"Computing career score for user {profile.user_id}")
        
        # Calculate all metrics
        m = calculate_metrics(db, profile)
        
        # CoreScore = (0.60 * SS) + (0.25 * DS) + (0.15 * P)
        core_score = (0.60 * m['SS']) + (0.25 * m['DS']) + (0.15 * m['P'])
        
        # AdjustedScore = CoreScore * MarketFactor * MetaFactor
        adjusted_score = core_score * m['MarketFactor'] * m['MetaFactor']
        
        # Final Score = round(100 * AdjustedScore)
        final = round(100 * adjusted_score)
        
        # Ensure score is within valid range
        final = max(0, min(100, final))
        
        logger.info(f"Career score computed successfully: {final}")
        
    except Exception as e:
        logger.error(f"Error computing career score: {str(e)}")
        if isinstance(e, (ProfileNotFoundError, KnowledgeBaseError)):
            raise
        raise ScoringError(f"Failed to compute career score: {str(e)}")
    
    # Generate strengths and improvements
    strengths = []
    improvements = []
    
    # Analyze strengths
    if m['SS'] > 0.6: strengths.append("Strong soft skills foundation")
    if m['DS'] > 0.6: strengths.append("Good technical skill coverage")
    if m['P'] > 0.5: strengths.append("Practical experience evident")
    if m['EC'] > 0.7: strengths.append("High confidence in evidence")
    if m['MarketFactor'] > 0.7: strengths.append("Role aligns well with market demand")
    
    # Analyze improvements
    if m['SS'] < 0.5: improvements.append("Complete soft skill courses to boost score")
    if m['DS'] < 0.4: improvements.append("Acquire more domain-specific skills")
    if m['P'] < 0.3: improvements.append("Undertake more projects or internships")
    if m['DC'] < 0.6: improvements.append("Complete your profile details")
    if m['EC'] < 0.5: improvements.append("Upload verified certificates")
    
    breakdown = {
        'soft_skills': round(m['SS'], 3),
        'skill_coverage': round(m['DS'], 3),  # Mapping DS to skill_coverage for frontend compat
        'practical_evidence': round(m['P'], 3),
        'market_factor': round(m['MarketFactor'], 3),
        'meta_factor': round(m['MetaFactor'], 3),
        'role_demand': round(m['RD'], 3),
        'role_difficulty': round(m['RDf'], 3),
        'evidence_confidence': round(m['EC'], 3),
        'data_completeness': round(m['DC'], 3),
        'degree_score': round(m['D'], 3),
        'experience_score': round(m['E'], 3),
        'certificate_quality': round(m['CQ'], 3)
    }
    
    return final, strengths, improvements, breakdown, m['MetaFactor']

def persist_score(db: Session, user_id: int, final: int, breakdown: dict, confidence: float) -> Any:
    from app.models.career_score import CareerScore
    cs = CareerScore(
        user_id=user_id,
        total_score=final,
        degree_score=breakdown['degree_score'],
        experience_score=breakdown['experience_score'],
        skill_coverage_score=breakdown['skill_coverage'],
        certificate_quality_score=breakdown['certificate_quality'],
        practical_evidence_score=breakdown['practical_evidence'],
        soft_skills_score=breakdown['soft_skills'],
        confidence=confidence,
        # New metrics
        market_factor=breakdown.get('market_factor'),
        meta_factor=breakdown.get('meta_factor'),
        role_demand=breakdown.get('role_demand'),
        role_difficulty=breakdown.get('role_difficulty'),
        evidence_confidence=breakdown.get('evidence_confidence'),
        data_completeness=breakdown.get('data_completeness')
    )
    db.add(cs)
    db.commit()
    db.refresh(cs)
    return cs

def recommend(db: Session, profile: Any) -> tuple[list[str], list[str]]:
    """Generate job recommendations and skill gaps based on profile and KB"""
    kb = load_kb()
    
    # Get profile skills and interests
    profile_text = f"{profile.skills or ''} {profile.interests or ''} {profile.bio or ''}".lower()
    profile_skills = _extract_skills_from_text(profile_text)
    
    # Find matching roles from KB
    role_matches = []
    
    for _, row in kb.iterrows():
        role_dict = row.to_dict()
        role_text = f"{role_dict.get('technical_skills', '')} {role_dict.get('domain_skills', '')} {role_dict.get('job_role', '')}".lower()
        
        # Calculate match score
        role_skills = _extract_skills_from_text(role_text)
        
        if role_skills:
            matched_skills = sum(1 for skill in role_skills if any(ps in skill or skill in ps for ps in profile_skills))
            match_score = matched_skills / len(role_skills) if role_skills else 0
        else:
            # Fallback to text similarity
            profile_words = set(profile_text.split())
            role_words = set(role_text.split())
            match_score = len(profile_words & role_words) / max(len(role_words), 1)
        
        if match_score > 0.1:  # Minimum threshold
            role_matches.append({
                'role': role_dict.get('job_role', 'Unknown Role'),
                'level': role_dict.get('level', 'Entry'),
                'salary': role_dict.get('average_salary', 'Not specified'),
                'skills_required': role_dict.get('technical_skills', ''),
                'match_score': match_score
            })
    
    # Sort by match score and take top 5
    role_matches.sort(key=lambda x: x['match_score'], reverse=True)
    top_roles = role_matches[:5]
    
    # Extract job names
    job_recommendations = [role['role'] for role in top_roles]
    
    # Calculate skill gaps
    skills_to_learn = set()
    
    for role in top_roles:
        required_skills = role['skills_required']
        if required_skills:
            role_skills = [skill.strip().lower() for skill in required_skills.split(',')]
            for skill in role_skills:
                # Check if skill is missing from profile
                if not any(ps in skill or skill in ps for ps in profile_skills):
                    skills_to_learn.add(skill.title())
    
    # Add some common high-value skills if missing
    common_skills = ['SQL', 'Python', 'Git', 'Communication', 'Problem Solving']
    for skill in common_skills:
        if not any(skill.lower() in ps.lower() for ps in profile_skills):
            skills_to_learn.add(skill)
    
    skills_to_learn = list(skills_to_learn)[:10]  # Limit to top 10
    
    # Fallback if no matches found
    if not job_recommendations:
        job_recommendations = ['Software Developer Intern', 'Data Analyst Intern', 'Business Analyst Intern']
    
    return job_recommendations, skills_to_learn
