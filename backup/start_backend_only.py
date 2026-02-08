import subprocess
import sys
import os
import time

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting Todo API backend server...")
    print("Access the API at: http://127.0.0.1:8000")
    print("API documentation available at: http://127.0.0.1:8000/docs")
    
    # Change to the project directory
    os.chdir("C:\\Users\\Saeed\\OneDrive\\Desktop\\todo-app")
    
    try:
        # Run the backend server using the proper uvicorn command
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.todo_api:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except subprocess.CalledProcessError as e:
        print(f"Error starting backend: {e}")

if __name__ == "__main__":
    start_backend()