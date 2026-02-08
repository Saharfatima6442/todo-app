import React, { useState, useEffect } from 'react';
import { apiFetch } from '../services/api_client';

const ViewTodos = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Get the user ID from wherever it's stored (could be from auth context)
      const userId = localStorage.getItem('userId'); // Placeholder - adjust based on your auth implementation
      
      const response = await apiFetch(`/api/${userId}/todos`);
      
      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to fetch todos');
      }
    } catch (err) {
      setError('Network error occurred');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading todos...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="view-todos">
      <h2>Your Todos</h2>
      
      {todos.length === 0 ? (
        <div className="empty-state">No todos found. Add a new todo to get started!</div>
      ) : (
        <ul className="todos-list">
          {todos.map(todo => (
            <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
              <div className="todo-content">
                <h3>{todo.title}</h3>
                {todo.description && <p>{todo.description}</p>}
                <div className="todo-meta">
                  <span>ID: {todo.id}</span>
                  <span>Status: {todo.completed ? 'Completed' : 'Pending'}</span>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ViewTodos;