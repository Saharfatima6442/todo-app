"""
Service for managing conversations
"""
from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by ID"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.session.exec(statement).first()

    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.session.exec(statement).all()

    def get_full_conversation_with_messages(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation with all its messages for context"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = self.session.exec(statement).first()

        if conversation:
            # Eager load messages
            conversation.messages = sorted(conversation.messages, key=lambda m: m.timestamp)

        return conversation

    def update_conversation_title(self, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update conversation title"""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: UUID) -> bool:
        """Delete a conversation"""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False