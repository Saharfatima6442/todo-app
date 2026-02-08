"""
MCP tools for todo operations
"""
import asyncio
from typing import Dict, Any, Optional
import httpx
import os
from pydantic import BaseModel

# Base URL for the existing todo API
TODO_API_BASE_URL = os.getenv("TODO_API_BASE_URL", "http://localhost:8000/api")

class AddTaskParams(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: str

async def add_task(params: AddTaskParams) -> Dict[str, Any]:
    """
    Add a new task via the existing todo API
    """
    try:
        # Validate input parameters
        if not params.title or not params.title.strip():
            return {
                "success": False,
                "task_id": None,
                "error": "Title is required and cannot be empty"
            }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TODO_API_BASE_URL}/{params.user_id}/todos",
                json={
                    "title": params.title,
                    "description": params.description or "",
                    "completed": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "task_id": result.get("id"),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "task_id": None,
                    "error": f"Failed to add task: {response.text}"
                }
    except httpx.RequestError as e:
        return {
            "success": False,
            "task_id": None,
            "error": f"Network error occurred: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "task_id": None,
            "error": f"Unexpected error: {str(e)}"
        }


class ListTasksParams(BaseModel):
    user_id: str

async def list_tasks(params: ListTasksParams) -> Dict[str, Any]:
    """
    List all tasks for a user via the existing todo API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TODO_API_BASE_URL}/{params.user_id}/todos")
            
            if response.status_code == 200:
                tasks = response.json()
                return {
                    "success": True,
                    "tasks": tasks,
                    "count": len(tasks),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "tasks": [],
                    "count": 0,
                    "error": f"Failed to list tasks: {response.text}"
                }
    except Exception as e:
        return {
            "success": False,
            "tasks": [],
            "count": 0,
            "error": str(e)
        }


class CompleteTaskParams(BaseModel):
    task_id: int
    user_id: str

async def complete_task(params: CompleteTaskParams) -> Dict[str, Any]:
    """
    Mark a task as complete via the existing todo API
    """
    try:
        async with httpx.AsyncClient() as client:
            # First get the task to update it
            get_response = await client.get(f"{TODO_API_BASE_URL}/{params.user_id}/todos/{params.task_id}")
            
            if get_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Task with ID {params.task_id} not found"
                }
                
            task_data = get_response.json()
            task_data["completed"] = True
            
            # Update the task
            put_response = await client.put(
                f"{TODO_API_BASE_URL}/{params.user_id}/todos/{params.task_id}",
                json=task_data
            )
            
            if put_response.status_code == 200:
                return {
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to complete task: {put_response.text}"
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


class DeleteTaskParams(BaseModel):
    task_id: int
    user_id: str

async def delete_task(params: DeleteTaskParams) -> Dict[str, Any]:
    """
    Delete a task via the existing todo API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{TODO_API_BASE_URL}/{params.user_id}/todos/{params.task_id}")
            
            if response.status_code in [200, 204]:
                return {
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to delete task: {response.text}"
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


class UpdateTaskParams(BaseModel):
    task_id: int
    user_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

async def update_task(params: UpdateTaskParams) -> Dict[str, Any]:
    """
    Update a task via the existing todo API
    """
    try:
        async with httpx.AsyncClient() as client:
            # First get the current task
            get_response = await client.get(f"{TODO_API_BASE_URL}/{params.user_id}/todos/{params.task_id}")
            
            if get_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Task with ID {params.task_id} not found"
                }
                
            task_data = get_response.json()
            
            # Update fields that were provided
            if params.title is not None:
                task_data["title"] = params.title
            if params.description is not None:
                task_data["description"] = params.description
            if params.completed is not None:
                task_data["completed"] = params.completed
                
            # Update the task
            put_response = await client.put(
                f"{TODO_API_BASE_URL}/{params.user_id}/todos/{params.task_id}",
                json=task_data
            )
            
            if put_response.status_code == 200:
                return {
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to update task: {put_response.text}"
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }