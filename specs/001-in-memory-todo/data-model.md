# Data Model: JWT Authenticated Todo Application

## Overview
This document describes the data model for the JWT authenticated todo application, including user identity and task ownership relationships.

## Entities

### User (from JWT)
Represents the authenticated user identity extracted from the JWT token.

**Attributes:**
- `id` (string): Unique user identifier (from JWT `sub` claim)
- `email` (string): User's email address (from JWT `email` claim)
- `authenticated` (boolean): Whether the user is currently authenticated

**Notes:**
- User data is not stored locally but extracted from JWT tokens
- Authentication state is maintained via JWT validity

### Todo
Represents a task with an ID (unique identifier), title (string), description (string), completion status (boolean), and owner (user ID).

**Attributes:**
- `id` (string): Unique identifier for the todo
- `title` (string): Title of the task (1-100 characters)
- `description` (string): Detailed description of the task (up to 500 characters)
- `completed` (boolean): Whether the task is completed
- `owner_id` (string): ID of the user who owns this task

**Relationships:**
- Belongs to one User (via `owner_id`)

**Validation Rules:**
- Title must be 1-100 characters
- Description must be up to 500 characters
- Owner ID must match the authenticated user's ID

### Session
Represents the current authenticated session state.

**Attributes:**
- `jwt_token` (string): The current JWT token
- `expires_at` (datetime): When the token expires
- `user_id` (string): Associated user ID

## State Transitions

### Todo State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user marks task as incomplete

## Access Control Rules

### Ownership Enforcement
- A user can only access todos where `todo.owner_id` equals the user's ID from JWT
- All API operations must validate that the authenticated user owns the resources they're accessing
- Requests with mismatched user IDs in URL vs JWT will be rejected

## Data Flow

### Creation Flow
1. User authenticates and receives JWT
2. JWT contains user ID in `sub` claim
3. When creating a todo, `owner_id` is set to user ID from JWT
4. Todo is stored with ownership information

### Access Flow
1. User makes request with JWT in Authorization header
2. Backend extracts user ID from JWT
3. Backend verifies that requested todo's `owner_id` matches JWT's user ID
4. Request proceeds only if ownership matches