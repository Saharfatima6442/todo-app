# Quickstart Guide: In-Memory Todo CLI

## Overview
This guide provides instructions for setting up and running the In-Memory Todo CLI application.

## Prerequisites
- Python 3.13 or higher
- UV package manager

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up the Python environment**
   ```bash
   # Using UV to create and manage the virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   # Or if using pyproject.toml
   uv sync
   ```

## Running the Application

1. **Start the application**
   ```bash
   python src/cli/main.py
   ```

2. **Using the application**
   - The application will display a menu with options to:
     - Add a new todo
     - View all todos
     - Update a todo
     - Delete a todo
     - Mark a todo as complete/incomplete
     - Exit the application

3. **Example workflow**
   ```
   Welcome to the Todo CLI Application!
   
   Menu:
   1. Add Todo
   2. View Todos
   3. Update Todo
   4. Delete Todo
   5. Mark Todo Complete/Incomplete
   6. Exit
   
   Enter your choice: 1
   Enter title: Buy groceries
   Enter description: Milk, eggs, bread
   Todo added successfully with ID: 1
   
   Enter your choice: 2
   ID: 1, Title: Buy groceries, Description: Milk, eggs, bread, Completed: False
   ```

## Running Tests

1. **Run all tests**
   ```bash
   pytest
   ```

2. **Run specific test suites**
   ```bash
   # Unit tests
   pytest tests/unit/
   
   # Integration tests
   pytest tests/integration/
   ```

## Development

1. **Adding new features**
   - Follow the TDD approach as required by the constitution
   - Write tests first, then implement functionality
   - Ensure all code follows clean code principles with proper separation of concerns

2. **Code structure**
   - Place data models in `src/models/`
   - Place business logic in `src/services/`
   - Place CLI interface in `src/cli/`
   - Place utilities in `src/lib/`
   - Place tests in the corresponding `tests/` directories