"""
Additional router for conversation-related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.session import get_session
from ..models.conversation import Conversation
from ..models.message import Message
from ..chat.services.conversation_service import ConversationService
from ..chat.services.message_service import MessageService
from ..middleware.auth import get_current_user, verify_user_owns_resource


router = APIRouter(prefix="/api/{user_id}", tags=["conversations"])


@router.get("/conversations")
async def get_user_conversations(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all conversations for a user
    """
    try:
        # Verify that the authenticated user matches the user_id in the path
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        conversation_service = ConversationService(session)
        conversations = conversation_service.get_user_conversations(user_id)

        return {
            "conversations": [
                {
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_user_conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/conversations/{conversation_id}")
async def get_conversation_detail(
    user_id: str,
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific conversation including its messages
    """
    try:
        # Verify that the authenticated user matches the user_id in the path
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Validate conversation_id is a valid UUID
        try:
            uuid_conversation_id = UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID")

        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Verify the conversation belongs to the user
        conversation = conversation_service.get_conversation(uuid_conversation_id)
        if not conversation or not verify_user_owns_resource(user_id, conversation.user_id):
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get all messages for this conversation
        messages = message_service.get_messages_for_conversation(uuid_conversation_id)

        return {
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            },
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_conversation_detail: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")