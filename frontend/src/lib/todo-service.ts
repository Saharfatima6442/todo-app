import { Todo } from '@/types/todo';
import { authProvider } from '@/auth/auth_provider';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Generic fetch helper with auth
 */
const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  console.log('Fetching from URL:', url);

  // Get the auth token
  const token = authProvider.getToken();

  // Add authorization header if token exists
  const authOptions = {
    ...options,
    headers: {
      ...options.headers,
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      'Content-Type': 'application/json',
    }
  };

  const response = await fetch(url, authOptions);

  console.log('Response status:', response.status);

  if (!response.ok) {
    let errorText = '';

    try {
      errorText = await response.text();
      console.error('Raw error response:', errorText);

      const errorData = JSON.parse(errorText);
      console.error('Parsed API Error:', errorData);

      throw new Error(
        errorData.detail ||
        errorData.message ||
        `HTTP error! status: ${response.status}`
      );
    } catch (e) {
      console.error('Non-JSON API Error:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
  }

  return response.json();
};

/**
 * Fetch all todos
 */
export const fetchTodos = async (): Promise<Todo[]> => {
  return fetchWithAuth(`${API_BASE_URL}/todos`);
};

/**
 * Create a new todo
 */
export const createTodo = async (title: string, description?: string): Promise<Todo> => {
  const params = new URLSearchParams({ title });
  if (description) params.append('description', description);
  
  return fetchWithAuth(`${API_BASE_URL}/todos?${params.toString()}`, {
    method: 'POST'
  });
};

/**
 * Update todo
 */
export const updateTodo = async (
  id: number,
  title?: string,
  description?: string
): Promise<Todo> => {
  const params = new URLSearchParams();
  if (title) params.append('title', title);
  if (description) params.append('description', description);
  
  const queryString = params.toString();
  const url = queryString ? `${API_BASE_URL}/todos/${id}?${queryString}` : `${API_BASE_URL}/todos/${id}`;
  
  return fetchWithAuth(url, {
    method: 'PUT'
  });
};

/**
 * Toggle completion
 */
export const toggleTodoCompletion = async (id: number): Promise<Todo> => {
  return fetchWithAuth(`${API_BASE_URL}/todos/${id}/toggle`, {
    method: 'PATCH',
  });
};

/**
 * Delete todo
 */
export const deleteTodo = async (id: number): Promise<void> => {
  await fetchWithAuth(`${API_BASE_URL}/todos/${id}`, {
    method: 'DELETE'
  });
};
