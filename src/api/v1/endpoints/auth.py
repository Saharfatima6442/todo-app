from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import Dict
from src.models.user_db import UserRegistration, UserLogin, UserResponse
from src.services.user_service import UserService
from src.utils.jwt_handler import create_access_token
from datetime import timedelta
import re

router = APIRouter()

# Global instance of UserService
user_service = UserService()

# Define security for endpoints that require authentication
security = HTTPBearer()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegistration):
    """Register a new user."""
    # Validate email format
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Check password length
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    # Try to register the user
    user = user_service.register_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    return UserResponse.from_user(user)


@router.post("/login")
def login(user_data: UserLogin):
    """Authenticate user and return JWT token."""
    # Authenticate the user
    user = user_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token_expires = timedelta(days=30)  # Token valid for 30 days
    token_data = {
        "sub": user.id,
        "email": user.email
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_user(user)
    }


from src.api.deps import get_current_user

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get current authenticated user info."""
    return current_user