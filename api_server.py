"""
Main entry point for the Todo API server
"""
from src.api.todo_api import app
import uvicorn


def start_api():
    """Start the FastAPI server"""
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start_api()