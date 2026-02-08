"""
Authentication middleware using Better Auth
"""
from fastapi import HTTPException, Request, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt
from typing import Dict, Optional


security = HTTPBearer()


def verify_token(token: str) -> Optional[Dict[str, any]]:
    """
    Verify the authentication token and return user info
    """
    try:
        # In a real implementation, we would use Better Auth's verification method
        # For now, we'll simulate the verification
        secret = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
        
        # Decode the JWT token
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, any]:
    """
    Get the current user from the authentication token
    """
    token = credentials.credentials
    user_info = verify_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_info


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the user owns the resource they're trying to access
    """
    return user_id == resource_user_id