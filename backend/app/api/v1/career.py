from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas import CareerScoreRead, RecommendationRead, CareerScoreDetail
from app.services.scoring_service import compute_score, recommend, persist_score
from app.services.rag_service import retrieve_roles
from app.services.gpt_service import summarize
from app.services.student_service import get_by_user_id

router = APIRouter()

@router.get('/score', response_model=CareerScoreDetail)
def score(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create your profile first.")
    
    score, strengths, improvements, breakdown, confidence = compute_score(db, profile)
    persist_score(db, current_user.id, score, breakdown, confidence)
    
    return {
        'score': score, 
        'breakdown': breakdown,
        'confidence': confidence,
        'strengths': strengths,
        'improvements': improvements
    }

@router.get('/recommendations', response_model=RecommendationRead)
def recommendations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create your profile first.")
    
    jobs, skills = recommend(db, profile)
    return {
        'job_roles': jobs,
        'skills_to_learn': skills
    }

@router.get('/ai-recommendations')
def ai_recommendations(db: Session = Depends(get_db)):
    # For demo purposes, always return demo data
    return {
        'summary': 'Based on current market trends, you show strong potential in frontend development with React.js and modern web technologies. Consider focusing on full-stack development to increase your market value.',
        'recommendations': [
            'Master React.js ecosystem including Redux and Next.js',
            'Learn backend technologies like Node.js and Express',
            'Gain experience with cloud platforms like AWS or Azure',
            'Build a strong portfolio with 3-5 projects',
            'Contribute to open-source projects to showcase skills'
        ],
        'career_path': 'Frontend Developer → Full Stack Developer → Senior Developer → Tech Lead'
    }
