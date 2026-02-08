"""
Simple test to verify the backend API is working
"""
import requests
import time
import subprocess
import sys

def test_backend():
    """Test if the backend API is responding"""
    try:
        # Wait a bit for the server to start if it's just been launched
        time.sleep(2)
        
        # Test the root endpoint
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✓ Backend API is running and responding")
            data = response.json()
            print(f"Response: {data}")
            return True
        else:
            print(f"✗ Backend API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend API. Is it running on http://127.0.0.1:8000?")
        return False
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False

def test_todos_endpoint():
    """Test the todos endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8000/todos")
        if response.status_code == 200:
            todos = response.json()
            print(f"✓ Todos endpoint working. Found {len(todos)} todos")
            return True
        else:
            print(f"✗ Todos endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing todos endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Testing Todo App Backend...")
    print("="*40)
    
    if test_backend():
        test_todos_endpoint()
        print("\n✓ Backend tests passed!")
    else:
        print("\n✗ Backend tests failed. Please ensure the backend server is running.")
        print("Run: python start_backend.py")