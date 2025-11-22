from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    score = Column(Integer, nullable=True)
    actions_completed = Column(Integer, default=0)
    courses_completed = Column(Integer, default=0)
    documents_uploaded = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
