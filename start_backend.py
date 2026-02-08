"""
Script to start the simplified Todo API backend server (stable baseline)
"""
from src.api.todo_api import app
import uvicorn
import sys
import os

def start_backend():
    """Start the FastAPI server"""
    print("Starting simplified Todo API server (stable baseline)...")
    print("Access the API at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")

    uvicorn.run(
        "src.api.todo_api:app",
        host="localhost",
        port=8000,
        reload=False,  # Set to False for production
        log_level="info"
    )

if __name__ == "__main__":
    start_backend()