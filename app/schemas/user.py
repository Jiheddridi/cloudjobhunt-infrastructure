"""
CloudJobHunt User Schemas (Pydantic)
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# User schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8)
    confirm_password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    """Schema for user in database"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Schema for user response"""
    pass


class UserInDB(UserInDBBase):
    """Schema for user with hashed password"""
    hashed_password: str


# CV schemas
class CVBase(BaseModel):
    """Base CV schema"""
    summary: Optional[str] = None
    skills: Optional[str] = None
    languages: Optional[str] = None
    years_of_experience: Optional[int] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    education: Optional[str] = None


class CVCreate(CVBase):
    """Schema for creating CV"""
    pass


class CVUpdate(CVBase):
    """Schema for updating CV"""
    pass


class CVInDBBase(CVBase):
    """Schema for CV in database"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CV(CVInDBBase):
    """Schema for CV response"""
    pass


# Search Preferences schemas
class SearchPreferencesBase(BaseModel):
    """Base search preferences schema"""
    job_titles: Optional[str] = None
    keywords: Optional[str] = None
    locations: Optional[str] = None
    remote_only: bool = False
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    experience_level: Optional[str] = None
    desired_skills: Optional[str] = None
    email_notifications: bool = True
    notification_frequency: str = "daily"


class SearchPreferencesCreate(SearchPreferencesBase):
    """Schema for creating search preferences"""
    pass


class SearchPreferencesUpdate(SearchPreferencesBase):
    """Schema for updating search preferences"""
    pass


class SearchPreferencesInDB(SearchPreferencesBase):
    """Schema for search preferences in database"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SearchPreferences(SearchPreferencesInDB):
    """Schema for search preferences response"""
    pass
