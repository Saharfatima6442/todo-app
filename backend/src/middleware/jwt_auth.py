from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from src.utils.jwt_handler import verify_token

security = HTTPBearer()

async def jwt_bearer_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    JWT Bearer token authentication dependency
    """
    token = credentials.credentials
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return user info from the token
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "exp": payload.get("exp")
    }