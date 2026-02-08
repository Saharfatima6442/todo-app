---
id: "003"
title: "ai-chat-agent-specification"
stage: "spec"
date_iso: "2026-02-01"
surface: "agent"
model: "default"
feature: "ai-chat-agent"
branch: "002-ai-chat-agent"
user: "Saeed"
command: "/sp.specify You are a senior AI software architect. Project Context: I have already completed: Phase 1: - Python CLI todo application using Spec-Kit Plus Phase 2: - Frontend: Next.js Todo Web App - Backend: FastAPI - Database: Neon PostgreSQL - ORM: SQLModel - Working CRUD APIs for tasks: - POST /api/{user_id}/todos - GET /api/{user_id}/todos - PUT /api/{user_id}/todos/{id} - DELETE /api/{user_id}/todos/{id} Now I need Phase 3 implementation exactly according to the following requirements: TECH STACK (MANDATORY): - Frontend: OpenAI ChatKit - Backend: Python FastAPI - AI Framework: OpenAI Agents SDK style logic - MCP Server: Official MCP SDK - ORM: SQLModel - Database: Neon PostgreSQL - Authentication: Better Auth ARCHITECTURE RULES: - Server must be stateless - Conversation history stored in database - AI must use MCP tools for ALL task operations - AI cannot access database directly - Only one API endpoint allowed: POST /api/{user_id}/chat DATABASE MODELS TO ADD: - Conversation (user_id, id, timestamps) - Message (conversation_id, role, content) MCP TOOLS REQUIRED: - add_task - list_tasks - complete_task - delete_task - update_task AGENT BEHAVIOR RULES: - User requests must be mapped to correct MCP tools - Always confirm actions - Graceful error handling - Context persistence via database TASK: Generate a complete, production-ready codebase with: 1. FastAPI chat endpoint implementation 2. MCP server implementation exposing all tools 3. Agent runner logic compatible with Qwen 4. SQLModel database models 5. Example ChatKit frontend integration 6. Folder structure 7. Example .env 8. README instructions OUTPUT FORMAT: Return code in the following structure: /backend /mcp server.py tools.py /chat router.py agent.py /models conversation.py message.py main.py /frontend chatkit integration example Provide full runnable code only. Do NOT modify existing todo CRUD APIs – reuse them."
labels: ["specification", "ai-chat", "mcp", "todo-app"]
links:
  spec: "../specs/002-ai-chat-agent/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/002-ai-chat-agent/spec.md"
  - "specs/002-ai-chat-agent/checklists/requirements.md"
tests_yaml: []
outcome: "Successfully created feature specification for AI Chat Agent with MCP integration. Created branch 002-ai-chat-agent and documented requirements for implementing an AI-powered chat interface that uses MCP tools for todo operations."
evaluation: "Specification is complete with user scenarios, functional requirements, and success criteria. Ready for planning phase."
---

# Prompt

```
/sp.specify You are a senior AI software architect. Project Context: I have already completed: Phase 1: - Python CLI todo application using Spec-Kit Plus Phase 2: - Frontend: Next.js Todo Web App - Backend: FastAPI - Database: Neon PostgreSQL - ORM: SQLModel - Working CRUD APIs for tasks: - POST /api/{user_id}/todos - GET /api/{user_id}/todos - PUT /api/{user_id}/todos/{id} - DELETE /api/{user_id}/todos/{id} Now I need Phase 3 implementation exactly according to the following requirements: TECH STACK (MANDATORY): - Frontend: OpenAI ChatKit - Backend: Python FastAPI - AI Framework: OpenAI Agents SDK style logic - MCP Server: Official MCP SDK - ORM: SQLModel - Database: Neon PostgreSQL - Authentication: Better Auth ARCHITECTURE RULES: - Server must be stateless - Conversation history stored in database - AI must use MCP tools for ALL task operations - AI cannot access database directly - Only one API endpoint allowed: POST /api/{user_id}/chat DATABASE MODELS TO ADD: - Conversation (user_id, id, timestamps) - Message (conversation_id, role, content) MCP TOOLS REQUIRED: - add_task - list_tasks - complete_task - delete_task - update_task AGENT BEHAVIOR RULES: - User requests must be mapped to correct MCP tools - Always confirm actions - Graceful error handling - Context persistence via database TASK: Generate a complete, production-ready codebase with: 1. FastAPI chat endpoint implementation 2. MCP server implementation exposing all tools 3. Agent runner logic compatible with Qwen 4. SQLModel database models 5. Example ChatKit frontend integration 6. Folder structure 7. Example .env 8. README instructions OUTPUT FORMAT: Return code in the following structure: /backend /mcp server.py tools.py /chat router.py agent.py /models conversation.py message.py main.py /frontend chatkit integration example Provide full runnable code only. Do NOT modify existing todo CRUD APIs – reuse them.
```

# Response

I'll create a concise short name for the branch based on the feature description.

**Short name**: `ai-chat-agent`

Now I'll check for existing branches and create a new one with the appropriate number:

...

[Response content continues with the full interaction]