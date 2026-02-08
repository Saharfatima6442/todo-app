"""
Router for chat endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from typing import Optional
from uuid import UUID
import json
from ..database.session import get_session
from ..models.conversation import Conversation
from ..models.message import Message
from ..chat.agent import TodoAgent
from ..chat.services.conversation_service import ConversationService
from ..chat.services.message_service import MessageService
from ..middleware.auth import get_current_user, verify_user_owns_resource


router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


class ChatRequest:
    def __init__(self, message: str, conversation_id: Optional[str] = None):
        self.message = message
        self.conversation_id = conversation_id


class ChatResponse:
    def __init__(self, response: str, conversation_id: str, tool_calls: list):
        self.response = response
        self.conversation_id = conversation_id
        self.tool_calls = tool_calls


@router.post("/chat")
async def chat_endpoint(
    user_id: str,
    request: dict,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that handles user messages and returns AI responses
    """
    try:
        # Verify that the authenticated user matches the user_id in the path
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Extract message and optional conversation_id from request
        message_text = request.get("message", "")
        conversation_id_str = request.get("conversation_id", None)

        if not message_text:
            raise HTTPException(status_code=400, detail="Message is required")

        # Initialize services
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Get or create conversation
        if conversation_id_str:
            try:
                conversation_id = UUID(conversation_id_str)
                conversation = conversation_service.get_conversation(conversation_id)
                if not conversation or not verify_user_owns_resource(user_id, conversation.user_id):
                    # If conversation doesn't exist or doesn't belong to user, create new one
                    conversation = conversation_service.create_conversation(user_id, title=message_text[:50] + "..." if len(message_text) > 50 else message_text)
            except ValueError:
                # Invalid UUID, create new conversation
                conversation = conversation_service.create_conversation(user_id, title=message_text[:50] + "..." if len(message_text) > 50 else message_text)
        else:
            # Create new conversation
            conversation = conversation_service.create_conversation(user_id, title=message_text[:50] + "..." if len(message_text) > 50 else message_text)

        # Save user message to database
        user_message = message_service.create_message(conversation.id, "user", message_text)

        # Initialize the AI agent
        agent = TodoAgent(user_id)

        # Get conversation history for context
        conversation_history = []
        messages = message_service.get_messages_for_conversation(conversation.id)
        for msg in messages:
            conversation_history.append({"role": msg.role, "content": msg.content})

        # Process the user input with the agent
        agent_response = await agent.process_input(message_text, conversation_history)

        # Save assistant message to database
        assistant_message = message_service.create_message(conversation.id, "assistant", agent_response.response)

        # Prepare response
        response_data = {
            "response": agent_response.response,
            "conversation_id": str(conversation.id),
            "tool_calls": [call.dict() for call in agent_response.tool_calls]
        }

        return response_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and return a generic error response
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")