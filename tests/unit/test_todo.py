"""
Unit tests for the Todo model.
"""
import pytest
from src.models.todo import Todo


def test_todo_creation():
    """Test creating a Todo object with valid data."""
    todo = Todo(id=1, title="Test Todo", description="Test Description", completed=False)
    
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.completed is False


def test_todo_creation_defaults():
    """Test creating a Todo object with default values."""
    todo = Todo(id=1, title="Test Todo")
    
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == ""
    assert todo.completed is False


def test_todo_title_validation():
    """Test that Todo validates non-empty title."""
    with pytest.raises(ValueError):
        Todo(id=1, title="", description="Test Description")
    
    with pytest.raises(ValueError):
        Todo(id=1, title="   ", description="Test Description")


def test_todo_description_default():
    """Test that Todo handles None description by setting it to empty string."""
    todo = Todo(id=1, title="Test Todo", description=None)
    
    assert todo.description == ""