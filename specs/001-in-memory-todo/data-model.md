# Data Model: In-Memory Todo CLI

## Overview
This document defines the data models for the In-Memory Todo CLI application based on the feature specification.

## Todo Entity

### Fields
- **id** (integer): Unique identifier for the todo item, automatically assigned
- **title** (string): Title of the todo item (required)
- **description** (string): Detailed description of the todo item (optional)
- **completed** (boolean): Completion status of the todo item (default: false)

### Validation Rules
- **id**: Must be unique within the application session
- **title**: Must not be empty or null
- **description**: Can be empty but not null
- **completed**: Must be a boolean value (true/false)

### State Transitions
- **Initial State**: When created, a Todo has `completed = false`
- **Completed State**: When marked complete, `completed` changes to `true`
- **Incomplete State**: When marked incomplete, `completed` changes to `false`

## Todo Service

### Responsibilities
- Manage the collection of Todo items in memory
- Provide methods to add, view, update, delete, and mark todos
- Ensure unique IDs are assigned to each todo
- Validate todo data before operations

### Methods
- **add_todo(title, description)**: Creates a new todo with a unique ID
- **get_all_todos()**: Returns all todos
- **get_todo_by_id(id)**: Returns a specific todo by ID
- **update_todo(id, title, description)**: Updates an existing todo
- **delete_todo(id)**: Removes a todo by ID
- **mark_complete(id)**: Marks a todo as complete
- **mark_incomplete(id)**: Marks a todo as incomplete
- **toggle_completion(id)**: Toggles the completion status of a todo