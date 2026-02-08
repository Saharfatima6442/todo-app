import { Todo } from '@/types/todo';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Generic fetch helper without auth
 */
const fetchWithoutAuth = async (url: string, options: RequestInit = {}) => {
  console.log('Fetching from URL:', url);

  const response = await fetch(url, options);

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
  return fetchWithoutAuth(`${API_BASE_URL}/todos`);
};

/**
 * Create a new todo
 * FIXED: Using query params instead of JSON body
 */
export const createTodo = async (title: string, description?: string): Promise<Todo> => {

  const url = new URL(`${API_BASE_URL}/todos`);

  url.searchParams.append("title", title);

  if (description) {
    url.searchParams.append("description", description);
  }

  return fetchWithoutAuth(url.toString(), {
    method: 'POST'
  });
};

/**
 * Update todo
 * FIXED: Using query params instead of JSON body
 */
export const updateTodo = async (
  id: number,
  title?: string,
  description?: string
): Promise<Todo> => {

  const url = new URL(`${API_BASE_URL}/todos/${id}`);

  if (title) url.searchParams.append("title", title);
  if (description) url.searchParams.append("description", description);

  return fetchWithoutAuth(url.toString(), {
    method: 'PUT'
  });
};

/**
 * Toggle completion
 */
export const toggleTodoCompletion = async (id: number): Promise<Todo> => {
  return fetchWithoutAuth(`${API_BASE_URL}/todos/${id}/toggle`, {
    method: 'PATCH',
  });
};

/**
 * Delete todo
 */
export const deleteTodo = async (id: number): Promise<void> => {
  await fetchWithoutAuth(`${API_BASE_URL}/todos/${id}`, {
    method: 'DELETE'
  });
};
