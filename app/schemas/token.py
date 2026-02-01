"""
CloudJobHunt Token Schemas (Pydantic)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    expires: Optional[datetime] = None


class TokenPayload(BaseModel):
    """Token payload schema for JWT"""
    sub: str  # Subject (user ID or email)
    email: Optional[str] = None
    exp: Optional[datetime] = None


class Message(BaseModel):
    """Generic message schema"""
    message: str


class LoginRequest(BaseModel):
    """Login request schema"""
    email: str
    password: str
