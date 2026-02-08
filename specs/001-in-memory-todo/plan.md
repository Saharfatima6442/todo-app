# Implementation Plan: JWT Authentication for Todo App

**Branch**: `001-in-memory-todo` | **Date**: 2026-01-19 | **Spec**: [specs/001-in-memory-todo/spec.md](specs/001-in-memory-todo/spec.md)
**Input**: Feature specification from `/specs/001-in-memory-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement stateless JWT authentication across frontend and backend so that every API request is authenticated via JWT, each user can only access their own tasks, and the backend independently verifies identity without calling the frontend. The existing REST endpoints remain unchanged.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for frontend
**Primary Dependencies**: FastAPI (backend), Better Auth (frontend authentication), PyJWT (backend JWT handling)
**Storage**: In-memory storage (as per spec), no persistent storage
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (frontend + backend)
**Project Type**: Web application (separate frontend and backend)
**Performance Goals**: <200ms authentication verification, <50ms token validation
**Constraints**: Stateless authentication, token-based security, zero-trust model for user IDs
**Scale/Scope**: Individual user isolation, variable performance by user tier

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Library-first approach: Authentication service as a reusable module
- [x] Test-first: All authentication flows covered by tests
- [x] Integration testing: JWT validation and user isolation tested
- [x] Observability: Proper logging of authentication events
- [x] Simplicity: Using standard JWT implementation without over-engineering

## Project Structure

### Documentation (this feature)

```text
specs/001-in-memory-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── todo.py
│   ├── services/
│   │   ├── auth.py
│   │   └── todo_service.py
│   ├── middleware/
│   │   └── jwt_auth.py
│   └── api/
│       ├── deps.py
│       └── v1/
│           └── endpoints/
│               └── todos.py
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   │   └── api_client.js
│   └── auth/
│       └── auth_provider.js
└── tests/
```

**Structure Decision**: Web application with separate frontend and backend components to handle the JWT authentication flow properly. The frontend handles user login and session management with Better Auth, while the backend implements JWT verification middleware to ensure all API requests are authenticated.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate frontend/backend | Required for JWT auth flow | Would compromise security model |
| Middleware implementation | Required for consistent auth enforcement | Per-endpoint checks would be inconsistent |

## Phase 0: Research & Unknown Resolution

### Research Tasks

1. **Better Auth Integration**: How to configure Better Auth to issue JWTs that can be validated by our backend
   - Decision: Use Better Auth's built-in JWT capabilities with shared secret
   - Rationale: Standard approach that aligns with industry practices
   - Alternatives considered: Custom JWT implementation vs. Better Auth's built-in support

2. **JWT Token Format**: What claims need to be included in the JWT for proper user identification
   - Decision: Include sub (user ID), email, iat (issued at), exp (expiration)
   - Rationale: Contains all necessary information for user identification and validation
   - Alternatives considered: Minimal claims vs. extended claims approach

3. **Shared Secret Management**: How to securely share the JWT signing secret between frontend and backend
   - Decision: Environment variable configuration with same value in both services
   - Rationale: Standard practice for microservice authentication
   - Alternatives considered: Separate secrets vs. shared secret approach

## Phase 1: Design & Contracts

### Data Model Updates

The authentication system introduces new data concepts that need to be reflected in our data model:

- User identity extracted from JWT token
- Ownership relationship between users and todos
- Authentication state management

### API Contract Modifications

All existing API endpoints will require authentication validation:

- GET /api/{user_id}/tasks → Requires valid JWT with matching user ID
- POST /api/{user_id}/tasks → Requires valid JWT with matching user ID
- PUT /api/{user_id}/tasks/{task_id} → Requires valid JWT with matching user ID
- DELETE /api/{user_id}/tasks/{task_id} → Requires valid JWT with matching user ID

### Authentication Flow

1. User authenticates via Better Auth on frontend
2. Better Auth issues JWT with user identity claims
3. Frontend stores JWT and attaches to all API requests
4. Backend middleware validates JWT signature and expiration
5. Backend enforces user ownership on all data operations

## Phase 2: Implementation Plan

### Component-Level Implementation

1. **Better Auth Configuration**:
   - Configure JWT plugin in Better Auth
   - Set token expiration (e.g., 7 days)
   - Define required claims (sub, email, iat, exp)

2. **Frontend API Client**:
   - Implement automatic JWT attachment to requests
   - Handle token expiration and refresh
   - Redirect to login on authentication failures

3. **Backend JWT Middleware**:
   - Extract and validate JWT from Authorization header
   - Verify signature using shared secret
   - Attach user identity to request context

4. **Backend API Route Protection**:
   - Enforce ownership checks on all data operations
   - Ensure user_id in JWT matches user_id in URL/route
   - Return appropriate error codes for unauthorized access

### Security Guarantees

- User Isolation: Each user only sees their own tasks
- Stateless Auth: No backend session storage required
- Token Expiry: Automatic session expiration
- Zero Trust URLs: URL user ID never trusted over JWT
- Independent Verification: Backend verifies auth without external calls
