---
id: 1
title: Generate Todo CLI Tasks
stage: tasks
date_iso: 2025-12-31
surface: agent
model: Qwen Code
feature: in-memory-todo
branch: 001-in-memory-todo
user: Saeed
command: /sp.tasks
labels:
  - tasks
  - todo-app
  - cli
  - implementation
links:
  spec: specs/001-in-memory-todo/spec.md
  plan: specs/001-in-memory-todo/plan.md
  tasks: specs/001-in-memory-todo/tasks.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-in-memory-todo/tasks.md
tests_yaml: []
---

---

description: "Task list template for feature implementation"
---

# Tasks: In-Memory Todo CLI

**Input**: Design documents from `/specs/001-in-memory-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python 3.13+ project with UV dependencies
- [ ] T003 [P] Configure linting and formatting tools (pylint, black, flake8)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create base Todo model in src/models/todo.py
- [ ] T005 [P] Create TodoService in src/services/todo_service.py (depends on T004)
- [ ] T006 Create in-memory storage mechanism for todos
- [ ] T007 Create CLI interface framework in src/cli/main.py
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items to their list with a title and description, assigning a unique ID

**Independent Test**: The application allows users to add a new todo with a title and description, assigns it a unique ID, and displays it in the list of todos.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for add todo functionality in tests/contract/test_add_todo.py
- [ ] T011 [P] [US1] Unit test for Todo model validation in tests/unit/test_todo.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create Todo model with validation in src/models/todo.py (depends on T004)
- [ ] T013 [P] [US1] Create add_todo method in TodoService in src/services/todo_service.py (depends on T005)
- [ ] T014 [US1] Implement add todo CLI command in src/cli/main.py (depends on T007, T005)
- [ ] T015 [US1] Add validation for title and description in src/models/todo.py
- [ ] T016 [US1] Add unique ID assignment logic in src/services/todo_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todos (Priority: P1)

**Goal**: Enable users to view all their todos with ID, title, description, and completion status

**Independent Test**: The application displays all todos with their ID, title, description, and completion status in a clear, readable format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Contract test for view todos functionality in tests/contract/test_view_todos.py
- [ ] T018 [P] [US2] Unit test for get_all_todos method in tests/unit/test_todo_service.py

### Implementation for User Story 2

- [ ] T019 [P] [US2] Create get_all_todos method in TodoService in src/services/todo_service.py (depends on T005)
- [ ] T020 [US2] Implement view todos CLI command in src/cli/main.py (depends on T007, T019)
- [ ] T021 [US2] Add formatting for displaying todos in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo (Priority: P2)

**Goal**: Enable users to update the title and/or description of an existing todo using its ID

**Independent Test**: The application allows users to update the title and/or description of an existing todo using its ID.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US3] Contract test for update todo functionality in tests/contract/test_update_todo.py
- [ ] T023 [P] [US3] Unit test for update_todo method in tests/unit/test_todo_service.py

### Implementation for User Story 3

- [ ] T024 [P] [US3] Create update_todo method in TodoService in src/services/todo_service.py (depends on T005)
- [ ] T025 [US3] Implement update todo CLI command in src/cli/main.py (depends on T007, T024)
- [ ] T026 [US3] Add validation for update operations in src/models/todo.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todo (Priority: P2)

**Goal**: Enable users to delete a todo using its ID

**Independent Test**: The application allows users to delete a todo using its ID, and the todo is removed from the in-memory list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US4] Contract test for delete todo functionality in tests/contract/test_delete_todo.py
- [ ] T028 [P] [US4] Unit test for delete_todo method in tests/unit/test_todo_service.py

### Implementation for User Story 4

- [ ] T029 [P] [US4] Create delete_todo method in TodoService in src/services/todo_service.py (depends on T005)
- [ ] T030 [US4] Implement delete todo CLI command in src/cli/main.py (depends on T007, T029)

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Todo Complete/Incomplete (Priority: P2)

**Goal**: Enable users to toggle the completion status of a todo using its ID

**Independent Test**: The application allows users to toggle the completion status of a todo using its ID.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US5] Contract test for mark complete/incomplete functionality in tests/contract/test_mark_todo.py
- [ ] T032 [P] [US5] Unit test for toggle_completion method in tests/unit/test_todo_service.py

### Implementation for User Story 5

- [ ] T033 [P] [US5] Create mark_complete, mark_incomplete, and toggle_completion methods in TodoService in src/services/todo_service.py (depends on T005)
- [ ] T034 [US5] Implement mark complete/incomplete CLI command in src/cli/main.py (depends on T007, T033)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] Documentation updates in docs/
- [ ] T036 Code cleanup and refactoring
- [ ] T037 Performance optimization across all stories
- [ ] T038 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T039 Security hardening
- [ ] T040 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for add todo functionality in tests/contract/test_add_todo.py"
Task: "Unit test for Todo model validation in tests/unit/test_todo.py"

# Launch all models for User Story 1 together:
Task: "Create Todo model with validation in src/models/todo.py"
Task: "Create add_todo method in TodoService in src/services/todo_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Response Summary

The tasks.md file has been successfully generated for the In-Memory Todo CLI application with 40 tasks organized across 7 phases:

- Setup phase (3 tasks)
- Foundational phase (6 tasks)
- 5 user story phases with priority-based ordering
- Polish & cross-cutting concerns phase (5 tasks)

Each task follows the required checklist format with proper ID, parallel markers where applicable, story labels for user story tasks, and specific file paths. The tasks are organized to enable independent implementation and testing of each user story as required by the specification.