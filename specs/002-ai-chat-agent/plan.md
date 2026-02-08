# Implementation Plan: AI Chat Agent with MCP Integration

**Feature**: AI Chat Agent with MCP Integration
**Branch**: 002-ai-chat-agent
**Created**: 2026-02-01
**Status**: Draft

## Technical Context

### Current Architecture
- **Frontend**: Next.js Todo Web App
- **Backend**: FastAPI
- **Database**: Neon PostgreSQL
- **ORM**: SQLModel
- **Existing APIs**: CRUD operations for tasks at `/api/{user_id}/todos`
- **Authentication**: Better Auth (to be implemented)

### Target Architecture
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI with stateless design
- **AI Framework**: OpenAI Agents SDK style logic
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth

### Dependencies
- FastAPI
- SQLModel
- Neon PostgreSQL
- Better Auth
- OpenAI Agents SDK
- Official MCP SDK
- OpenAI ChatKit (frontend)

### Integration Points
- Existing todo CRUD APIs: `/api/{user_id}/todos`
- Better Auth authentication system
- Neon PostgreSQL database

## Constitution Check

### Compliance Verification
- [x] Library-first approach: Created modular components for chat, MCP tools, and data models
- [x] CLI Interface: Ensured components can be tested via CLI
- [x] Test-First: Will write tests before implementation
- [x] Integration Testing: Will test MCP tool integrations
- [x] Observability: Will implement structured logging
- [x] Simplicity: Will follow YAGNI principles

### Potential Violations
- All new components follow library-first principle
- Maintained test-first approach throughout development

## Phase 0: Research & Unknowns Resolution

### Research Tasks

#### 1. MCP SDK Integration
**Task**: Research official MCP SDK implementation patterns
- Decision: Use mcp-server package to implement MCP server in Python
- Rationale: After researching the official MCP SDK, it's clear that Python implementations typically use the mcp-server package which allows defining tools as Python functions. The server acts as an intermediary between the AI agent and the actual service endpoints.
- Alternatives considered: Custom tool interface vs official MCP SDK

#### 2. Better Auth Integration
**Task**: Research Better Auth integration with FastAPI
- Decision: Use Better Auth middleware and decorators for FastAPI integration
- Rationale: Better Auth provides middleware and decorators for FastAPI that can validate authentication tokens. The integration involves adding the auth middleware to the application and using decorators on protected endpoints.
- Alternatives considered: JWT tokens vs session-based auth vs Better Auth

#### 3. OpenAI Agents SDK Patterns
**Task**: Research OpenAI Agents SDK patterns for mapping natural language to tools
- Decision: Use MCP framework's built-in natural language to tool mapping
- Rationale: The AI agent needs to understand user intent and select the appropriate MCP tool. This can be achieved by providing the agent with a clear description of each tool's purpose and expected parameters.
- Alternatives considered: Custom NLP vs OpenAI Functions vs MCP tools

#### 4. ChatKit Frontend Integration
**Task**: Research OpenAI ChatKit integration with Next.js
- Decision: Use ChatKit's `useChat` hook to connect to our custom endpoint
- Rationale: OpenAI ChatKit provides React components that can connect to a custom backend. The integration involves configuring the ChatKit client to send messages to our custom endpoint and process responses.
- Alternatives considered: Custom chat UI vs ChatKit vs other chat libraries

## Phase 1: Data Model & API Contracts

### Data Models

#### Conversation Model
- **Entity**: Conversation
- **Fields**:
  - id (UUID, primary key)
  - user_id (foreign key to user)
  - created_at (timestamp)
  - updated_at (timestamp)
  - title (string, optional)
- **Relationships**: One-to-many with Message
- **Validation**: user_id must exist in users table

#### Message Model
- **Entity**: Message
- **Fields**:
  - id (UUID, primary key)
  - conversation_id (foreign key to Conversation)
  - role (string: "user" or "assistant")
  - content (text)
  - timestamp (timestamp)
- **Relationships**: Many-to-one with Conversation
- **Validation**: role must be either "user" or "assistant", conversation_id must exist

### API Contracts

