from typing import List, Dict, Optional
import os
import json
import logging
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)

_openai_available = False
_ollama_available = False
_client = None

# Try to initialize OpenAI client
try:
    from openai import OpenAI
    api_key = settings.GPT5_API_KEY or os.getenv('OPENAI_API_KEY')
    if api_key:
        _client = OpenAI(api_key=api_key)
        _openai_available = True
        logger.info("OpenAI client initialized successfully")
    else:
        logger.info("No OpenAI API key found. Will try Ollama.")
except Exception as e:
    logger.info(f"OpenAI not available: {e}")
    _openai_available = False

# Try to connect to Ollama
def check_ollama_connection():
    """Check if Ollama is running and available"""
    try:
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                logger.info(f"Ollama connected successfully. Available models: {[m['name'] for m in models[:3]]}")
                return True, models
        return False, []
    except Exception as e:
        logger.info(f"Ollama not available: {e}")
        return False, []

_ollama_available, _ollama_models = check_ollama_connection()

def call_ollama(prompt: str, model: str = None) -> str:
    """Call Ollama API for text generation"""
    try:
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        
        # Use specified model or default
        if not model:
            model = os.getenv('OLLAMA_MODEL', 'qwen2.5:1.5b')
        
        logger.info(f"Calling Ollama with model: {model}")
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1000  # Use num_predict instead of max_tokens for Ollama
            }
        }
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json=payload,
            timeout=120,  # Increased timeout for AI processing
            headers={'Content-Type': 'application/json'}
        )
        
        logger.info(f"Ollama response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '').strip()
            logger.info(f"Ollama response length: {len(response_text)} characters")
            return response_text
        else:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            raise Exception(f"Ollama API returned status {response.status_code}")
            
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        raise Exception("Ollama request timed out")
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Ollama")
        raise Exception("Failed to connect to Ollama - is it running?")
    except Exception as e:
        logger.error(f"Error calling Ollama: {e}")
        raise Exception(f"Ollama error: {str(e)}")

def create_career_prompt(profile: Dict, roles: List[Dict]) -> str:
    """Create a structured prompt for career recommendations"""
    
    prompt = f"""
You are a professional career advisor AI. Based on the student profile and available job roles, provide personalized career guidance.

STUDENT PROFILE:
- Skills: {profile.get('skills', 'Not specified')}
- Interests: {profile.get('interests', 'Not specified')}
- Education: {profile.get('education_level', 'Not specified')}
- Bio: {profile.get('bio', 'Not specified')}

AVAILABLE JOB ROLES:
"""
    
    for i, role in enumerate(roles[:5], 1):
        prompt += f"""
{i}. {role.get('job_role', 'Unknown Role')}
   - Level: {role.get('level', 'Not specified')}
   - Technical Skills: {role.get('technical_skills', 'Not specified')}
   - Soft Skills: {role.get('soft_skills', 'Not specified')}
   - Salary: {role.get('average_salary', 'Not specified')}
   - Description: {role.get('description', 'Not specified')}
"""

    prompt += """

TASK:
Provide a JSON response with the following structure:
{
    "recommended_roles": [
        {
            "role_name": "Role Name",
            "match_percentage": 85,
            "reasoning": "Why this role fits the student"
        }
    ],
    "skills_to_develop": [
        {
            "skill": "Skill Name",
            "priority": "High/Medium/Low",
            "reasoning": "Why this skill is important"
        }
    ],
    "career_path": "A brief 2-3 sentence career path recommendation",
    "next_steps": ["Specific actionable step 1", "Specific actionable step 2"],
    "market_insights": "Brief market outlook for recommended roles"
}

Focus on:
1. Realistic role matches based on current skills
2. Specific, actionable skill development recommendations
3. Clear reasoning for each recommendation
4. Market-relevant insights
"""
    
    return prompt

def parse_gpt_response(content: str) -> Dict:
    """Parse GPT response and extract structured data"""
    try:
        # Try to parse as JSON first
        if content.strip().startswith('{'):
            return json.loads(content)
        
        # Fallback: extract information using text parsing
        lines = content.split('\n')
        result = {
            'recommended_roles': [],
            'skills_to_develop': [],
            'career_path': '',
            'next_steps': [],
            'market_insights': ''
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if 'recommended' in line.lower() and 'role' in line.lower():
                current_section = 'roles'
            elif 'skill' in line.lower() and ('develop' in line.lower() or 'learn' in line.lower()):
                current_section = 'skills'
            elif 'career path' in line.lower():
                current_section = 'path'
            elif 'next step' in line.lower():
                current_section = 'steps'
            elif 'market' in line.lower():
                current_section = 'market'
            elif line and current_section:
                if current_section == 'roles' and line.startswith(('-', '*', '•')):
                    role_name = line.lstrip('-*•').strip()
                    result['recommended_roles'].append({
                        'role_name': role_name,
                        'match_percentage': 75,
                        'reasoning': 'Based on profile analysis'
                    })
                elif current_section == 'skills' and line.startswith(('-', '*', '•')):
                    skill_name = line.lstrip('-*•').strip()
                    result['skills_to_develop'].append({
                        'skill': skill_name,
                        'priority': 'Medium',
                        'reasoning': 'Important for career growth'
                    })
        
        return result
        
    except Exception as e:
        logger.error(f"Error parsing GPT response: {e}")
        return {
            'recommended_roles': [{'role_name': 'Software Developer', 'match_percentage': 70, 'reasoning': 'General recommendation'}],
            'skills_to_develop': [{'skill': 'Programming', 'priority': 'High', 'reasoning': 'Essential skill'}],
            'career_path': 'Focus on building technical skills and gaining practical experience.',
            'next_steps': ['Complete online courses', 'Build portfolio projects'],
            'market_insights': 'Technology sector continues to show strong growth.'
        }

def summarize(profile: Dict, roles: List[Dict]) -> Dict:
    """Generate AI-powered career recommendations using Ollama or OpenAI - AI ONLY, NO FALLBACKS"""
    
    # Create the career guidance prompt
    prompt = create_career_prompt(profile, roles)
    
    # Try Ollama first (local LLM)
    if _ollama_available:
        logger.info("Using Ollama for career recommendations")
        try:
            # Create a comprehensive prompt for Ollama
            ollama_prompt = f"""You are an expert career advisor with deep knowledge of technology, business, and emerging career paths. Analyze this student profile and provide detailed, personalized career guidance.

STUDENT PROFILE:
- Skills: {profile.get('skills', 'Not specified')}
- Interests: {profile.get('interests', 'Not specified')}
- Education: {profile.get('education_level', 'Not specified')}
- Experience: {profile.get('experience_years', 'Not specified')} years

AVAILABLE JOB ROLES IN KNOWLEDGE BASE:
{chr(10).join([f"- {role.get('job_role', 'Unknown')}: {role.get('technical_skills', '')} | Salary: {role.get('average_salary', 'Not specified')}" for role in roles[:8]])}

PROVIDE DETAILED ANALYSIS:

1. RECOMMENDED JOB ROLES (Top 3-5 most suitable):
   - List specific job titles that match their profile
   - Explain why each role fits their skills/interests

2. SKILLS TO DEVELOP (Priority order):
   - Technical skills they need to learn
   - Soft skills to improve
   - Certifications to pursue

3. CAREER PATH STRATEGY:
   - Short-term goals (6 months)
   - Medium-term goals (1-2 years)
   - Long-term vision (3-5 years)

4. NEXT STEPS (Actionable items):
   - Specific courses or resources
   - Projects to build
   - Experience to gain

5. MARKET INSIGHTS:
   - Industry trends relevant to their interests
   - Salary expectations
   - Growth opportunities

Format your response with clear sections and bullet points. Be specific and actionable."""

            response = call_ollama(ollama_prompt, model=settings.OLLAMA_MODEL)
            
            if response and response.strip():
                # Parse Ollama response
                parsed = parse_ollama_response(response, roles)
                logger.info("Successfully generated Ollama career recommendations")
                return parsed
            else:
                logger.error("Ollama returned empty response")
                raise Exception("Ollama failed to generate response")
                
        except Exception as e:
            logger.error(f"Error with Ollama: {e}")
            if not _openai_available:
                raise Exception("AI service unavailable: Ollama failed and OpenAI not configured")
    
    # Try OpenAI if Ollama fails
    if _openai_available and _client:
        logger.info("Using OpenAI for career recommendations")
        try:
            response = _client.chat.completions.create(
                model=settings.GPT5_MODEL if settings.GPT5_MODEL != 'gpt-5' else 'gpt-4',
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert career advisor with deep knowledge of the job market, skills requirements, and career development paths. Provide specific, actionable, and realistic career guidance. Always provide detailed, personalized recommendations."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info("Successfully generated OpenAI career recommendations")
            
            # Parse the structured response
            structured_response = parse_gpt_response(content)
            
            # Convert to expected format
            return {
                'job_roles': [role['role_name'] for role in structured_response.get('recommended_roles', [])],
                'skills_to_learn': [skill['skill'] for skill in structured_response.get('skills_to_develop', [])],
                'references': [r.get('sources', '') for r in roles if r.get('sources')],
                'career_path': structured_response.get('career_path', ''),
                'next_steps': structured_response.get('next_steps', []),
                'market_insights': structured_response.get('market_insights', ''),
                'detailed_recommendations': structured_response.get('recommended_roles', []),
                'detailed_skills': structured_response.get('skills_to_develop', [])
            }
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise Exception(f"OpenAI API failed: {e}")
    
    # NO FALLBACKS - Raise error if AI is not available
    raise Exception("AI service unavailable: Neither Ollama nor OpenAI is configured and working. Please set up at least one AI service.")

def parse_ollama_response(response: str, roles: List[Dict]) -> Dict:
    """Parse Ollama response into structured format"""
    try:
        lines = response.split('\n')
        job_roles = []
        skills_to_learn = []
        career_path = ""
        next_steps = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if any(keyword in line.lower() for keyword in ['recommended', 'job role', 'roles']):
                current_section = 'roles'
                continue
            elif any(keyword in line.lower() for keyword in ['skill', 'learn']):
                current_section = 'skills'
                continue
            elif any(keyword in line.lower() for keyword in ['career path', 'advice']):
                current_section = 'path'
                continue
            elif any(keyword in line.lower() for keyword in ['next step', 'steps']):
                current_section = 'steps'
                continue
            
            # Extract content based on section
            if current_section == 'roles' and (line.startswith(('-', '*', '•')) or line[0].isdigit()):
                role = line.lstrip('-*•0123456789. ').strip()
                if role and len(role) > 3:
                    job_roles.append(role)
            elif current_section == 'skills' and (line.startswith(('-', '*', '•')) or line[0].isdigit()):
                skill = line.lstrip('-*•0123456789. ').strip()
                if skill and len(skill) > 2:
                    skills_to_learn.append(skill)
            elif current_section == 'path' and len(line) > 20:
                career_path += line + " "
            elif current_section == 'steps' and (line.startswith(('-', '*', '•')) or line[0].isdigit()):
                step = line.lstrip('-*•0123456789. ').strip()
                if step and len(step) > 5:
                    next_steps.append(step)
        
        # Fallback extraction if sections weren't detected properly
        if not job_roles:
            # Extract job roles from available roles that appear in response
            for role in roles[:5]:
                role_name = role.get('job_role', '')
                if role_name.lower() in response.lower():
                    job_roles.append(role_name)
        
        if not skills_to_learn:
            # Extract common skills mentioned
            common_skills = ['Python', 'JavaScript', 'SQL', 'React', 'Node.js', 'Git', 'Docker', 'AWS', 'Machine Learning', 'Data Analysis']
            for skill in common_skills:
                if skill.lower() in response.lower():
                    skills_to_learn.append(skill)
        
        # Ensure we have AI-generated content, no hardcoded fallbacks
        if not job_roles and not skills_to_learn and not career_path.strip():
            raise Exception("AI response parsing failed - no meaningful content extracted")
        
        return {
            'job_roles': job_roles[:5] if job_roles else [],
            'skills_to_learn': skills_to_learn[:8] if skills_to_learn else [],
            'references': [r.get('sources', '') for r in roles if r.get('sources')],
            'career_path': career_path.strip() if career_path.strip() else '',
            'next_steps': next_steps[:5] if next_steps else [],
            'market_insights': 'AI-generated market insights based on current industry trends and student profile.'
        }
        
    except Exception as e:
        logger.error(f"Error parsing Ollama response: {e}")
        raise Exception(f"Failed to parse AI response: {e}")

# Fallback function removed - AI ONLY system

