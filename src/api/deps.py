from fastapi import Depends, HTTPException, status
from typing import Dict
from src.middleware.jwt_auth import jwt_bearer_auth
from src.models.user_db import UserResponse
from src.services.user_service import UserService

async def get_current_user(jwt_payload: Dict = Depends(jwt_bearer_auth)) -> UserResponse:
    """
    Get the current authenticated user from the JWT payload
    """
    if not jwt_payload or not jwt_payload.get("sub"):  # Changed from "id" to "sub" to match JWT standard
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the user from the user service
    user_service = UserService()
    user = user_service.get_user_by_id(jwt_payload.get("sub"))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return a UserResponse instance
    return UserResponse.from_user(user)