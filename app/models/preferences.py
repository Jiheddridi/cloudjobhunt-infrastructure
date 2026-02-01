"""
CloudJobHunt Search Preferences Model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class SearchPreferences(Base):
    """User search preferences for job matching"""
    
    __tablename__ = "search_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Job preferences
    job_titles = Column(Text, nullable=True)  # JSON array or comma-separated
    keywords = Column(Text, nullable=True)
    locations = Column(Text, nullable=True)
    remote_only = Column(Boolean, default=False)
    
    # Company preferences
    company_types = Column(Text, nullable=True)  # startup, enterprise, etc.
    
    # Salary preferences
    expected_salary_min = Column(Integer, nullable=True)
    expected_salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), default="USD")
    
    # Experience
    experience_level = Column(String(50), nullable=True)
    
    # Skills to match
    desired_skills = Column(Text, nullable=True)
    
    # Notifications
    email_notifications = Column(Boolean, default=True)
    notification_frequency = Column(String(20), default="daily")  # daily, weekly
    
    # Raw filters
    filters = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<SearchPreferences for user {self.user_id}>"
