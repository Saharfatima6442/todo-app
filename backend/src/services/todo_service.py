"""
TodoService manages the collection of Todo items in memory and provides methods
to add, view, update, delete, and mark todos.
This simplified version works without authentication for the stable baseline.
"""
from typing import List, Optional
from src.models.todo import Todo, TodoCreate, TodoUpdate


class TodoService:
    """
    Service class to manage todos in memory without authentication.
    Responsibilities:
    - Manage the collection of Todo items in memory
    - Provide methods to add, view, update, delete, and mark todos
    - Ensure unique IDs are assigned to each todo
    - Validate todo data before operations
    """

    def __init__(self):
        """Initialize the service with an empty list of todos and ID counter."""
        self.todos: List[Todo] = []
        self._next_id = 1

    def create_todo(self, todo_create: TodoCreate, owner_id: str = "default_user") -> Todo:
        """Create a new todo without authentication"""
        # Validate the input
        if len(todo_create.title) < 1 or len(todo_create.title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")

        if todo_create.description and len(todo_create.description) > 500:
            raise ValueError("Description must be at most 500 characters")

        # Create the todo data with a default owner ID
        todo_data = Todo(
            id=self._next_id,
            title=todo_create.title,
            description=todo_create.description,
            completed=todo_create.completed if todo_create.completed is not None else False,
            owner_id=owner_id
        )

        # Add to list and increment ID counter
        self.todos.append(todo_data)
        self._next_id += 1

        return todo_data

    def get_todo_by_id(self, todo_id: str, owner_id: str = "default_user") -> Optional[Todo]:
        """Get a specific todo by ID without authentication"""
        # Convert string ID to integer for comparison
        try:
            int_id = int(todo_id)
        except ValueError:
            return None
            
        for todo in self.todos:
            if todo.id == int_id:
                return todo
        return None

    def get_todos_by_owner(self, owner_id: str = "default_user") -> List[Todo]:
        """Get all todos without authentication"""
        # Return all todos since there's no authentication
        return self.todos.copy()

    def update_todo(self, todo_id: str, owner_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update a todo without authentication"""
        # Convert string ID to integer for comparison
        try:
            int_id = int(todo_id)
        except ValueError:
            return None
            
        for i, todo in enumerate(self.todos):
            if todo.id == int_id:
                # Prepare update data
                if todo_update.title is not None:
                    if len(todo_update.title) < 1 or len(todo_update.title) > 100:
                        raise ValueError("Title must be between 1 and 100 characters")
                    todo.title = todo_update.title

                if todo_update.description is not None:
                    if len(todo_update.description) > 500:
                        raise ValueError("Description must be at most 500 characters")
                    todo.description = todo_update.description

                if todo_update.completed is not None:
                    todo.completed = todo_update.completed

                # Update the todo in the list
                self.todos[i] = todo
                return todo
        return None

    def delete_todo(self, todo_id: str, owner_id: str = "default_user") -> bool:
        """Delete a todo without authentication"""
        # Convert string ID to integer for comparison
        try:
            int_id = int(todo_id)
        except ValueError:
            return False
            
        for i, todo in enumerate(self.todos):
            if todo.id == int_id:
                del self.todos[i]
                return True
        return False

    def get_all_todos(self) -> List[Todo]:
        """Get all todos without authentication"""
        return self.todos.copy()

# Global instance
todo_service = TodoService()