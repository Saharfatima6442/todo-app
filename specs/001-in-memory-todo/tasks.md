# Tasks: In-Memory Todo CLI with Web Support

**Feature**: In-Memory Todo CLI with Web Support
**Branch**: `001-in-memory-todo`
**Generated from**: specs/001-in-memory-todo/spec.md, specs/001-in-memory-todo/plan.md, specs/001-in-memory-todo/data-model.md

## Overview

This document outlines the implementation tasks for building a Python console-based todo application with in-memory storage that also supports web access. The application will have both CLI and web interfaces with JWT authentication for web access.

## Phase 1: Setup

Initialize the project structure and configure shared dependencies.

- [ ] T001 Create backend directory structure: backend/src/{models,services,middleware,api}
- [ ] T002 Create frontend directory structure: frontend/src/{components,pages,services,auth}
- [ ] T003 Initialize backend requirements.txt with FastAPI, PyJWT, python-multipart, and python-dotenv
- [ ] T004 Initialize frontend package.json with necessary dependencies for React, Next.js, and authentication
- [ ] T005 Create shared environment configuration for BETTER_AUTH_SECRET
- [ ] T006 Set up project root with main.py for CLI and src/api/todo_api.py for web API
- [ ] T007 Configure gitignore for both backend and frontend

## Phase 2: Foundational Components

Implement foundational components that all user stories depend on.

- [ ] T010 [P] Implement JWT utility functions in backend/src/utils/jwt_handler.py
- [ ] T011 [P] Create authentication middleware in backend/src/middleware/jwt_auth.py with CORS support
- [ ] T012 [P] Create Todo model in backend/src/models/todo.py with owner_id field
- [ ] T013 [P] Create User model representation based on JWT claims
- [ ] T014 [P] Create basic API dependency handlers in backend/src/api/deps.py
- [ ] T015 [P] Create frontend API client with JWT attachment in frontend/src/services/api_client.js
- [ ] T016 [P] Create frontend auth provider in frontend/src/auth/auth_provider.js
- [ ] T017 Configure shared BETTER_AUTH_SECRET in both frontend and backend environments
- [ ] T018 [P] Create in-memory storage service in backend/src/services/storage_service.py
- [ ] T019 [P] Create todo service with ownership enforcement in backend/src/services/todo_service.py
- [ ] T020 [P] Configure CORS middleware in backend/src/api/todo_api.py to allow frontend origin

## Phase 3: User Story 1 - Add Todo (Priority: P1)

As a user, I want to add new todo items to my list so that I can keep track of tasks I need to complete.

**Independent Test**: The application allows users to add a new todo with a title and description, assigns it a unique ID, and displays it in the list of todos.

**Acceptance Scenarios**:
1. Given I am at the main menu, When I select the "Add Todo" option and enter a title and description, Then a new todo is created with a unique ID and added to the in-memory list.
2. Given I have entered a title and description for a new todo, When I submit the form, Then I see a confirmation message and the new todo appears in the list when I view all todos.

- [ ] T021 [US1] Create API endpoint for adding todos in backend/src/api/v1/endpoints/todos.py
- [ ] T022 [US1] Implement JWT validation in add todo endpoint
- [ ] T023 [US1] Implement ownership assignment in add todo endpoint (set owner_id from JWT)
- [ ] T024 [US1] Add character validation for title (1-100 chars) and description (up to 500 chars)
- [ ] T025 [US1] Create frontend component for adding todos in frontend/src/components/AddTodo.jsx
- [ ] T026 [US1] Connect frontend add todo component to authenticated API client
- [ ] T027 [US1] Implement error handling for add todo operation
- [ ] T028 [US1] Add tests for add todo functionality in backend/tests/test_todos.py
- [ ] T029 [US1] Implement CLI command for adding todos in src/cli/main.py

## Phase 4: User Story 2 - View Todos (Priority: P1)

As a user, I want to view all my todos so that I can see what tasks I need to complete.

