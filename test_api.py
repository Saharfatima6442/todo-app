"""
Test script to verify the Todo API is working correctly
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing Todo API...")
    print("="*50)
    
    # Test 1: Get all todos (should be empty initially)
    print("1. Testing GET /todos...")
    try:
        response = requests.get(f"{BASE_URL}/todos")
        if response.status_code == 200:
            todos = response.json()
            print(f"   ✓ Success: Got {len(todos)} todos")
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 2: Create a new todo
    print("2. Testing POST /todos...")
    try:
        new_todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo item"
        }
        response = requests.post(f"{BASE_URL}/todos", json=new_todo_data)
        if response.status_code == 200:
            created_todo = response.json()
            print(f"   ✓ Success: Created todo with ID {created_todo['id']}")
            todo_id = created_todo['id']
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Get the specific todo
    print("3. Testing GET /todos/{id}...")
    try:
        response = requests.get(f"{BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            todo = response.json()
            print(f"   ✓ Success: Retrieved todo '{todo['title']}'")
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 4: Update the todo
    print("4. Testing PUT /todos/{id}...")
    try:
        update_data = {
            "title": "Updated Test Todo",
            "description": "This todo has been updated"
        }
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
        if response.status_code == 200:
            updated_todo = response.json()
            print(f"   ✓ Success: Updated todo to '{updated_todo['title']}'")
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 5: Toggle completion
    print("5. Testing PATCH /todos/{id}/toggle...")
    try:
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            toggled_todo = response.json()
            print(f"   ✓ Success: Toggled completion status, now completed={toggled_todo['completed']}")
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 6: Delete the todo
    print("6. Testing DELETE /todos/{id}...")
    try:
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            print("   ✓ Success: Deleted todo")
        else:
            print(f"   ✗ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("="*50)
    print("✓ All API tests passed!")
    return True

if __name__ == "__main__":
    test_api()