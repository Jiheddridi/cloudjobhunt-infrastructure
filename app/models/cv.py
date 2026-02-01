"""
CloudJobHunt CV Model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class CV(Base):
    """CV/Resume model for user profiles"""
    
    __tablename__ = "cv"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile information
    summary = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)  # JSON string or comma-separated
    languages = Column(Text, nullable=True)
    
    # Experience
    years_of_experience = Column(Integer, nullable=True)
    current_title = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    
    # Education
    education = Column(Text, nullable=True)
    
    # Raw CV data
    raw_data = Column(JSON, nullable=True)  # Full parsed CV data
    
    # File reference
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cv")
    
    def __repr__(self):
        return f"<CV for user {self.user_id}>"
