import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app  # Assuming the FastAPI app is in main.py


@pytest.fixture
def client():
    """Create a test client for the API"""
    return TestClient(app)


def test_add_todo_success(client):
    """Test successfully adding a new todo"""
    # Mock JWT validation to simulate an authenticated user
    mock_user_data = {"sub": "user123", "email": "user@example.com"}
    
    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.post(
            "/api/user123/todos",
            json={"title": "Test Todo", "description": "Test Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["completed"] is False
        assert data["owner_id"] == "user123"


def test_add_todo_missing_title(client):
    """Test adding a todo without a title (should fail validation)"""
    mock_user_data = {"sub": "user123", "email": "user@example.com"}
    
    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.post(
            "/api/user123/todos",
            json={"description": "Test Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert response.status_code == 400


def test_add_todo_invalid_title_length(client):
    """Test adding a todo with title that's too long or too short"""
    mock_user_data = {"sub": "user123", "email": "user@example.com"}
    
    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        # Test with title too short (empty)
        response = client.post(
            "/api/user123/todos",
            json={"title": "", "description": "Test Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert response.status_code == 400
        
        # Test with title too long
        long_title = "a" * 101  # More than 100 characters
        response = client.post(
            "/api/user123/todos",
            json={"title": long_title, "description": "Test Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert response.status_code == 400


def test_add_todo_unauthorized(client):
    """Test adding a todo without valid authentication"""
    response = client.post(
        "/api/user123/todos",
        json={"title": "Test Todo", "description": "Test Description"}
        # No Authorization header
    )
    
    assert response.status_code == 401


def test_add_todo_mismatched_user_id(client):
    """Test adding a todo with mismatched user ID in URL vs JWT"""
    # JWT has user456 but URL has user123
    mock_user_data = {"sub": "user456", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.post(
            "/api/user123/todos",
            json={"title": "Test Todo", "description": "Test Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 403  # Forbidden due to user ID mismatch


def test_update_todo_success(client):
    """Test successfully updating an existing todo"""
    # First, add a todo to update
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        # Create a todo first
        create_response = client.post(
            "/api/user123/todos",
            json={"title": "Original Title", "description": "Original Description"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert create_response.status_code == 201
        created_todo = create_response.json()
        todo_id = created_todo["id"]

        # Now update the todo
        update_response = client.put(
            f"/api/user123/todos/{todo_id}",
            json={
                "title": "Updated Title",
                "description": "Updated Description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["title"] == "Updated Title"
        assert updated_todo["description"] == "Updated Description"
        assert updated_todo["completed"] is True


def test_update_todo_not_found(client):
    """Test updating a non-existent todo"""
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.put(
            "/api/user123/todos/nonexistent-id",
            json={
                "title": "Updated Title",
                "description": "Updated Description"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404


def test_update_todo_unauthorized(client):
    """Test updating a todo without valid authentication"""
    response = client.put(
        "/api/user123/todos/some-id",
        json={
            "title": "Updated Title",
            "description": "Updated Description"
        }
        # No Authorization header
    )

    assert response.status_code == 401


def test_update_todo_mismatched_user_id(client):
    """Test updating a todo with mismatched user ID in URL vs JWT"""
    mock_user_data = {"sub": "user456", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.put(
            "/api/user123/todos/some-id",
            json={
                "title": "Updated Title",
                "description": "Updated Description"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 403  # Forbidden due to user ID mismatch


def test_delete_todo_success(client):
    """Test successfully deleting an existing todo"""
    # First, add a todo to delete
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        # Create a todo first
        create_response = client.post(
            "/api/user123/todos",
            json={"title": "Title to Delete", "description": "Description to Delete"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert create_response.status_code == 201
        created_todo = create_response.json()
        todo_id = created_todo["id"]

        # Now delete the todo
        delete_response = client.delete(
            f"/api/user123/todos/{todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Todo deleted successfully"


def test_delete_todo_not_found(client):
    """Test deleting a non-existent todo"""
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.delete(
            "/api/user123/todos/nonexistent-id",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404


def test_delete_todo_unauthorized(client):
    """Test deleting a todo without valid authentication"""
    response = client.delete(
        "/api/user123/todos/some-id"
        # No Authorization header
    )

    assert response.status_code == 401


def test_delete_todo_mismatched_user_id(client):
    """Test deleting a todo with mismatched user ID in URL vs JWT"""
    mock_user_data = {"sub": "user456", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.delete(
            "/api/user123/todos/some-id",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 403  # Forbidden due to user ID mismatch


def test_toggle_todo_completion_success(client):
    """Test successfully toggling the completion status of an existing todo"""
    # First, add a todo to toggle
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        # Create a todo first
        create_response = client.post(
            "/api/user123/todos",
            json={"title": "Title to Toggle", "description": "Description to Toggle"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert create_response.status_code == 201
        created_todo = create_response.json()
        todo_id = created_todo["id"]
        assert created_todo["completed"] is False  # Initially not completed

        # Now toggle the completion status
        toggle_response = client.patch(
            f"/api/user123/todos/{todo_id}/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert toggle_response.status_code == 200
        toggled_todo = toggle_response.json()
        assert toggled_todo["id"] == todo_id
        assert toggled_todo["completed"] is True  # Should now be completed


def test_toggle_todo_completion_twice(client):
    """Test toggling the completion status twice returns to original state"""
    # First, add a todo to toggle
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        # Create a todo first
        create_response = client.post(
            "/api/user123/todos",
            json={"title": "Title to Toggle Twice", "description": "Description to Toggle Twice"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert create_response.status_code == 201
        created_todo = create_response.json()
        todo_id = created_todo["id"]
        assert created_todo["completed"] is False  # Initially not completed

        # Toggle the completion status first time
        toggle_response_1 = client.patch(
            f"/api/user123/todos/{todo_id}/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert toggle_response_1.status_code == 200
        assert toggle_response_1.json()["completed"] is True  # Should now be completed

        # Toggle the completion status second time
        toggle_response_2 = client.patch(
            f"/api/user123/todos/{todo_id}/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert toggle_response_2.status_code == 200
        assert toggle_response_2.json()["completed"] is False  # Should now be incomplete again


def test_toggle_todo_not_found(client):
    """Test toggling completion status of a non-existent todo"""
    mock_user_data = {"sub": "user123", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.patch(
            "/api/user123/todos/nonexistent-id/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404


def test_toggle_todo_unauthorized(client):
    """Test toggling completion status without valid authentication"""
    response = client.patch(
        "/api/user123/todos/some-id/toggle-completion"
        # No Authorization header
    )

    assert response.status_code == 401


def test_toggle_todo_mismatched_user_id(client):
    """Test toggling completion status with mismatched user ID in URL vs JWT"""
    mock_user_data = {"sub": "user456", "email": "user@example.com"}

    with patch('backend.src.middleware.jwt_auth.verify_jwt_token', return_value=mock_user_data):
        response = client.patch(
            "/api/user123/todos/some-id/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 403  # Forbidden due to user ID mismatch


if __name__ == "__main__":
    pytest.main()