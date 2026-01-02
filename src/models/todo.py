"""
Todo model representing a task with an ID, title, description, and completion status.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    """
    Represents a task with an ID (unique identifier), title (string), 
    description (string), and completion status (boolean)
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the Todo object after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title must not be empty or null")
        if self.description is None:
            self.description = ""