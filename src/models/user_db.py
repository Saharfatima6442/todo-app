from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class User(BaseModel):
    id: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    @classmethod
    def create_new(cls, email: str, password_hash: str):
        """Create a new user with a unique ID"""
        user_id = str(uuid.uuid4())
        now = datetime.now()
        return cls(
            id=user_id,
            email=email,
            password_hash=password_hash,
            created_at=now,
            updated_at=now,
            is_active=True
        )


class UserRegistration(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )