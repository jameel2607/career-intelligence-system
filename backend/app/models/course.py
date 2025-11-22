from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)  # 'soft_skill', 'domain', 'project'
    description = Column(Text, nullable=True)
    duration_hours = Column(Integer, nullable=True)
    score_impact = Column(Float, nullable=True)  # Expected CRS boost
    target_component = Column(String(50), nullable=True)  # 'soft_skills', 'skill_coverage', etc.
    difficulty = Column(String(20), nullable=True)  # 'beginner', 'intermediate', 'advanced'
    url = Column(String(500), nullable=True)
    provider = Column(String(100), nullable=True)  # 'Coursera', 'Udemy', 'Internal'
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
