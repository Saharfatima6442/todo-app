from fastapi import Depends, HTTPException, status
from typing import Dict
from src.middleware.jwt_auth import jwt_bearer_auth
from src.models.user import User

async def get_current_user(jwt_payload: Dict = Depends(jwt_bearer_auth)) -> User:
    """
    Get the current authenticated user from the JWT payload
    """
    if not jwt_payload or not jwt_payload.get("id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create a User instance from the JWT payload
    user = User.from_jwt_payload(jwt_payload)
    
    # Verify that the user is properly authenticated
    if not user.authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user