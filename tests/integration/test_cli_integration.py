"""
Integration tests for the CLI and service layer.
"""
from src.services.todo_service import TodoService
from src.cli.main import TodoCLI
import io
import sys
from contextlib import redirect_stdout


def test_full_workflow():
    """Test the full workflow of adding, viewing, updating, and deleting a todo."""
    service = TodoService()
    
    # Add a todo
    todo = service.add_todo("Integration Test", "This is an integration test")
    assert len(service.get_all_todos()) == 1
    assert todo.title == "Integration Test"
    
    # Get the todo by ID
    retrieved = service.get_todo_by_id(todo.id)
    assert retrieved is not None
    assert retrieved.title == "Integration Test"
    
    # Update the todo
    updated = service.update_todo(todo.id, "Updated Integration Test", "Updated description")
    assert updated is not None
    assert updated.title == "Updated Integration Test"
    
    # Mark as complete
    result = service.mark_complete(todo.id)
    assert result is True
    assert service.get_todo_by_id(todo.id).completed is True
    
    # Toggle completion
    result = service.toggle_completion(todo.id)
    assert result is True
    assert service.get_todo_by_id(todo.id).completed is False
    
    # Delete the todo
    result = service.delete_todo(todo.id)
    assert result is True
    assert len(service.get_all_todos()) == 0


def test_cli_display_todos():
    """Test the CLI's display functionality."""
    service = TodoService()
    
    # Add a few todos
    service.add_todo("First Todo", "Description 1")
    service.add_todo("Second Todo", "Description 2")
    
    # Capture the output of view_todos
    cli = TodoCLI()
    cli.service = service  # Inject our service with todos
    
    f = io.StringIO()
    with redirect_stdout(f):
        cli.view_todos()
    
    output = f.getvalue()
    
    # Verify the output contains our todos
    assert "First Todo" in output
    assert "Second Todo" in output
    assert "Description 1" in output
    assert "Description 2" in output