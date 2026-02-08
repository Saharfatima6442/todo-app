// frontend/src/services/api_client.js

/**
 * API client that automatically attaches JWT to requests
 */
export async function apiFetch(url, options = {}) {
  // Get the JWT token from wherever it's stored (localStorage, cookie, etc.)
  // For this example, we'll assume it's in localStorage
  const token = localStorage.getItem('jwt_token');

  // Construct the full API URL using the base URL from environment
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
  const fullUrl = `${baseUrl}${url}`;

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  // Add authorization header if token exists
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(fullUrl, {
      ...options,
      headers,
    });

    // Handle 401 responses by clearing the token and redirecting to login
    if (response.status === 401) {
      localStorage.removeItem('jwt_token');
      window.location.href = '/login';
      throw new Error('Unauthorized: Please log in again');
    }

    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * Convenience method for GET requests
 */
export async function get(url) {
  const response = await apiFetch(url, { method: 'GET' });
  return response.json();
}

/**
 * Convenience method for POST requests
 */
export async function post(url, data) {
  const response = await apiFetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
  });
  return response.json();
}

/**
 * Convenience method for PUT requests
 */
export async function put(url, data) {
  const response = await apiFetch(url, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  return response.json();
}

/**
 * Convenience method for DELETE requests
 */
export async function del(url) {
  const response = await apiFetch(url, { method: 'DELETE' });
  return response.json();
}