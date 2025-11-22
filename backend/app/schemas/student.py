from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, Dict
from datetime import datetime

class StudentBase(BaseModel):
    # Journey tracking (read-only, managed by system)
    # journey_stage and completion_percentage are not in base as they're auto-calculated
    
    # Basic profile fields (existing)
    education_level: Optional[str] = Field(None, max_length=100, description="Educational qualification level")
    skills: Optional[str] = Field(None, max_length=2000, description="Technical and professional skills")
    interests: Optional[str] = Field(None, max_length=1000, description="Career interests and preferences")
    bio: Optional[str] = Field(None, max_length=2000, description="Professional biography")
    experience_years: Optional[float] = Field(None, ge=0, le=50, description="Years of professional experience")
    target_salary: Optional[float] = Field(None, ge=0, description="Target salary expectation")
    
    # Enhanced profile fields (new)
    name: Optional[str] = Field(None, max_length=200, description="Full name")
    contact_email: Optional[str] = Field(None, max_length=200, description="Contact email address")
    contact_phone: Optional[str] = Field(None, max_length=50, description="Contact phone number")
    career_direction: Optional[str] = Field(None, description="Career direction preference")
    language_fluency: Optional[Dict[str, str]] = Field(None, description="Language proficiency levels")
    medium_of_instruction_10: Optional[str] = Field(None, max_length=50, description="Medium of instruction in 10th grade")
    medium_of_instruction_12: Optional[str] = Field(None, max_length=50, description="Medium of instruction in 12th grade")
    gpa_percentile: Optional[float] = Field(None, ge=0, le=100, description="GPA or percentile")
    linkedin_url: Optional[str] = Field(None, max_length=500, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub profile URL")

    @validator('education_level')
    def validate_education_level(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            valid_levels = [
                'high school', 'secondary', 'diploma', 'associate', 'certificate',
                'bachelor', 'bachelors', 'bsc', 'ba', 'btech', 'be', 'bcom', 'bba',
                'master', 'masters', 'msc', 'ma', 'mba', 'mtech', 'me', 'mca', 'mcom',
                'phd', 'doctorate', 'ph.d', 'bca', 'bcs', 'bds', 'mbbs', 'md', 'ms'
            ]
            if not any(level in v.lower() for level in valid_levels):
                raise ValueError('Invalid education level')
        return v

    @validator('skills')
    def validate_skills(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            if len(v) < 10:
                raise ValueError('Skills description should be at least 10 characters')
        return v

    @validator('interests')
    def validate_interests(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v

    @validator('bio')
    def validate_bio(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
        return v
    
    @validator('career_direction')
    def validate_career_direction(cls, v):
        if v is not None:
            valid_directions = ['job', 'higher_studies_india', 'higher_studies_abroad', 'entrepreneurship', 'not_sure']
            if v not in valid_directions:
                raise ValueError(f'Career direction must be one of: {", ".join(valid_directions)}')
        return v
    
    @validator('linkedin_url', 'github_url')
    def validate_url(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            if not v.startswith('http://') and not v.startswith('https://'):
                v = 'https://' + v
        return v
    
    @validator('contact_email')
    def validate_email(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            if '@' not in v:
                raise ValueError('Invalid email address')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int
    user_id: int
    journey_stage: int
    completion_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

