"""
REST API for the todo application using FastAPI
"""
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from src.models.todo import Todo
from src.services.todo_service import TodoService


# Create a global instance of TodoService to maintain state across requests
# In a real application, you would use dependency injection or a database
todo_service = TodoService()

app = FastAPI(title="Todo API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Todo API"}


@app.get("/todos", response_model=List[Todo])
def get_todos():
    """Get all todos"""
    return todo_service.get_all_todos()


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=Todo)
def create_todo(todo_data: Todo):
    """Create a new todo"""
    # Extract only the fields we need for creation
    try:
        new_todo = todo_service.add_todo(
            title=todo_data.title,
            description=todo_data.description
        )
        return new_todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, title: Optional[str] = None, description: Optional[str] = None):
    """Update an existing todo"""
    # Check if todo exists
    existing_todo = todo_service.get_todo_by_id(todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Prepare update parameters
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
        return updated_todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/todos/{todo_id}/toggle", response_model=Todo)
def toggle_todo_completion(todo_id: int):
    """Toggle the completion status of a todo"""
    success = todo_service.toggle_completion(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Return the updated todo
    updated_todo = todo_service.get_todo_by_id(todo_id)
    return updated_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo by ID"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)