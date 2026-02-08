"""
AI Agent for processing user input and mapping to MCP tools
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..mcp.server import mcp_server
from ..mcp.tools import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


class AgentResponse(BaseModel):
    response: str
    tool_calls: List[ToolCall] = []


class TodoAgent:
    """
    AI Agent that processes user input and maps to appropriate MCP tools
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.confirmation_required_tools = ["complete_task", "delete_task", "update_task"]

    async def process_input(self, user_input: str, conversation_history: List[Dict[str, str]] = []) -> AgentResponse:
        """
        Process user input and return response with potential tool calls
        """
        # Analyze the user input to determine intent
        intent_analysis = await self._analyze_intent(user_input, conversation_history)

        if intent_analysis.get("requires_confirmation"):
            # Ask for confirmation before executing destructive actions
            confirmation_needed = await self._check_confirmation_needed(intent_analysis["tool_calls"])
            if confirmation_needed:
                return AgentResponse(
                    response="To proceed with this action, I need your confirmation. Would you like me to continue?",
                    tool_calls=[]
                )

        # Execute tool calls if any
        tool_results = []
        for tool_call in intent_analysis["tool_calls"]:
            try:
                result = await mcp_server.execute_tool(tool_call.name, tool_call.arguments)
                tool_results.append({
                    "name": tool_call.name,
                    "arguments": tool_call.arguments,
                    "result": result
                })
            except Exception as e:
                # Handle MCP server unavailability
                tool_results.append({
                    "name": tool_call.name,
                    "arguments": tool_call.arguments,
                    "result": {
                        "success": False,
                        "error": f"MCP server unavailable: {str(e)}"
                    }
                })

        # Generate response based on tool results
        response = await self._generate_response(user_input, tool_results)

        return AgentResponse(
            response=response,
            tool_calls=intent_analysis["tool_calls"]
        )

    async def _analyze_intent(self, user_input: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze user input to determine the appropriate tools to call
        """
        # Convert user input to lowercase for easier matching
        lower_input = user_input.lower().strip()
        
        tool_calls = []
        requires_confirmation = False
        
        # Check for add_task intent
        if any(keyword in lower_input for keyword in ["add", "create", "new", "make"]):
            # Extract task title and description from the input
            title = self._extract_task_title(lower_input)
            if title:
                tool_calls.append(ToolCall(
                    name="add_task",
                    arguments={"title": title, "user_id": self.user_id}
                ))
        
        # Check for list_tasks intent
        elif any(keyword in lower_input for keyword in ["list", "show", "view", "see", "my tasks", "what"]):
            tool_calls.append(ToolCall(
                name="list_tasks",
                arguments={"user_id": self.user_id}
            ))
        
        # Check for complete_task intent
        elif any(keyword in lower_input for keyword in ["complete", "done", "finish", "mark as done"]):
            task_id = self._extract_task_id(lower_input)
            if task_id:
                tool_calls.append(ToolCall(
                    name="complete_task",
                    arguments={"task_id": task_id, "user_id": self.user_id}
                ))
                requires_confirmation = True
        
        # Check for delete_task intent
        elif any(keyword in lower_input for keyword in ["delete", "remove", "cancel"]):
            task_id = self._extract_task_id(lower_input)
            if task_id:
                tool_calls.append(ToolCall(
                    name="delete_task",
                    arguments={"task_id": task_id, "user_id": self.user_id}
                ))
                requires_confirmation = True
        
        # Check for update_task intent
        elif any(keyword in lower_input for keyword in ["update", "change", "modify", "edit"]):
            task_id = self._extract_task_id(lower_input)
            if task_id:
                # Extract new title or description if available
                new_title = self._extract_task_title(lower_input)
                tool_calls.append(ToolCall(
                    name="update_task",
                    arguments={"task_id": task_id, "user_id": self.user_id, "title": new_title}
                ))
                requires_confirmation = True
        
        return {
            "tool_calls": tool_calls,
            "requires_confirmation": requires_confirmation
        }

    def _extract_task_title(self, user_input: str) -> Optional[str]:
        """
        Extract task title from user input
        """
        # Common patterns for task titles
        import re
        
        # Look for phrases like "add task to buy groceries" or "create task 'buy groceries'"
        patterns = [
            r"(?:add|create|make|new)\s+(?:task|todo|item)\s+(?:to\s+)?(.+?)(?:\.|$)",
            r"(?:add|create|make|new)\s+(?:task|todo|item)\s+[\"'](.+?)[\"']",
            r"(?:to|that|should)\s+(.+?)(?:\.|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up the title
                title = title.replace("to ", "").strip()
                if title:
                    return title
        
        # If no specific pattern matched, return the whole input as title
        # but only if it seems like a reasonable task title
        clean_input = user_input.replace("add task", "").replace("create task", "").strip()
        if clean_input and len(clean_input) < 100:  # Reasonable length for a task
            return clean_input
        
        return None

    def _extract_task_id(self, user_input: str) -> Optional[int]:
        """
        Extract task ID from user input
        """
        import re
        
        # Look for numbers in the input that might represent task IDs
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            # Return the first number found (assuming it's the task ID)
            return int(numbers[0])
        
        return None

    async def _check_confirmation_needed(self, tool_calls: List[ToolCall]) -> bool:
        """
        Check if any of the tool calls require confirmation
        """
        for tool_call in tool_calls:
            if tool_call.name in self.confirmation_required_tools:
                return True
        return False

    async def _generate_response(self, user_input: str, tool_results: List[Dict[str, Any]]) -> str:
        """
        Generate a natural language response based on tool results
        """
        if not tool_results:
            # If no tools were called, provide a default response
            return "I'm not sure how to help with that. You can ask me to add, list, complete, update, or delete tasks."
        
        # Process the tool results and generate a response
        responses = []
        
        for result in tool_results:
            tool_name = result["name"]
            tool_result = result["result"]
            
            if tool_result["success"]:
                if tool_name == "add_task":
                    responses.append(f"I've added the task '{result['arguments'].get('title', 'unnamed')}' to your list.")
                elif tool_name == "list_tasks":
                    tasks = tool_result.get("tasks", [])
                    if tasks:
                        task_list = [f"- {task.get('title', 'Unnamed task')} ({'✓' if task.get('completed') else '○'})" 
                                    for task in tasks[:5]]  # Limit to first 5 tasks
                        extra_count = len(tasks) - 5
                        extra_msg = f"\n... and {extra_count} more tasks" if extra_count > 0 else ""
                        responses.append(f"Here are your tasks:\n" + "\n".join(task_list) + extra_msg)
                    else:
                        responses.append("You don't have any tasks on your list.")
                elif tool_name == "complete_task":
                    responses.append(f"I've marked the task as complete.")
                elif tool_name == "delete_task":
                    responses.append(f"I've deleted the task from your list.")
                elif tool_name == "update_task":
                    responses.append(f"I've updated the task.")
            else:
                error_msg = tool_result.get("error", "Unknown error occurred")
                responses.append(f"Sorry, I couldn't complete that action: {error_msg}")
        
        return " ".join(responses)

    async def confirm_action(self, user_response: str) -> bool:
        """
        Check if user confirmed the action
        """
        user_response_lower = user_response.lower().strip()
        return user_response_lower in ["yes", "y", "confirm", "ok", "okay", "sure", "please do", "go ahead"]

    async def resume_conversation(self, conversation_context: List[Dict[str, str]]) -> str:
        """
        Resume a conversation by analyzing the context and generating an appropriate response
        """
        # Analyze the last few exchanges to understand the conversation state
        if not conversation_context:
            return "Hello! How can I help you with your tasks today?"

        # Look at the last few messages to understand the context
        recent_messages = conversation_context[-3:]  # Look at last 3 messages

        # Check if there was a pending action that needs confirmation
        for msg in reversed(recent_messages):
            if msg["role"] == "assistant" and "confirmation" in msg["content"].lower():
                return "I'm still waiting for your confirmation to proceed with the action. Would you like me to continue?"

        # If the conversation was about a specific task, acknowledge it
        return "Welcome back! How can I assist you with your tasks?"