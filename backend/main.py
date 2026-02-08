"""
Main entry point for the simplified Todo backend (stable baseline)
"""
from fastapi import FastAPI
# DISABLED: Chatbot modules - commented out for stable baseline
# from .chat.router import router as chat_router
# from .chat.conversations_router import router as conversations_router
from .database.session import engine
from .models.conversation import Conversation
from .models.message import Message
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database tables
    from sqlmodel import SQLModel
    # DISABLED: Only initialize basic todo tables for stable baseline
    # SQLModel.metadata.create_all(bind=engine)
    yield


# Create the FastAPI app
app = FastAPI(
    title="Todo API (Stable Baseline)",
    description="Basic todo CRUD operations without chatbot or authentication",
    version="1.0.0",
    lifespan=lifespan
)


# DISABLED: Chatbot routers - commented out for stable baseline
# Include the routers
# app.include_router(chat_router)
# app.include_router(conversations_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the simplified Todo API (Stable Baseline)!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Todo API (Stable Baseline)"}


# Basic todo endpoints for stable baseline
from .src.models.todo import Todo
from .src.services.todo_service import todo_service
from fastapi import HTTPException


@app.get("/todos")
async def get_todos():
    """Get all todos"""
    return todo_service.get_all_todos()


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos")
async def create_todo(todo: Todo):
    """Create a new todo"""
    created_todo = todo_service.create_todo(todo, "default_user")
    return created_todo


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    """Update an existing todo"""
    updated_todo = todo_service.update_todo(str(todo_id), "default_user", todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo by ID"""
    success = todo_service.delete_todo(str(todo_id), "default_user")
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}