from pydantic import BaseModel

class ScoreBreakdown(BaseModel):
    degree_score: float
    experience_score: float
    skill_coverage: float
    certificate_quality: float
    practical_evidence: float
    soft_skills: float

class CareerScoreDetail(BaseModel):
    score: int
    breakdown: ScoreBreakdown
    confidence: float