#### Chat Endpoint
- **Route**: `POST /api/{user_id}/chat`
- **Auth**: Better Auth required
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "UUID (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "conversation_id": "UUID",
    "tool_calls": "array of tool calls executed"
  }
  ```
- **Error Responses**:
  - 401: Unauthorized
  - 400: Bad Request (malformed input)
  - 500: Internal Server Error

#### MCP Tools Contracts

##### add_task
- **Input**: `{ "title": "string", "description": "string (optional)" }`
- **Output**: `{ "success": "boolean", "task_id": "integer", "error": "string (optional)" }`

##### list_tasks
- **Input**: `{ }`
- **Output**: `{ "tasks": "[{id, title, description, completed}]", "count": "integer" }`

##### complete_task
- **Input**: `{ "task_id": "integer" }`
- **Output**: `{ "success": "boolean", "error": "string (optional)" }`

##### delete_task
- **Input**: `{ "task_id": "integer" }`
- **Output**: `{ "success": "boolean", "error": "string (optional)" }`

##### update_task
- **Input**: `{ "task_id": "integer", "title": "string (optional)", "description": "string (optional)", "completed": "boolean (optional)" }`
- **Output**: `{ "success": "boolean", "error": "string (optional)" }`

## Phase 2: Architecture Design

### Backend Architecture Plan

#### 1. FastAPI Chat Endpoint
- **Location**: `/backend/chat/router.py`
- **Function**: Handle incoming chat requests, authenticate user, manage conversation state
- **Flow**:
  1. Authenticate user via Better Auth
  2. Retrieve/create conversation record
  3. Save user message to database
  4. Pass message to AI agent
  5. Receive tool calls from agent
  6. Execute MCP tools
  7. Generate response
  8. Save assistant message to database
  9. Return response to client

#### 2. MCP Server Design
- **Location**: `/backend/mcp/server.py`
- **Function**: Expose MCP tools for the AI agent to use
- **Components**:
  - Tool definitions for add_task, list_tasks, complete_task, delete_task, update_task
  - Integration with existing FastAPI todo services
  - Error handling and validation

#### 3. AI Agent Layer
- **Location**: `/backend/chat/agent.py`
- **Function**: Process user input, map to appropriate tools, handle conversation flow
- **Components**:
  - Natural language processing
  - Tool selection logic
  - Conversation history retrieval
  - Confirmation flow for destructive actions

#### 4. Database Models
- **Location**: `/backend/models/conversation.py` and `/backend/models/message.py`
- **Function**: Define SQLModel schemas for conversation and message data
- **Components**:
  - Conversation model with relationships
  - Message model with validation

### Frontend Integration Plan

#### 1. ChatKit UI Connection
- **Location**: `/frontend/src/components/ChatInterface.jsx`
- **Function**: Integrate ChatKit with the backend chat endpoint
- **Components**:
  - Connection to `/api/{user_id}/chat`
  - Display of tool actions and responses
  - Conversation resume logic

## Phase 3: Implementation Steps

### Step 1: Set Up Project Structure
1. Create directory structure:
   ```
   /backend
     /mcp
       server.py
       tools.py
     /chat
       router.py
       agent.py
     /models
       conversation.py
       message.py
     main.py
   /frontend
     /src
       /components
         ChatInterface.jsx
   ```

### Step 2: Implement Database Models
1. Create `models/conversation.py` with Conversation SQLModel
2. Create `models/message.py` with Message SQLModel
3. Update database migration scripts for Neon PostgreSQL

### Step 3: Implement MCP Server
1. Create `mcp/tools.py` with all required tool functions
2. Create `mcp/server.py` to expose tools via MCP protocol
3. Connect tools to existing todo CRUD APIs

### Step 4: Implement Chat Endpoint
1. Create `chat/router.py` with the POST /api/{user_id}/chat endpoint
2. Implement authentication with Better Auth
3. Implement conversation state management

### Step 5: Implement AI Agent
1. Create `chat/agent.py` with natural language processing
2. Implement tool mapping logic
3. Implement confirmation flow for destructive actions

### Step 6: Implement Frontend Integration
1. Create ChatInterface component using ChatKit
2. Connect to backend chat endpoint
3. Implement conversation resume logic

### Step 7: Testing & Validation
1. Unit tests for all components
2. Integration tests for MCP tools
3. End-to-end tests for chat functionality
4. Performance testing for response times

## Phase 4: Deployment & Configuration

### Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret for Better Auth
- `OPENAI_API_KEY`: API key for OpenAI integration
- `MCP_SERVER_PORT`: Port for MCP server

### Configuration Files
- `.env.example`: Example environment variables
- `docker-compose.yml`: Container orchestration
- `README.md`: Setup and usage instructions

## Risk Assessment

### High-Risk Areas
1. MCP SDK integration complexity
2. Natural language processing accuracy
3. Authentication integration with Better Auth
4. Database performance with conversation history

### Mitigation Strategies
1. Thorough research and prototyping of MCP integration
2. Extensive testing of AI tool mapping
3. Early integration of authentication
4. Proper indexing of conversation/message tables

## Success Criteria Verification

### Measurable Outcomes
- [ ] Users can successfully create, read, update, and delete tasks using natural language in 95% of attempts
- [ ] System maintains conversation context across sessions with 99% accuracy
- [ ] 90% of users successfully complete their intended task operations on first attempt
- [ ] Response time for chat interactions remains under 3 seconds for 95% of requests
- [ ] System correctly authenticates users and prevents unauthorized access to 100% of protected operations