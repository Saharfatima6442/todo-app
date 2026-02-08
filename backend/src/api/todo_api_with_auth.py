"""
REST API for the todo application using FastAPI with authentication
"""
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from src.models.todo import Todo
from src.services.todo_service import TodoService
from src.models.user_db import UserResponse
from src.api.deps import get_current_user
from fastapi.middleware.cors import CORSMiddleware


# Create a global instance of TodoService to maintain state across requests
# In a real application, you would use dependency injection or a database
todo_service = TodoService()

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"message": "Todo API with Authentication"}


# Include the auth router
from src.api.v1.endpoints.auth import router as auth_router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


# Authenticated endpoints for todos
@app.get("/todos", response_model=List[Todo])
def get_todos(current_user: UserResponse = Depends(get_current_user)):
    """Get all todos for the authenticated user"""
    # In a real implementation, we would filter todos by user ID
    # For now, returning all todos but this would be filtered by user
    return todo_service.get_all_todos()


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, current_user: UserResponse = Depends(get_current_user)):
    """Get a specific todo by ID for the authenticated user"""
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    # In a real implementation, we would check if the todo belongs to the user
    return todo


from pydantic import BaseModel

class TodoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

@app.post("/todos", response_model=Todo)
def create_todo(
    title: str = Query(...),
    description: Optional[str] = Query(None),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        new_todo = todo_service.add_todo(
            title=title,
            description=description
        )
        # In a real implementation, we would associate the todo with the user
        return new_todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    current_user: UserResponse = Depends(get_current_user)
):

    # Prepare update parameters from the request body
    update_params = {}
    if title is not None:
        update_params['title'] = title
    if description is not None:
        update_params['description'] = description

    if not update_params:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        updated_todo = todo_service.update_todo(todo_id, **update_params)
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        # In a real implementation, we would check if the todo belongs to the user
        return updated_todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/todos/{todo_id}/toggle", response_model=Todo)
def toggle_todo_completion(todo_id: int, current_user: UserResponse = Depends(get_current_user)):
    """Toggle the completion status of a todo"""
    success = todo_service.toggle_completion(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Return the updated todo
    updated_todo = todo_service.get_todo_by_id(todo_id)
    # In a real implementation, we would check if the todo belongs to the user
    return updated_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: UserResponse = Depends(get_current_user)):
    """Delete a todo by ID"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    # In a real implementation, we would check if the todo belongs to the user
    return {"message": "Todo deleted successfully"}


# DISABLED: Chatbot module - commented out for stable baseline
'''
@app.post("/api/{user_id}/chat")
async def chat_endpoint(user_id: str, request: dict):
    """
    Chat endpoint that handles user messages and returns AI responses
    """
    # This endpoint is disabled in the stable baseline
    raise HTTPException(status_code=501, detail="Chat functionality is disabled in stable baseline")
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)