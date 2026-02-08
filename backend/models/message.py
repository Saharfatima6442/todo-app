"""
SQLModel model for Message entity
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # Either "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    """
    Represents individual messages within a conversation
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: UUID
    timestamp: datetime