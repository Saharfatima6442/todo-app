from typing import Dict, List, Optional
from src.models.todo import Todo
import uuid
from datetime import datetime

class InMemoryStorageService:
    def __init__(self):
        self.todos: Dict[str, Todo] = {}
    
    def create_todo(self, todo_data: Todo) -> Todo:
        """Create a new todo item"""
        # Generate a unique ID
        todo_id = str(uuid.uuid4())
        
        # Create the todo with the generated ID
        todo = Todo(
            id=todo_id,
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            owner_id=todo_data.owner_id,
            created_at=datetime.now()
        )
        
        # Store the todo
        self.todos[todo_id] = todo
        
        return todo
    
    def get_todo_by_id(self, todo_id: str, owner_id: str) -> Optional[Todo]:
        """Get a todo by ID for a specific owner"""
        todo = self.todos.get(todo_id)
        if todo and todo.owner_id == owner_id:
            return todo
        return None
    
    def get_todos_by_owner(self, owner_id: str) -> List[Todo]:
        """Get all todos for a specific owner"""
        return [todo for todo in self.todos.values() if todo.owner_id == owner_id]
    
    def update_todo(self, todo_id: str, owner_id: str, update_data: dict) -> Optional[Todo]:
        """Update a todo if it belongs to the owner"""
        todo = self.get_todo_by_id(todo_id, owner_id)
        if not todo:
            return None
        
        # Update the todo with new values
        for field, value in update_data.items():
            if hasattr(todo, field) and value is not None:
                setattr(todo, field, value)
        
        # Update the stored todo
        self.todos[todo_id] = todo
        return todo
    
    def delete_todo(self, todo_id: str, owner_id: str) -> bool:
        """Delete a todo if it belongs to the owner"""
        todo = self.get_todo_by_id(todo_id, owner_id)
        if not todo:
            return False
        
        # Remove the todo
        del self.todos[todo_id]
        return True

# Global instance
storage_service = InMemoryStorageService()