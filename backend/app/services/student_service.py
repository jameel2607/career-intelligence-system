from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def get_by_user_id(db: Session, user_id: int) -> Student | None:
    return db.query(Student).filter(Student.user_id == user_id).first()

def create_profile(db: Session, user_id: int, data: StudentCreate) -> Student:
    profile = Student(
        user_id=user_id,
        education_level=data.education_level,
        skills=data.skills,
        interests=data.interests,
        bio=data.bio,
        experience_years=data.experience_years,
        target_salary=data.target_salary
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def update_profile(db: Session, profile: Student, data: StudentUpdate) -> Student:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(profile, k, v)
    db.commit()
    db.refresh(profile)
    return profile

