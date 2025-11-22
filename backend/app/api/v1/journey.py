"""
Journey API - Endpoints for user journey tracking and progress
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.student import Student
from app.services import journey_service
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class JourneyStatusResponse(BaseModel):
    stage: int
    completion_percentage: float
    next_actions: List[Dict[str, str]]
    encouraging_message: str
    can_access_stages: Dict[int, bool]

@router.get('/status', response_model=JourneyStatusResponse)
def get_journey_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current journey status including stage, completion %, and next actions
    """
    # Get or create student profile
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        # Create minimal profile if doesn't exist
        student = Student(user_id=current_user.id)
        db.add(student)
        db.commit()
        db.refresh(student)
    
    # Update journey progress
    stage, completion = journey_service.update_journey_progress(db, student)
    
    # Get next actions
    next_actions = journey_service.get_next_actions(db, student)
    
    # Get encouraging message
    message = journey_service.get_encouraging_message(stage, completion)
    
    # Check which stages can be accessed
    can_access = {
        1: True,  # Always accessible
        2: journey_service.can_unlock_stage(db, student, 2),
        3: journey_service.can_unlock_stage(db, student, 3),
        4: journey_service.can_unlock_stage(db, student, 4),
        5: journey_service.can_unlock_stage(db, student, 5),
    }
    
    return {
        'stage': stage,
        'completion_percentage': completion,
        'next_actions': next_actions,
        'encouraging_message': message,
        'can_access_stages': can_access
    }

@router.post('/refresh')
def refresh_journey_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually refresh journey status (useful after profile updates)
    """
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    stage, completion = journey_service.update_journey_progress(db, student)
    
    return {
        'message': 'Journey status refreshed',
        'stage': stage,
        'completion_percentage': completion
    }
