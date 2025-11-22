"""
Journey Service - Manages user journey stages and progress tracking
"""
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.document import Document
from app.models.career_score import CareerScore
from typing import Tuple, List, Dict

def calculate_completion_percentage(db: Session, student: Student) -> float:
    """
    Calculate overall profile completion percentage (0-100)
    Based on: profile fields, documents uploaded, score generated
    """
    completion = 0.0
    total_weight = 100.0
    
    # Profile completion (60% weight)
    profile_fields = {
        'education_level': 5,
        'skills': 10,
        'interests': 5,
        'bio': 5,
        'experience_years': 5,
        'target_salary': 3,
        'name': 5,
        'contact_email': 3,
        'career_direction': 8,
        'language_fluency': 3,
        'linkedin_url': 4,
        'github_url': 4,
    }
    
    for field, weight in profile_fields.items():
        value = getattr(student, field, None)
        if value is not None and value != '' and value != {}:
            completion += weight
    
    # Documents uploaded (20% weight)
    doc_count = db.query(Document).filter(Document.user_id == student.user_id).count()
    if doc_count >= 1:
        completion += 5
    if doc_count >= 2:
        completion += 5
    if doc_count >= 3:
        completion += 5
    if doc_count >= 5:
        completion += 5
    
    # Career score generated (20% weight)
    score_exists = db.query(CareerScore).filter(CareerScore.user_id == student.user_id).first()
    if score_exists:
        completion += 20
    
    return min(completion, 100.0)


def get_current_stage(db: Session, student: Student) -> int:
    """
    Determine current journey stage (1-5) based on completion criteria
    Stage 1: Profile Onboarding
    Stage 2: Upload & Verification
    Stage 3: CRS Generation
    Stage 4: Pathway Navigation
    Stage 5: Improvement Actions
    """
    # Stage 1: Always accessible
    stage = 1
    
    # Stage 2: Profile basics completed
    if (student.education_level and student.skills and 
        student.experience_years is not None and student.career_direction):
        stage = 2
    
    # Stage 3: At least 1 document uploaded
    doc_count = db.query(Document).filter(Document.user_id == student.user_id).count()
    if stage >= 2 and doc_count >= 1:
        stage = 3
    
    # Stage 4: Career score generated
    score_exists = db.query(CareerScore).filter(CareerScore.user_id == student.user_id).first()
    if stage >= 3 and score_exists:
        stage = 4
    
    # Stage 5: Viewed pathways (auto-unlock after stage 4)
    if stage >= 4:
        stage = 5
    
    return stage


def can_unlock_stage(db: Session, student: Student, target_stage: int) -> bool:
    """
    Check if user can access a specific stage
    """
    current_stage = get_current_stage(db, student)
    return target_stage <= current_stage


def get_next_actions(db: Session, student: Student) -> List[Dict[str, str]]:
    """
    Get smart CTA suggestions based on current stage and completion
    Returns list of actions with title, description, and link
    """
    actions = []
    current_stage = get_current_stage(db, student)
    
    # Stage 1: Complete profile
    if current_stage == 1:
        if not student.education_level:
            actions.append({
                'title': 'Add Education Level',
                'description': 'Select your highest qualification',
                'link': '/profile',
                'priority': 'high'
            })
        if not student.skills or len(student.skills) < 10:
            actions.append({
                'title': 'Add Your Skills',
                'description': 'List your technical and soft skills',
                'link': '/profile',
                'priority': 'high'
            })
        if not student.career_direction:
            actions.append({
                'title': 'Choose Career Direction',
                'description': 'Select your career path preference',
                'link': '/profile',
                'priority': 'high'
            })
        if student.experience_years is None:
            actions.append({
                'title': 'Add Experience',
                'description': 'Enter your years of experience',
                'link': '/profile',
                'priority': 'medium'
            })
    
    # Stage 2: Upload documents
    elif current_stage == 2:
        doc_count = db.query(Document).filter(Document.user_id == student.user_id).count()
        if doc_count == 0:
            actions.append({
                'title': 'Upload Your First Certificate',
                'description': 'Add certificates to boost your score',
                'link': '/documents',
                'priority': 'high'
            })
        elif doc_count < 3:
            actions.append({
                'title': f'Upload More Certificates ({doc_count}/3)',
                'description': 'More certificates = higher career score',
                'link': '/documents',
                'priority': 'medium'
            })
    
    # Stage 3: Generate score
    elif current_stage == 3:
        score_exists = db.query(CareerScore).filter(CareerScore.user_id == student.user_id).first()
        if not score_exists:
            actions.append({
                'title': 'Generate Your Career Score',
                'description': 'See your career readiness analysis',
                'link': '/career-analysis',
                'priority': 'high'
            })
    
    # Stage 4: Explore pathways
    elif current_stage == 4:
        actions.append({
            'title': 'Explore Career Pathways',
            'description': 'View personalized job recommendations',
            'link': '/career-pathways',
            'priority': 'high'
        })
    
    # Stage 5: Upskilling
    elif current_stage == 5:
        actions.append({
            'title': 'Start Upskilling',
            'description': 'Enroll in courses to boost your score',
            'link': '/upskilling',
            'priority': 'high'
        })
    
    # Always suggest completing profile if not 100%
    completion = calculate_completion_percentage(db, student)
    if completion < 100 and current_stage > 1:
        actions.append({
            'title': f'Complete Your Profile ({int(completion)}%)',
            'description': 'Add missing details for better recommendations',
            'link': '/profile',
            'priority': 'low'
        })
    
    return actions


def get_encouraging_message(stage: int, completion: float) -> str:
    """
    Get context-aware encouraging message based on stage and completion
    """
    messages = {
        1: [
            "Welcome! Let's build your career profile together 🚀",
            "Great start! Complete your profile to unlock career insights",
            "You're on your way! Keep adding your details"
        ],
        2: [
            "Nice progress! Upload certificates to showcase your skills 📜",
            "Looking good! Add your achievements to boost your score",
            "You're just 1 step away from your readiness score!"
        ],
        3: [
            "Excellent! Time to see your career readiness score 📊",
            "Almost there! Generate your score to see where you stand",
            "Ready for insights? Let's analyze your career readiness"
        ],
        4: [
            "Awesome! Explore personalized career pathways 🎯",
            "Great job! Discover roles that match your skills",
            "You're doing amazing! Check out your career options"
        ],
        5: [
            "Outstanding! Start upskilling to reach your goals 🌟",
            "You're career-ready! Keep improving with courses",
            "Fantastic progress! Continue your growth journey"
        ]
    }
    
    stage_messages = messages.get(stage, messages[1])
    
    # Select message based on completion
    if completion < 30:
        return stage_messages[0]
    elif completion < 70:
        return stage_messages[1]
    else:
        return stage_messages[2]


def update_journey_progress(db: Session, student: Student) -> Tuple[int, float]:
    """
    Update student's journey stage and completion percentage
    Returns (new_stage, new_completion)
    """
    new_stage = get_current_stage(db, student)
    new_completion = calculate_completion_percentage(db, student)
    
    student.journey_stage = new_stage
    student.completion_percentage = new_completion
    db.commit()
    db.refresh(student)
    
    return new_stage, new_completion
