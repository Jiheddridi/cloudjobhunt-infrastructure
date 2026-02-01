"""
CloudJobHunt Job Schemas (Pydantic)
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Job schemas
class JobBase(BaseModel):
    """Base job schema"""
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a job"""
    external_id: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    skills: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    is_remote: bool = False
    posted_at: Optional[datetime] = None


class JobUpdate(BaseModel):
    """Schema for updating a job"""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    is_active: Optional[bool] = None


class JobInDBBase(JobBase):
    """Schema for job in database"""
    id: int
    external_id: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    skills: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    is_remote: bool
    posted_at: Optional[datetime] = None
    scraped_at: datetime
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Job(JobInDBBase):
    """Schema for job response"""
    pass


class JobListResponse(BaseModel):
    """Schema for job list response"""
    jobs: List[Job]
    total: int
    page: int
    page_size: int
    total_pages: int


# Job Match schemas
class JobMatchBase(BaseModel):
    """Base job match schema"""
    job_id: int
    match_score: Optional[float] = None
    matched_skills: Optional[str] = None
    missing_skills: Optional[str] = None
    match_explanation: Optional[str] = None


class JobMatchCreate(JobMatchBase):
    """Schema for creating job match"""
    pass


class JobMatchUpdate(BaseModel):
    """Schema for updating job match"""
    status: Optional[str] = None
    is_favorite: Optional[bool] = None
    is_hidden: Optional[bool] = None


class JobMatchInDB(JobMatchBase):
    """Schema for job match in database"""
    id: int
    user_id: int
    status: str
    is_favorite: bool
    is_hidden: bool
    matched_at: datetime
    viewed_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobMatch(JobMatchInDB):
    """Schema for job match response"""
    job: Optional[Job] = None


class JobMatchListResponse(BaseModel):
    """Schema for job match list response"""
    matches: List[JobMatch]
    total: int
