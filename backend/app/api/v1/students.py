from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.student import StudentCreate, StudentUpdate, StudentRead
from app.services.student_service import get_by_user_id, create_profile, update_profile

router = APIRouter()

@router.get("/me", response_model=StudentRead)
def get_me(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.post("/me", response_model=StudentRead, status_code=201)
def create_me(data: StudentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing = get_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return create_profile(db, current_user.id, data)

@router.put("/me", response_model=StudentRead)
def update_me(data: StudentUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return update_profile(db, profile, data)

