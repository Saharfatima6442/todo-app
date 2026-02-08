"""
Main entry point for the Todo API server with authentication
"""
from src.api.todo_api import app
import uvicorn


def start_api():
    """Start the FastAPI server"""
    uvicorn.run("src.api.todo_api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start_api()