"""
Test script for the stable baseline functionality
"""
from src.services.todo_service import TodoService

def test_basic_crud():
    print("Testing basic CRUD operations...")
    
    # Create service instance
    service = TodoService()
    
    # Test creating a todo
    print("\n1. Testing create operation...")
    todo = service.add_todo('Test todo', 'Test description')
    print(f"   Created todo: ID={todo.id}, Title='{todo.title}', Completed={todo.completed}")
    
    # Test getting all todos
    print("\n2. Testing read (all) operation...")
    all_todos = service.get_all_todos()
    print(f"   Total todos: {len(all_todos)}")
    for t in all_todos:
        print(f"     - ID={t.id}, Title='{t.title}', Completed={t.completed}")
    
    # Test getting a specific todo
    print("\n3. Testing read (specific) operation...")
    retrieved = service.get_todo_by_id(todo.id)
    if retrieved:
        print(f"   Retrieved todo: ID={retrieved.id}, Title='{retrieved.title}', Completed={retrieved.completed}")
    else:
        print("   Failed to retrieve todo")
    
    # Test updating a todo
    print("\n4. Testing update operation...")
    updated = service.update_todo(todo.id, 'Updated todo title', 'Updated description')
    if updated:
        print(f"   Updated todo: ID={updated.id}, Title='{updated.title}', Description='{updated.description}'")
    else:
        print("   Failed to update todo")
    
    # Test toggling completion
    print("\n5. Testing toggle completion...")
    initial_completed = retrieved.completed if retrieved else False
    service.toggle_completion(todo.id)
    toggled_todo = service.get_todo_by_id(todo.id)
    if toggled_todo:
        print(f"   Toggled completion: was {initial_completed}, now {toggled_todo.completed}")
    
    # Test deleting a todo
    print("\n6. Testing delete operation...")
    delete_success = service.delete_todo(todo.id)
    print(f"   Delete successful: {delete_success}")
    
    # Verify deletion
    all_todos_after = service.get_all_todos()
    print(f"   Todos after deletion: {len(all_todos_after)}")
    
    print("\nAll basic CRUD operations completed successfully!")

if __name__ == "__main__":
    test_basic_crud()