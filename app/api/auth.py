"""
CloudJobHunt Authentication API
"""
from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.config import settings
from app.database import get_db
from app.crud.user import authenticate_user, create_user, get_user_by_email, get_user_by_id
from app.schemas.user import UserCreate
from app.schemas.token import Token, TokenData, Message

router = APIRouter()

# OAuth2PasswordBearer with auto_error=False - won't throw 401 automatically
# This allows public endpoints to work even without tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login", auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)] = None,
    db: Session = Depends(get_db)
) -> TokenData:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # If no token provided, raise auth error
    if token is None:
        raise credentials_exception
        
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        # include email from payload to lookup user (login/register set email in token)
        email: str = payload.get("email")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id), email=email)
    except JWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception
    
    # Prefer lookup by id if available, fallback to email
    user = None
    if token_data.user_id:
        user = get_user_by_id(db, token_data.user_id)
    if not user and token_data.email:
        user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return token_data


def get_current_active_user(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TokenData:
    """Get current active user"""
    # In a real implementation, check if user is active
    return current_user


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Mode dev: pas de vérification de DB
    # Générer simplement un token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(hash(user_data.email) % 1000000), "email": user_data.email},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login and get access token"""
    # Mode dev: accepter toute combinaison email/password
    # Générer simplement un token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(hash(form_data.username) % 1000000), "email": form_data.username},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout")
async def logout(current_user: TokenData = Depends(get_current_active_user)):
    """Logout (client-side token removal)"""
    return Message(message="Successfully logged out")


@router.get("/me", response_model=TokenData)
async def get_me(current_user: TokenData = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
