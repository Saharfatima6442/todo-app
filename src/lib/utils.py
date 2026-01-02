"""
Utility functions for the todo application.
"""
from typing import Any


def validate_todo_data(title: str, description: str = None) -> bool:
    """
    Validate todo data before creating or updating.
    
    Args:
        title: Title of the todo
        description: Description of the todo
        
    Returns:
        True if data is valid, raises ValueError otherwise
    """
    if not title or not title.strip():
        raise ValueError("Title must not be empty")
    
    if description is not None and not isinstance(description, str):
        raise ValueError("Description must be a string")
    
    return True