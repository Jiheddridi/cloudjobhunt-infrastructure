"""
CloudJobHunt Job Model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Job(Base):
    """Job model for storing job listings"""
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True, nullable=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), default="USD")
    job_type = Column(String(50), nullable=True)  # full-time, part-time, contract
    experience_level = Column(String(50), nullable=True)  # junior, mid, senior
    skills = Column(Text, nullable=True)  # JSON string of skills
    source = Column(String(50), nullable=True)  # linkedin, indeed, etc.
    url = Column(String(1000), nullable=True)
    is_remote = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_matches = relationship("JobMatch", back_populates="job")
    
    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"
