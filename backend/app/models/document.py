from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=True)
    
    # OCR fields (existing)
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    
    # Verification fields (new)
    verification_status = Column(String(20), default='needs_action')  # 'verified', 'low_trust', 'needs_action'
    provider = Column(String(100), nullable=True)  # 'Coursera', 'Udemy', 'Unknown'
    extracted_skills = Column(JSON, nullable=True)  # ['Python', 'React']
    manual_edits = Column(JSON, nullable=True)  # User corrections
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")

