"""
Standalone MCP server implementation
"""
import asyncio
import json
from typing import Dict, Any, Callable
from pydantic import BaseModel
from .tools import add_task, list_tasks, complete_task, delete_task, update_task
from .tools import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams


class MCPServer:
    """
    MCP Server that exposes tools for the AI agent to use
    """
    def __init__(self):
        self.tools: Dict[str, Callable] = {
            "add_task": self._wrap_tool(add_task, AddTaskParams),
            "list_tasks": self._wrap_tool(list_tasks, ListTasksParams),
            "complete_task": self._wrap_tool(complete_task, CompleteTaskParams),
            "delete_task": self._wrap_tool(delete_task, DeleteTaskParams),
            "update_task": self._wrap_tool(update_task, UpdateTaskParams),
        }

    def _wrap_tool(self, func, param_class):
        """
        Wrap a tool function to handle parameter parsing
        """
        async def wrapper(arguments: Dict[str, Any]) -> Dict[str, Any]:
            try:
                # Parse arguments using Pydantic model
                params = param_class(**arguments)
                # Call the actual function
                result = await func(params)
                return result
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Invalid arguments: {str(e)}"
                }
        
        return wrapper

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with the given arguments
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }
        
        tool_func = self.tools[tool_name]
        return await tool_func(arguments)

    def get_tool_list(self) -> list:
        """
        Get a list of available tools
        """
        return list(self.tools.keys())

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """
        Get the schema for a specific tool (simplified for this implementation)
        """
        # In a real implementation, this would return the JSON schema for the tool
        # For now, we'll return a basic schema
        schemas = {
            "add_task": {
                "name": "add_task",
                "description": "Add a new task to the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "The description of the task (optional)"},
                        "user_id": {"type": "string", "description": "The ID of the user"}
                    },
                    "required": ["title", "user_id"]
                }
            },
            "list_tasks": {
                "name": "list_tasks",
                "description": "List all tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"}
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"},
                        "user_id": {"type": "string", "description": "The ID of the user"}
                    },
                    "required": ["task_id", "user_id"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Delete a task from the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                        "user_id": {"type": "string", "description": "The ID of the user"}
                    },
                    "required": ["task_id", "user_id"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Update a task in the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "title": {"type": "string", "description": "New title for the task (optional)"},
                        "description": {"type": "string", "description": "New description for the task (optional)"},
                        "completed": {"type": "boolean", "description": "New completion status (optional)"}
                    },
                    "required": ["task_id", "user_id"]
                }
            }
        }
        return schemas.get(tool_name, {})


# Global MCP server instance
mcp_server = MCPServer()


async def run_mcp_server():
    """
    Run the MCP server (placeholder implementation)
    In a real implementation, this would start an actual server
    """
    print("MCP Server started...")
    print(f"Available tools: {mcp_server.get_tool_list()}")
    
    # Example of how to use the server
    # result = await mcp_server.execute_tool("list_tasks", {"user_id": "user123"})
    # print(result)
    
    # Keep the server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("MCP Server shutting down...")


if __name__ == "__main__":
    asyncio.run(run_mcp_server())