from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    title: str
    description: Optional[str] = None
    
    # Validation for title length
    def __init__(self, **data):
        super().__init__(**data)
        if len(self.title) < 1 or len(self.title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        
        if self.description and len(self.description) > 500:
            raise ValueError("Description must be at most 500 characters")

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: str
    owner_id: str
    created_at: Optional[datetime] = None
    
    # Validation for title length
    def __init__(self, **data):
        super().__init__(**data)
        if hasattr(self, 'title') and self.title:
            if len(self.title) < 1 or len(self.title) > 100:
                raise ValueError("Title must be between 1 and 100 characters")
            
            if self.description and len(self.description) > 500:
                raise ValueError("Description must be at most 500 characters")