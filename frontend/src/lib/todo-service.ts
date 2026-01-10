/**
 * Service to interact with the Todo API
 */
import { Todo } from '@/types/todo';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Fetch all todos from the API
 */
export const fetchTodos = async (): Promise<Todo[]> => {
  const response = await fetch(`${API_BASE_URL}/todos`);
  if (!response.ok) {
    throw new Error('Failed to fetch todos');
  }
  return response.json();
};

/**
 * Create a new todo
 */
export const createTodo = async (title: string, description?: string): Promise<Todo> => {
  const response = await fetch(`${API_BASE_URL}/todos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: 0, title, description, completed: false }), // id will be assigned by backend
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create todo');
  }
  
  return response.json();
};

/**
 * Update an existing todo
 */
export const updateTodo = async (id: number, title?: string, description?: string): Promise<Todo> => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, description }),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to update todo');
  }
  
  return response.json();
};

/**
 * Toggle the completion status of a todo
 */
export const toggleTodoCompletion = async (id: number): Promise<Todo> => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}/toggle`, {
    method: 'PATCH',
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to toggle todo completion');
  }
  
  return response.json();
};

/**
 * Delete a todo
 */
export const deleteTodo = async (id: number): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to delete todo');
  }
};