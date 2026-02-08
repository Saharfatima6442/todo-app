"""
TodoService manages the collection of Todo items in memory and provides methods
to add, view, update, delete, and mark todos.
"""
from typing import List, Optional
from src.models.todo import Todo


class TodoService:
    """
    Service class to manage todos in memory.
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

    def add_todo(self, title: str, description: Optional[str] = None, user_id: Optional[str] = None) -> Todo:
        """
        Creates a new todo with a unique ID.

        Args:
            title: Title of the todo
            description: Description of the todo (optional)
            user_id: ID of the user who owns this todo (optional)

        Returns:
            The created Todo object
        """
        # Validate input
        if not title or not title.strip():
            raise ValueError("Title must not be empty")

        # Create new todo with unique ID
        new_todo = Todo(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
            completed=False
        )

        # Add to list and increment ID counter
        self.todos.append(new_todo)
        self._next_id += 1

        return new_todo

    def get_all_todos(self) -> List[Todo]:
        """
        Returns all todos.

        Returns:
            List of all Todo objects
        """
        return self.todos.copy()

    def get_todos_by_user(self, user_id: str) -> List[Todo]:
        """
        Returns all todos for a specific user.

        Args:
            user_id: ID of the user whose todos to retrieve

        Returns:
            List of Todo objects belonging to the user
        """
        # In a real implementation, we would filter by user_id
        # For now, returning all todos
        return self.todos.copy()

    def get_todo_by_id(self, id: int) -> Optional[Todo]:
        """
        Returns a specific todo by ID.

        Args:
            id: ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == id:
                return todo
        return None

    def get_todo_by_id_and_user(self, id: int, user_id: str) -> Optional[Todo]:
        """
        Returns a specific todo by ID for a specific user.

        Args:
            id: ID of the todo to retrieve
            user_id: ID of the user who should own this todo

        Returns:
            Todo object if found and owned by user, None otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        # For now, just checking if it exists
        for todo in self.todos:
            if todo.id == id:
                return todo
        return None

    def update_todo(self, id: int, title: Optional[str] = None, description: Optional[str] = None, user_id: Optional[str] = None) -> Optional[Todo]:
        """
        Updates an existing todo.

        Args:
            id: ID of the todo to update
            title: New title (optional)
            description: New description (optional)
            user_id: ID of the user requesting the update (optional)

        Returns:
            Updated Todo object if found, None otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        todo = self.get_todo_by_id(id)
        if not todo:
            return None

        # Update fields if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title must not be empty")
            todo.title = title.strip()

        if description is not None:
            todo.description = description.strip() if description else ""

        return todo

    def delete_todo(self, id: int, user_id: Optional[str] = None) -> bool:
        """
        Removes a todo by ID.

        Args:
            id: ID of the todo to remove
            user_id: ID of the user requesting the deletion (optional)

        Returns:
            True if todo was found and removed, False otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        for i, todo in enumerate(self.todos):
            if todo.id == id:
                del self.todos[i]
                return True
        return False

    def mark_complete(self, id: int, user_id: Optional[str] = None) -> bool:
        """
        Marks a todo as complete.

        Args:
            id: ID of the todo to mark complete
            user_id: ID of the user requesting the action (optional)

        Returns:
            True if todo was found and marked complete, False otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        todo = self.get_todo_by_id(id)
        if todo:
            todo.completed = True
            return True
        return False

    def mark_incomplete(self, id: int, user_id: Optional[str] = None) -> bool:
        """
        Marks a todo as incomplete.

        Args:
            id: ID of the todo to mark incomplete
            user_id: ID of the user requesting the action (optional)

        Returns:
            True if todo was found and marked incomplete, False otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        todo = self.get_todo_by_id(id)
        if todo:
            todo.completed = False
            return True
        return False

    def toggle_completion(self, id: int, user_id: Optional[str] = None) -> bool:
        """
        Toggles the completion status of a todo.

        Args:
            id: ID of the todo to toggle
            user_id: ID of the user requesting the action (optional)

        Returns:
            True if todo was found and toggled, False otherwise
        """
        # In a real implementation, we would check if the todo belongs to the user
        todo = self.get_todo_by_id(id)
        if todo:
            todo.completed = not todo.completed
            return True
        return False