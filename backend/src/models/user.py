from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    email: Optional[str] = None
    authenticated: bool = False
    
    @classmethod
    def from_jwt_payload(cls, payload: dict):
        """Create a User instance from JWT payload"""
        return cls(
            id=payload.get("sub"),
            email=payload.get("email"),
            authenticated=True
        )