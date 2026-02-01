"""
CloudJobHunt Users API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_users,
    update_user,
    delete_user,
    get_password_hash,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User
from app.api.auth import get_current_active_user, TokenData

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get all users (admin only in production)"""
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
async def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get current user information"""
    user = get_user_by_id(db, current_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get a specific user by ID"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Update current user profile"""
    user = get_user_by_id(db, current_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=User)
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Update a specific user (admin only)"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Delete a user (admin only)"""
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
