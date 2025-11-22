from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class CareerScore(Base):
    __tablename__ = "career_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    total_score = Column(Integer, nullable=False)
    degree_score = Column(Float, nullable=True)
    experience_score = Column(Float, nullable=True)
    skill_coverage_score = Column(Float, nullable=True)
    certificate_quality_score = Column(Float, nullable=True)
    practical_evidence_score = Column(Float, nullable=True)
    soft_skills_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    
    # New metrics (Phase 5)
    market_factor = Column(Float, nullable=True)
    meta_factor = Column(Float, nullable=True)
    role_demand = Column(Float, nullable=True)
    role_difficulty = Column(Float, nullable=True)
    salary_fit = Column(Float, nullable=True)
    evidence_confidence = Column(Float, nullable=True)
    data_completeness = Column(Float, nullable=True)
    
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")