**Independent Test**: The application displays all todos with their ID, title, description, and completion status in a clear, readable format.

**Acceptance Scenarios**:
1. Given I have added one or more todos, When I select the "View Todos" option, Then all todos are displayed with their ID, title, description, and completion status.
2. Given I have no todos in the system, When I select the "View Todos" option, Then I see a message indicating that there are no todos to display.

- [ ] T030 [US2] Create API endpoint for viewing todos in backend/src/api/v1/endpoints/todos.py
- [ ] T031 [US2] Implement JWT validation in view todos endpoint
- [ ] T032 [US2] Implement ownership filtering in view todos endpoint (only return user's todos)
- [ ] T033 [US2] Create frontend component for viewing todos in frontend/src/components/ViewTodos.jsx
- [ ] T034 [US2] Connect frontend view todos component to authenticated API client
- [ ] T035 [US2] Implement empty state handling for no todos
- [ ] T036 [US2] Add tests for view todos functionality in backend/tests/test_todos.py
- [ ] T037 [US2] Implement CLI command for viewing todos in src/cli/main.py

## Phase 5: User Story 3 - Update Todo (Priority: P2)

As a user, I want to update the title and/or description of an existing todo so that I can keep my task information accurate.

**Independent Test**: The application allows users to update the title and/or description of an existing todo using its ID.

**Acceptance Scenarios**:
1. Given I have a list of todos, When I select the "Update Todo" option and provide a valid todo ID along with new title and/or description, Then the todo is updated with the new information.
2. Given I attempt to update a todo with an invalid ID, When I submit the update request, Then I receive an error message indicating that the todo was not found.

- [ ] T040 [US3] Create API endpoint for updating todos in backend/src/api/v1/endpoints/todos.py
- [ ] T041 [US3] Implement JWT validation in update todo endpoint
- [ ] T042 [US3] Implement ownership verification in update todo endpoint (ensure user owns the todo)
- [ ] T043 [US3] Add character validation for title (1-100 chars) and description (up to 500 chars)
- [ ] T044 [US3] Create frontend component for updating todos in frontend/src/components/UpdateTodo.jsx
- [ ] T045 [US3] Connect frontend update todo component to authenticated API client
- [ ] T046 [US3] Implement error handling for update todo operation (invalid ID, unauthorized)
- [ ] T047 [US3] Add tests for update todo functionality in backend/tests/test_todos.py
- [ ] T048 [US3] Implement CLI command for updating todos in src/cli/main.py

## Phase 6: User Story 4 - Delete Todo (Priority: P2)

As a user, I want to delete a todo so that I can remove tasks that are no longer relevant.

**Independent Test**: The application allows users to delete a todo using its ID, and the todo is removed from the in-memory list.

**Acceptance Scenarios**:
1. Given I have a list of todos, When I select the "Delete Todo" option and provide a valid todo ID, Then the todo is removed from the list.
2. Given I attempt to delete a todo with an invalid ID, When I submit the delete request, Then I receive an error message indicating that the todo was not found.

- [ ] T050 [US4] Create API endpoint for deleting todos in backend/src/api/v1/endpoints/todos.py
- [ ] T051 [US4] Implement JWT validation in delete todo endpoint
- [ ] T052 [US4] Implement ownership verification in delete todo endpoint (ensure user owns the todo)
- [ ] T053 [US4] Create frontend component for deleting todos in frontend/src/components/DeleteTodo.jsx
- [ ] T054 [US4] Connect frontend delete todo component to authenticated API client
- [ ] T055 [US4] Implement error handling for delete todo operation (invalid ID, unauthorized)
- [ ] T056 [US4] Add tests for delete todo functionality in backend/tests/test_todos.py
- [ ] T057 [US4] Implement CLI command for deleting todos in src/cli/main.py

## Phase 7: User Story 5 - Mark Todo Complete/Incomplete (Priority: P2)

As a user, I want to mark a todo as complete or incomplete so that I can track my progress.

**Independent Test**: The application allows users to toggle the completion status of a todo using its ID.

**Acceptance Scenarios**:
1. Given I have a list of todos, When I select the "Mark Complete/Incomplete" option and provide a valid todo ID, Then the completion status of the todo is toggled.
2. Given I attempt to mark a todo with an invalid ID, When I submit the request, Then I receive an error message indicating that the todo was not found.

- [ ] T060 [US5] Create API endpoint for toggling todo completion in backend/src/api/v1/endpoints/todos.py
- [ ] T061 [US5] Implement JWT validation in toggle completion endpoint
- [ ] T062 [US5] Implement ownership verification in toggle completion endpoint (ensure user owns the todo)
- [ ] T063 [US5] Create frontend component for toggling todo completion in frontend/src/components/ToggleTodoCompletion.jsx
- [ ] T064 [US5] Connect frontend toggle completion component to authenticated API client
- [ ] T065 [US5] Implement error handling for toggle completion operation (invalid ID, unauthorized)
- [ ] T066 [US5] Add tests for toggle completion functionality in backend/tests/test_todos.py
- [ ] T067 [US5] Implement CLI command for marking todos complete/incomplete in src/cli/main.py

## Phase 8: CLI Interface Implementation

Implement the console-based user interface as specified in the original spec.

- [ ] T070 [P] Implement main CLI menu in src/cli/main.py
- [ ] T071 [P] Implement CLI input validation and error handling
- [ ] T072 [P] Create CLI helper functions for displaying todos in a formatted way
- [ ] T073 [P] Add CLI configuration to main.py to run CLI interface
- [ ] T074 [P] Add CLI tests in tests/test_cli.py

## Phase 9: Security & Validation

Implement security measures and validation checks.

- [ ] T080 Configure Better Auth to issue JWTs with required claims (sub, email, iat, exp)
- [ ] T081 Implement standardized error responses for authentication failures
- [ ] T082 Implement standardized error responses for authorization failures
- [ ] T083 Add rate limiting to prevent abuse of authentication endpoints
- [ ] T084 Implement token refresh mechanism for frontend
- [ ] T085 Add comprehensive logging for authentication events
- [ ] T086 Add tests for authentication edge cases in backend/tests/test_auth.py

## Phase 10: Polish & Cross-Cutting Concerns

Final touches and cross-cutting concerns.

- [ ] T090 Create main application entry point for backend in backend/main.py
- [ ] T091 Create main application entry point for frontend in frontend/src/index.js
- [ ] T092 Implement graceful error handling throughout the application
- [ ] T093 Add comprehensive documentation for API endpoints
- [ ] T094 Create health check endpoint in backend/src/api/v1/endpoints/health.py
- [ ] T095 Add comprehensive tests for all user stories in backend/tests/integration/
- [ ] T096 Create README with setup and usage instructions
- [ ] T097 Perform end-to-end testing of all user stories
- [ ] T098 Conduct security review of JWT implementation
- [ ] T099 Optimize performance based on defined goals (<200ms auth verification)
- [ ] T100 Update start scripts to properly coordinate frontend and backend startup

## Dependencies

- User Story 1 (Add Todo) has no dependencies
- User Story 2 (View Todos) has no dependencies
- User Story 3 (Update Todo) depends on User Story 1 (need to have todos to update)
- User Story 4 (Delete Todo) depends on User Story 1 (need to have todos to delete)
- User Story 5 (Mark Complete/Incomplete) depends on User Story 1 (need to have todos to mark)

## Parallel Execution Examples

For each user story, the following tasks can be executed in parallel:
- API endpoint implementation
- Frontend component development
- CLI command implementation
- Related tests creation

## Implementation Strategy

1. **MVP Scope**: Complete User Story 1 (Add Todo) and User Story 2 (View Todos) with basic JWT authentication and CLI functionality
2. **Incremental Delivery**: Add remaining user stories in priority order (P1, P2)
3. **Security First**: Implement authentication and authorization before business logic
4. **Test Continuously**: Add tests alongside implementation for each user story