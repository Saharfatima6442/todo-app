"""
MCP tools for todo operations
"""
import asyncio
from typing import Dict, Any, Optional
import httpx
import os
from pydantic import BaseModel

# Base URL for the existing todo API
TODO_API_BASE_URL = os.getenv("TODO_API_BASE_URL", "http://localhost:8000")

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
            # Note: Our API uses query parameters, not JSON body
            params_dict = {"title": params.title}
            if params.description:
                params_dict["description"] = params.description
            
            # In a real implementation, we'd need to pass the user's auth token
            # For this demo, we'll call the endpoint directly
            # This is a limitation of the in-memory implementation
            response = await client.post(
                f"{TODO_API_BASE_URL}/todos",
                params=params_dict
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
            # In a real implementation, we'd need to pass the user's auth token
            # For this demo, we'll call the endpoint directly
            response = await client.get(f"{TODO_API_BASE_URL}/todos")

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
            # Toggle the completion status
            response = await client.patch(f"{TODO_API_BASE_URL}/todos/{params.task_id}/toggle")

            if response.status_code == 200:
                return {
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to complete task: {response.text}"
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
            response = await client.delete(f"{TODO_API_BASE_URL}/todos/{params.task_id}")

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
            # Prepare update parameters
            params_dict = {}
            if params.title is not None:
                params_dict["title"] = params.title
            if params.description is not None:
                params_dict["description"] = params.description

            # Send the update request
            response = await client.put(
                f"{TODO_API_BASE_URL}/todos/{params.task_id}",
                params=params_dict
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to update task: {response.text}"
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }