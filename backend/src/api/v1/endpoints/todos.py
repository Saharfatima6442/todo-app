from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.api.deps import get_current_user
from src.models.user import User
from src.services.todo_service import todo_service

router = APIRouter(prefix="/api/{user_id}/todos", tags=["todos"])

@router.post("/", response_model=Todo)
async def create_todo(
    user_id: str,
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new todo item for the authenticated user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create todos for yourself"
        )
    
    try:
        # Create the todo with the authenticated user as the owner
        created_todo = todo_service.create_todo(todo_create, current_user.id)
        return created_todo
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the todo: {str(e)}"
        )

@router.get("/", response_model=list[Todo])
async def list_todos(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all todos for the authenticated user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own todos"
        )
    
    # Get all todos for the authenticated user
    todos = todo_service.get_todos_by_owner(current_user.id)
    return todos

@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    user_id: str,
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific todo by ID
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own todos"
        )
    
    # Get the specific todo
    todo = todo_service.get_todo_by_id(todo_id, current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    user_id: str,
    todo_id: str,
    todo_update: Dict,
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific todo by ID
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own todos"
        )
    
    # Convert the update data to TodoUpdate model
    from src.models.todo import TodoUpdate
    todo_update_model = TodoUpdate(**todo_update)
    
    # Update the todo
    updated_todo = todo_service.update_todo(todo_id, current_user.id, todo_update_model)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return updated_todo

@router.patch("/{todo_id}/toggle-completion", response_model=Todo)
async def toggle_todo_completion(
    user_id: str,
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific todo by ID
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only toggle completion status of your own todos"
        )

    # Get the current todo
    current_todo = todo_service.get_todo_by_id(todo_id, current_user.id)
    if not current_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Toggle the completion status
    update_data = {"completed": not current_todo.completed}
    updated_todo = todo_service.update_todo(todo_id, current_user.id, TodoUpdate(**update_data))

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return updated_todo


@router.delete("/{todo_id}")
async def delete_todo(
    user_id: str,
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific todo by ID
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own todos"
        )

    # Delete the todo
    success = todo_service.delete_todo(todo_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": "Todo deleted successfully"}