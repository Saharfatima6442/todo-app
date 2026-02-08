"""
Integration tests for the JWT authenticated todo application.
Tests the complete user journey across multiple API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from main import app  # Assuming the FastAPI app is in main.py


@pytest.fixture
def client():
    """Create a test client for the API"""
    return TestClient(app)


def test_complete_user_journey(client):
    """
    Test the complete user journey: create, read, update, toggle completion, delete a todo
    """
    # Mock JWT validation to simulate an authenticated user
    mock_user_data = {"sub": "user123", "email": "user@example.com"}
    
    with patch('backend.src.middleware.jwt_auth.verify_token', return_value=mock_user_data):
        # Step 1: Create a new todo
        create_response = client.post(
            "/api/user123/todos",
            json={"title": "Integration Test Todo", "description": "This is for integration testing"},
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert create_response.status_code == 201
        created_todo = create_response.json()
        assert created_todo["title"] == "Integration Test Todo"
        assert created_todo["description"] == "This is for integration testing"
        assert created_todo["completed"] is False
        assert "id" in created_todo
        todo_id = created_todo["id"]
        
        # Step 2: Get the newly created todo
        get_response = client.get(
            f"/api/user123/todos/{todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert get_response.status_code == 200
        retrieved_todo = get_response.json()
        assert retrieved_todo["id"] == todo_id
        assert retrieved_todo["title"] == "Integration Test Todo"
        
        # Step 3: Get all todos for the user (should include the new one)
        list_response = client.get(
            "/api/user123/todos",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert list_response.status_code == 200
        todos_list = list_response.json()
        assert len(todos_list) == 1
        assert todos_list[0]["id"] == todo_id
        
        # Step 4: Update the todo
        update_response = client.put(
            f"/api/user123/todos/{todo_id}",
            json={
                "title": "Updated Integration Test Todo",
                "description": "Updated description for integration testing",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == "Updated Integration Test Todo"
        assert updated_todo["description"] == "Updated description for integration testing"
        
        # Step 5: Toggle the completion status
        toggle_response = client.patch(
            f"/api/user123/todos/{todo_id}/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert toggle_response.status_code == 200
        toggled_todo = toggle_response.json()
        assert toggled_todo["id"] == todo_id
        assert toggled_todo["completed"] is True  # Should now be completed
        
        # Step 6: Toggle again to make sure it goes back to incomplete
        toggle_response_2 = client.patch(
            f"/api/user123/todos/{todo_id}/toggle-completion",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert toggle_response_2.status_code == 200
        toggled_todo_2 = toggle_response_2.json()
        assert toggled_todo_2["id"] == todo_id
        assert toggled_todo_2["completed"] is False  # Should now be incomplete again
        
        # Step 7: Delete the todo
        delete_response = client.delete(
            f"/api/user123/todos/{todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Todo deleted successfully"
        
        # Step 8: Verify the todo is gone
        get_deleted_response = client.get(
            f"/api/user123/todos/{todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        
        assert get_deleted_response.status_code == 404


def test_multiple_users_isolation(client):
    """
    Test that users can only access their own todos
    """
    # Mock JWT validation for user1
    mock_user1_data = {"sub": "user1", "email": "user1@example.com"}
    # Mock JWT validation for user2
    mock_user2_data = {"sub": "user2", "email": "user2@example.com"}
    
    with patch('backend.src.middleware.jwt_auth.verify_token', return_value=mock_user1_data):
        # User1 creates a todo
        create_response = client.post(
            "/api/user1/todos",
            json={"title": "User1's Todo", "description": "This belongs to user1"},
            headers={"Authorization": "Bearer fake-jwt-token-for-user1"}
        )
        
        assert create_response.status_code == 201
        user1_todo = create_response.json()
        user1_todo_id = user1_todo["id"]
        
        # User1 should be able to access their own todo
        get_response = client.get(
            f"/api/user1/todos/{user1_todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token-for-user1"}
        )
        
        assert get_response.status_code == 200
    
    with patch('backend.src.middleware.jwt_auth.verify_token', return_value=mock_user2_data):
        # User2 should NOT be able to access user1's todo
        unauthorized_get_response = client.get(
            f"/api/user2/todos/{user1_todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token-for-user2"}
        )
        
        # This should fail because the todo doesn't belong to user2
        # Even though the URL says user2, the todo belongs to user1, so access should be denied
        assert unauthorized_get_response.status_code == 404  # or 403 depending on implementation
    
    # Clean up: delete user1's todo
    with patch('backend.src.middleware.jwt_auth.verify_token', return_value=mock_user1_data):
        delete_response = client.delete(
            f"/api/user1/todos/{user1_todo_id}",
            headers={"Authorization": "Bearer fake-jwt-token-for-user1"}
        )
        
        assert delete_response.status_code == 200


if __name__ == "__main__":
    pytest.main()