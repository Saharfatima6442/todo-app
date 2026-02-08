# Data Model: AI Chat Agent with MCP Integration

## Entity: Conversation
- **Purpose**: Represents a single chat session with metadata
- **Fields**:
  - id (UUID, primary key)
  - user_id (foreign key to user, indexed)
  - created_at (timestamp with timezone, default now)
  - updated_at (timestamp with timezone, default now, auto-update)
  - title (string, optional, max 200 chars)
- **Relationships**: 
  - One-to-many with Message entity
- **Validation**: 
  - user_id must exist in users table
  - title length must be ≤ 200 characters if provided

## Entity: Message
- **Purpose**: Represents individual messages within a conversation
- **Fields**:
  - id (UUID, primary key)
  - conversation_id (foreign key to Conversation, indexed)
  - role (string enum: "user" or "assistant", not null)
  - content (text, not null)
  - timestamp (timestamp with timezone, default now)
- **Relationships**: 
  - Many-to-one with Conversation entity
- **Validation**: 
  - role must be either "user" or "assistant"
  - conversation_id must exist in conversations table
  - content must not be empty

## Relationship Diagram
```
User (users table)
  |
  | 1..*
  |
Conversation
  |
  | 1..*
  |
Message
```

## Indexes
- conversations.user_id: For efficient user-specific queries
- messages.conversation_id: For efficient conversation-specific queries
- messages.timestamp: For chronological ordering of messages