"""
Test script to verify the todo application functionality
"""
from src.services.todo_service import TodoService


def test_todo_functionality():
    """Test all the main functionality of the todo application."""
    print("Testing Todo Application functionality...")
    
    # Create a service instance
    service = TodoService()
    
    # Test 1: Add a todo
    print("\n1. Testing add todo functionality...")
    todo1 = service.add_todo("Buy groceries", "Milk, eggs, bread")
    print(f"   Added todo: ID={todo1.id}, Title='{todo1.title}', Description='{todo1.description}', Completed={todo1.completed}")
    
    # Test 2: Add another todo
    todo2 = service.add_todo("Walk the dog", "Don't forget the leash")
    print(f"   Added todo: ID={todo2.id}, Title='{todo2.title}', Description='{todo2.description}', Completed={todo2.completed}")
    
    # Test 3: View all todos
    print("\n2. Testing view all todos...")
    all_todos = service.get_all_todos()
    print(f"   Total todos: {len(all_todos)}")
    for todo in all_todos:
        print(f"   - ID={todo.id}, Title='{todo.title}', Completed={todo.completed}")
    
    # Test 4: Get a specific todo
    print("\n3. Testing get todo by ID...")
    retrieved_todo = service.get_todo_by_id(todo1.id)
    if retrieved_todo:
        print(f"   Retrieved todo: ID={retrieved_todo.id}, Title='{retrieved_todo.title}'")
    else:
        print("   Todo not found!")
    
    # Test 5: Update a todo
    print("\n4. Testing update todo...")
    updated_todo = service.update_todo(todo1.id, "Buy groceries and cook dinner", "Milk, eggs, bread, chicken")
    if updated_todo:
        print(f"   Updated todo: ID={updated_todo.id}, Title='{updated_todo.title}', Description='{updated_todo.description}'")
    else:
        print("   Todo not found for update!")
    
    # Test 6: Mark as complete
    print("\n5. Testing mark complete...")
    result = service.mark_complete(todo1.id)
    if result:
        updated_todo = service.get_todo_by_id(todo1.id)
        print(f"   Todo marked complete: ID={updated_todo.id}, Completed={updated_todo.completed}")
    else:
        print("   Failed to mark todo as complete!")
    
    # Test 7: Toggle completion
    print("\n6. Testing toggle completion...")
    result = service.toggle_completion(todo1.id)
    if result:
        updated_todo = service.get_todo_by_id(todo1.id)
        print(f"   Todo completion toggled: ID={updated_todo.id}, Completed={updated_todo.completed}")
    else:
        print("   Failed to toggle todo completion!")
    
    # Test 8: Delete a todo
    print("\n7. Testing delete todo...")
    result = service.delete_todo(todo2.id)
    if result:
        print(f"   Todo with ID {todo2.id} deleted successfully")
    else:
        print(f"   Failed to delete todo with ID {todo2.id}")
    
    # Verify deletion
    all_todos = service.get_all_todos()
    print(f"   Remaining todos after deletion: {len(all_todos)}")
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_todo_functionality()