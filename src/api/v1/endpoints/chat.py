"""
Chat API endpoints for the todo application
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.models.user_db import UserResponse
from src.api.deps import get_current_user
from src.services.chat_service import ChatRequest, ChatService, ChatResponse


router = APIRouter()
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Chat endpoint that handles user messages and returns AI responses
    """
    try:
        # Override the user_id in the request with the authenticated user's ID
        request.user_id = current_user.id
        
        # Process the message through the chat service
        response = await chat_service.process_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.get("/conversations")
async def get_conversations(current_user: UserResponse = Depends(get_current_user)):
    """
    Get a list of user's conversations
    """
    # This would return conversation metadata in a real implementation
    # For now, we'll return a simple response
    return {"message": "Conversations endpoint is working", "user_id": current_user.id}


@router.get("/conversations/{conversation_id}")
async def get_conversation_detail(
    conversation_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get specific conversation details
    """
    # This would return specific conversation details in a real implementation
    # For now, we'll return a simple response
    return {
        "message": f"Conversation {conversation_id} details",
        "user_id": current_user.id,
        "conversation_id": conversation_id
    }