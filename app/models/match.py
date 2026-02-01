"""
CloudJobHunt Job Match Model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base


class JobMatch(Base):
    """Job match model for tracking user-job matches"""
    
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Match score (0-100)
    match_score = Column(Float, nullable=True)
    
    # Match details
    matched_skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    match_explanation = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default="new")  # new, viewed, saved, applied, rejected
    is_favorite = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    
    # Timestamps
    matched_at = Column(DateTime, default=datetime.utcnow)
    viewed_at = Column(DateTime, nullable=True)
    applied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")
    
    # Unique constraint
    __table_args__ = (
        {"schema": None},
    )
    
    def __repr__(self):
        return f"<JobMatch user={self.user_id} job={self.job_id} score={self.match_score}>"
