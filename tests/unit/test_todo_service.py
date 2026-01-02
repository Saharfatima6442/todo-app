"""
Unit tests for the TodoService.
"""
import pytest
from src.services.todo_service import TodoService


def test_add_todo():
    """Test adding a new todo."""
    service = TodoService()
    
    # Add a new todo
    todo = service.add_todo("Test Title", "Test Description")
    
    # Verify the todo was added
    assert len(service.todos) == 1
    assert todo.id == 1
    assert todo.title == "Test Title"
    assert todo.description == "Test Description"
    assert todo.completed is False


def test_add_todo_without_description():
    """Test adding a new todo without description."""
    service = TodoService()
    
    # Add a new todo without description
    todo = service.add_todo("Test Title")
    
    # Verify the todo was added with empty description
    assert len(service.todos) == 1
    assert todo.id == 1
    assert todo.title == "Test Title"
    assert todo.description == ""
    assert todo.completed is False


def test_add_todo_title_validation():
    """Test that adding a todo validates the title."""
    service = TodoService()
    
    with pytest.raises(ValueError):
        service.add_todo("")
    
    with pytest.raises(ValueError):
        service.add_todo("   ")


def test_get_all_todos():
    """Test getting all todos."""
    service = TodoService()
    
    # Add some todos
    service.add_todo("Title 1", "Description 1")
    service.add_todo("Title 2", "Description 2")
    
    # Get all todos
    todos = service.get_all_todos()
    
    # Verify all todos are returned
    assert len(todos) == 2
    assert todos[0].title == "Title 1"
    assert todos[1].title == "Title 2"


def test_get_todo_by_id():
    """Test getting a todo by ID."""
    service = TodoService()
    
    # Add a todo
    added_todo = service.add_todo("Test Title", "Test Description")
    
    # Get the todo by ID
    retrieved_todo = service.get_todo_by_id(added_todo.id)
    
    # Verify the todo is retrieved correctly
    assert retrieved_todo is not None
    assert retrieved_todo.id == added_todo.id
    assert retrieved_todo.title == "Test Title"


def test_get_todo_by_id_not_found():
    """Test getting a todo by ID that doesn't exist."""
    service = TodoService()
    
    # Try to get a todo with a non-existent ID
    retrieved_todo = service.get_todo_by_id(999)
    
    # Verify None is returned
    assert retrieved_todo is None


def test_update_todo():
    """Test updating a todo."""
    service = TodoService()
    
    # Add a todo
    original_todo = service.add_todo("Original Title", "Original Description")
    
    # Update the todo
    updated_todo = service.update_todo(original_todo.id, "Updated Title", "Updated Description")
    
    # Verify the todo was updated
    assert updated_todo is not None
    assert updated_todo.id == original_todo.id
    assert updated_todo.title == "Updated Title"
    assert updated_todo.description == "Updated Description"


def test_update_todo_partial():
    """Test updating only title or description of a todo."""
    service = TodoService()
    
    # Add a todo
    original_todo = service.add_todo("Original Title", "Original Description")
    
    # Update only the title
    updated_todo = service.update_todo(original_todo.id, title="Updated Title")
    
    # Verify only the title was updated
    assert updated_todo is not None
    assert updated_todo.id == original_todo.id
    assert updated_todo.title == "Updated Title"
    assert updated_todo.description == "Original Description"


def test_update_todo_not_found():
    """Test updating a todo that doesn't exist."""
    service = TodoService()
    
    # Try to update a todo with a non-existent ID
    result = service.update_todo(999, "New Title", "New Description")
    
    # Verify None is returned
    assert result is None


def test_update_todo_title_validation():
    """Test that updating a todo validates the title."""
    service = TodoService()
    
    # Add a todo
    original_todo = service.add_todo("Original Title", "Original Description")
    
    # Try to update with an empty title
    with pytest.raises(ValueError):
        service.update_todo(original_todo.id, title="")


def test_delete_todo():
    """Test deleting a todo."""
    service = TodoService()
    
    # Add a todo
    added_todo = service.add_todo("Test Title", "Test Description")
    
    # Delete the todo
    result = service.delete_todo(added_todo.id)
    
    # Verify the todo was deleted
    assert result is True
    assert len(service.todos) == 0


def test_delete_todo_not_found():
    """Test deleting a todo that doesn't exist."""
    service = TodoService()
    
    # Try to delete a todo with a non-existent ID
    result = service.delete_todo(999)
    
    # Verify False is returned
    assert result is False


def test_mark_complete():
    """Test marking a todo as complete."""
    service = TodoService()
    
    # Add a todo
    added_todo = service.add_todo("Test Title", "Test Description")
    
    # Verify initial state
    assert added_todo.completed is False
    
    # Mark as complete
    result = service.mark_complete(added_todo.id)
    
    # Verify the todo was marked complete
    assert result is True
    assert service.get_todo_by_id(added_todo.id).completed is True


def test_mark_incomplete():
    """Test marking a todo as incomplete."""
    service = TodoService()
    
    # Add a todo and mark it as complete
    added_todo = service.add_todo("Test Title", "Test Description")
    service.mark_complete(added_todo.id)
    
    # Verify it's complete
    assert service.get_todo_by_id(added_todo.id).completed is True
    
    # Mark as incomplete
    result = service.mark_incomplete(added_todo.id)
    
    # Verify the todo was marked incomplete
    assert result is True
    assert service.get_todo_by_id(added_todo.id).completed is False


def test_toggle_completion():
    """Test toggling a todo's completion status."""
    service = TodoService()
    
    # Add a todo
    added_todo = service.add_todo("Test Title", "Test Description")
    
    # Verify initial state (incomplete)
    assert added_todo.completed is False
    
    # Toggle to complete
    result = service.toggle_completion(added_todo.id)
    assert result is True
    assert service.get_todo_by_id(added_todo.id).completed is True
    
    # Toggle back to incomplete
    result = service.toggle_completion(added_todo.id)
    assert result is True
    assert service.get_todo_by_id(added_todo.id).completed is False