from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, func, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    
    # Journey tracking fields
    journey_stage = Column(Integer, default=1)  # 1-5 stages
    completion_percentage = Column(Float, default=0.0)  # 0-100
    
    # Basic profile fields (existing)
    education_level = Column(String(100), nullable=True)
    skills = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    experience_years = Column(Float, nullable=True, default=0.0)
    target_salary = Column(Float, nullable=True)
    
    # Enhanced profile fields (new)
    name = Column(String(200), nullable=True)
    contact_email = Column(String(200), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    career_direction = Column(String(50), nullable=True)  # 'job', 'higher_studies_india', 'higher_studies_abroad', 'entrepreneurship', 'not_sure'
    language_fluency = Column(JSON, nullable=True)  # {'english': 'fluent', 'hindi': 'native'}
    medium_of_instruction_10 = Column(String(50), nullable=True)
    medium_of_instruction_12 = Column(String(50), nullable=True)
    gpa_percentile = Column(Float, nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")

