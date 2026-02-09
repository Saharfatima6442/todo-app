"""
Chat service for the todo application using OpenAI and MCP tools
"""
import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# Import the MCP tools
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from mcp.server import mcp_server

# Conditionally import OpenAI to handle cases where API key is not set
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    AsyncOpenAI = None
    OPENAI_AVAILABLE = False


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime


class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime


class ChatService:
    """
    Service class to handle chat interactions using OpenAI and MCP tools
    """
    def __init__(self):
        # Initialize OpenAI client if available
        self.client = None
        self.model = "gpt-3.5-turbo"  # Default model, can be configured
        self.openai_available = False
        
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = AsyncOpenAI(api_key=api_key)
                self.openai_available = True
            else:
                print("Warning: OPENAI_API_KEY environment variable is not set. Chat functionality will be limited.")
        else:
            print("Warning: OpenAI library not available. Chat functionality will be limited.")
        
        # In-memory storage for conversations (in production, use a database)
        self.conversations: Dict[str, List[ChatMessage]] = {}

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """
        Process a user message and return an AI response
        """
        # Get or initialize conversation history
        conversation_id = request.user_id
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Add user message to conversation history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.now()
        )
        self.conversations[conversation_id].append(user_message)
        
        # If OpenAI is not available, return a mock response
        if not self.openai_available:
            # Simple rule-based responses for demonstration
            message_lower = request.message.lower()
            
            if "hello" in message_lower or "hi" in message_lower:
                response_text = "Hello! I'm your AI assistant for managing todos. You can ask me to add, list, update, or delete your tasks."
            elif "add" in message_lower or "create" in message_lower:
                response_text = "I would normally add a task for you, but the OpenAI API is not configured. Please set your OPENAI_API_KEY environment variable."
            elif "list" in message_lower or "show" in message_lower:
                response_text = "I would normally list your tasks, but the OpenAI API is not configured. Please set your OPENAI_API_KEY environment variable."
            elif "complete" in message_lower or "done" in message_lower:
                response_text = "I would normally mark a task as complete, but the OpenAI API is not configured. Please set your OPENAI_API_KEY environment variable."
            elif "delete" in message_lower or "remove" in message_lower:
                response_text = "I would normally delete a task for you, but the OpenAI API is not configured. Please set your OPENAI_API_KEY environment variable."
            else:
                response_text = "I'm your AI assistant for managing todos. You can ask me to add, list, update, or delete your tasks. However, the OpenAI API is not configured. Please set your OPENAI_API_KEY environment variable."
            
            # Add the assistant's response to the conversation history
            assistant_message = ChatMessage(
                role="assistant",
                content=response_text,
                timestamp=datetime.now()
            )
            self.conversations[conversation_id].append(assistant_message)
            
            return ChatResponse(
                response=response_text,
                conversation_id=conversation_id,
                timestamp=datetime.now()
            )
        
        # Prepare messages for OpenAI API
        messages = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in self.conversations[conversation_id]
        ]
        
        # Add system instruction to guide the AI on using tools
        system_instruction = {
            "role": "system",
            "content": (
                "You are a helpful assistant for managing todos. "
                "You can help users add, list, update, complete, and delete their todos. "
                "Use the available tools when the user wants to perform these actions. "
                "Always ask for confirmation before performing destructive actions like deleting a todo. "
                "If the user wants to perform a todo operation, use the appropriate tool. "
                "Otherwise, respond conversationally."
            )
        }
        messages.insert(0, system_instruction)
        
        try:
            # Call OpenAI API with function calling capabilities
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[
                    {
                        "type": "function",
                        "function": {
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
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_tasks",
                            "description": "List all tasks for the user",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The ID of the user"}
                                },
                                "required": ["user_id"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
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
                        }
                    },
                    {
                        "type": "function",
                        "function": {
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
                        }
                    },
                    {
                        "type": "function",
                        "function": {
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
                ],
                tool_choice="auto"
            )
            
            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            if tool_calls:
                # Process tool calls
                final_response = ""
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    tool_result = await mcp_server.execute_tool(function_name, function_args)
                    
                    # Format the response based on the tool result
                    if function_name == "add_task":
                        if tool_result["success"]:
                            final_response += f"I've added the task '{function_args['title']}' to your list.\n"
                        else:
                            final_response += f"Sorry, I couldn't add the task: {tool_result['error']}\n"
                            
                    elif function_name == "list_tasks":
                        if tool_result["success"]:
                            if tool_result["count"] == 0:
                                final_response += "You don't have any tasks on your list.\n"
                            else:
                                final_response += f"You have {tool_result['count']} tasks:\n"
                                for i, task in enumerate(tool_result["tasks"][:5], 1):  # Show first 5 tasks
                                    status = "✓" if task.get("completed", False) else "○"
                                    title = task.get("title", "Untitled")
                                    final_response += f"  {i}. [{status}] {title}\n"
                                if len(tool_result["tasks"]) > 5:
                                    final_response += f"  ... and {len(tool_result['tasks']) - 5} more\n"
                        else:
                            final_response += f"Sorry, I couldn't retrieve your tasks: {tool_result['error']}\n"
                            
                    elif function_name == "complete_task":
                        if tool_result["success"]:
                            final_response += f"I've marked the task as complete.\n"
                        else:
                            final_response += f"Sorry, I couldn't complete the task: {tool_result['error']}\n"
                            
                    elif function_name == "delete_task":
                        if tool_result["success"]:
                            final_response += f"I've deleted the task from your list.\n"
                        else:
                            final_response += f"Sorry, I couldn't delete the task: {tool_result['error']}\n"
                            
                    elif function_name == "update_task":
                        if tool_result["success"]:
                            final_response += f"I've updated the task.\n"
                        else:
                            final_response += f"Sorry, I couldn't update the task: {tool_result['error']}\n"
                
                # Add the tool responses to the conversation history
                tool_response_message = ChatMessage(
                    role="assistant",
                    content=final_response.strip(),
                    timestamp=datetime.now()
                )
                self.conversations[conversation_id].append(tool_response_message)
                
                return ChatResponse(
                    response=final_response.strip(),
                    conversation_id=conversation_id,
                    timestamp=datetime.now()
                )
            else:
                # No tool calls, just return the assistant's response
                assistant_response = response_message.content
                
                # Add the assistant's response to the conversation history
                assistant_message = ChatMessage(
                    role="assistant",
                    content=assistant_response,
                    timestamp=datetime.now()
                )
                self.conversations[conversation_id].append(assistant_message)
                
                return ChatResponse(
                    response=assistant_response,
                    conversation_id=conversation_id,
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            error_msg = f"Sorry, I encountered an error processing your request: {str(e)}"
            
            # Add error message to conversation history
            error_message = ChatMessage(
                role="assistant",
                content=error_msg,
                timestamp=datetime.now()
            )
            self.conversations[conversation_id].append(error_message)
            
            return ChatResponse(
                response=error_msg,
                conversation_id=conversation_id,
                timestamp=datetime.now()
            )