"""
Service for managing messages
"""
from typing import List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from ..models.message import Message, MessageCreate
from ..models.conversation import Conversation


class MessageService:
    def __init__(self, session: Session):
        self.session = session

    def get_message(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID"""
        statement = select(Message).where(Message.id == message_id)
        return self.session.exec(statement).first()

    def get_messages_for_conversation(self, conversation_id: UUID) -> List[Message]:
        """Get all messages for a conversation"""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def create_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        """Create a new message"""
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def delete_message(self, message_id: UUID) -> bool:
        """Delete a message"""
        message = self.get_message(message_id)
        if message:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

    def update_message_content(self, message_id: UUID, content: str) -> Optional[Message]:
        """Update message content"""
        message = self.get_message(message_id)
        if message:
            message.content = content
            message.timestamp = datetime.utcnow()  # Update timestamp
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
        return message