from pydantic import BaseModel

class CareerScoreRead(BaseModel):
    score: int
    strengths: list[str]
    improvements: list[str]

class RecommendationRead(BaseModel):
    job_roles: list[str]
    skills_to_learn: list[str]

