"""
Script to start both the simplified backend and frontend servers for the Todo app (stable baseline)
"""
import subprocess
import os
import sys
import time
import threading
from pathlib import Path

def start_backend():
    """Start the simplified FastAPI backend server"""
    print("Starting simplified Todo API backend server (stable baseline)...")
    print("Access the API at: http://127.0.0.1:8000")
    print("API documentation available at: http://127.0.0.1:8000/docs")

    try:
        # Run the simplified backend server
        result = subprocess.run([
            sys.executable, "-c",
            "from src.api.todo_api import app; import uvicorn; "
            "uvicorn.run('src.api.todo_api:app', host='127.0.0.1', port=8000, reload=False)"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting backend: {e}")

def start_frontend():
    """Start the Next.js frontend development server"""
    frontend_dir = Path(__file__).parent / "frontend"

    if not frontend_dir.exists():
        print("Error: Frontend directory not found!")
        return

    print("Starting Next.js frontend server...")
    print("Access the Todo App at: http://localhost:3000")

    # Set environment variable for the API base URL
    env = os.environ.copy()
    env["NEXT_PUBLIC_API_BASE_URL"] = "http://127.0.0.1:8000"

    try:
        # Change to frontend directory and run the dev server
        os.chdir(frontend_dir)
        result = subprocess.run(["npx", "next", "dev"], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting frontend: {e}")

def main():
    print("Starting Todo App (Stable Baseline) - Backend and Frontend")
    print("="*60)
    print("This version disables chatbot, MCP integrations, and authentication")
    print("Only basic todo CRUD operations are enabled")
    print("="*60)

    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Give the backend a moment to start
    time.sleep(3)

    # Start frontend in the main thread
    start_frontend()

if __name__ == "__main__":
    main()