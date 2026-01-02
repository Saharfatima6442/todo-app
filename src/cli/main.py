"""
Command-line interface for the todo application.
"""
from src.services.todo_service import TodoService


class TodoCLI:
    """
    Command-line interface for interacting with the todo application.
    """
    
    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*40)
        print("TODO APPLICATION")
        print("="*40)
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Todo Complete/Incomplete")
        print("6. Exit")
        print("="*40)

    def add_todo(self):
        """Add a new todo."""
        print("\n--- Add Todo ---")
        title = input("Enter title: ").strip()
        
        if not title:
            print("Error: Title cannot be empty.")
            return
        
        description = input("Enter description (optional): ").strip()
        if not description:
            description = None
        
        try:
            todo = self.service.add_todo(title, description)
            print(f"Todo added successfully with ID: {todo.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_todos(self):
        """View all todos."""
        print("\n--- View Todos ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No todos found.")
            return
        
        print(f"{'ID':<4} {'Title':<20} {'Description':<30} {'Status':<10}")
        print("-" * 70)
        for todo in todos:
            status = "Complete" if todo.completed else "Incomplete"
            print(f"{todo.id:<4} {todo.title[:19]:<20} {todo.description[:29]:<30} {status:<10}")

    def update_todo(self):
        """Update an existing todo."""
        print("\n--- Update Todo ---")
        try:
            todo_id = int(input("Enter todo ID to update: "))
        except ValueError:
            print("Error: Please enter a valid ID (number).")
            return
        
        # Check if todo exists
        existing_todo = self.service.get_todo_by_id(todo_id)
        if not existing_todo:
            print(f"Error: Todo with ID {todo_id} not found.")
            return
        
        print(f"Current title: {existing_todo.title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()
        
        print(f"Current description: {existing_todo.description}")
        new_description = input("Enter new description (or press Enter to keep current): ").strip()
        
        # Prepare update parameters
        update_params = {}
        if new_title:
            update_params['title'] = new_title
        if new_description:  # Allow empty description
            update_params['description'] = new_description
        
        if not update_params:
            print("No changes provided.")
            return
        
        try:
            updated_todo = self.service.update_todo(todo_id, **update_params)
            if updated_todo:
                print("Todo updated successfully.")
            else:
                print("Error updating todo.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_todo(self):
        """Delete a todo."""
        print("\n--- Delete Todo ---")
        try:
            todo_id = int(input("Enter todo ID to delete: "))
        except ValueError:
            print("Error: Please enter a valid ID (number).")
            return
        
        if self.service.delete_todo(todo_id):
            print(f"Todo with ID {todo_id} deleted successfully.")
        else:
            print(f"Error: Todo with ID {todo_id} not found.")

    def mark_todo_completion(self):
        """Mark a todo as complete or incomplete."""
        print("\n--- Mark Todo Complete/Incomplete ---")
        try:
            todo_id = int(input("Enter todo ID: "))
        except ValueError:
            print("Error: Please enter a valid ID (number).")
            return
        
        # Check current status
        existing_todo = self.service.get_todo_by_id(todo_id)
        if not existing_todo:
            print(f"Error: Todo with ID {todo_id} not found.")
            return
        
        current_status = "Complete" if existing_todo.completed else "Incomplete"
        print(f"Current status: {current_status}")
        
        # Toggle completion status
        if self.service.toggle_completion(todo_id):
            updated_todo = self.service.get_todo_by_id(todo_id)
            new_status = "Complete" if updated_todo.completed else "Incomplete"
            print(f"Todo with ID {todo_id} marked as {new_status}.")
        else:
            print("Error toggling completion status.")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo CLI Application!")
        
        while self.running:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.add_todo()
            elif choice == "2":
                self.view_todos()
            elif choice == "3":
                self.update_todo()
            elif choice == "4":
                self.delete_todo()
            elif choice == "5":
                self.mark_todo_completion()
            elif choice == "6":
                print("Thank you for using the Todo CLI Application!")
                self.running = False
            else:
                print("Invalid choice. Please enter a number between 1-6.")


def main():
    """Main function to run the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()