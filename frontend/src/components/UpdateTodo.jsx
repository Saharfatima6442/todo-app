import React, { useState } from 'react';
import { apiFetch } from '../services/api_client';

const UpdateTodo = ({ todo, onUpdate }) => {
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description || '');
  const [completed, setCompleted] = useState(todo.completed);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Get the user ID from wherever it's stored (could be from auth context)
      const userId = localStorage.getItem('userId'); // Placeholder - adjust based on your auth implementation
      
      const response = await apiFetch(`/api/${userId}/todos/${todo.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          completed: completed
        })
      });
      
      if (response.ok) {
        const updatedTodo = await response.json();
        onUpdate(updatedTodo); // Notify parent component of the updated todo
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('Network error occurred');
      console.error('Error updating todo:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="update-todo">
      <h3>Update Todo</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter todo title (1-100 characters)"
            maxLength="100"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter todo description (up to 500 characters)"
            maxLength="500"
          />
        </div>
        
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
            />
            Mark as completed
          </label>
        </div>
        
        {error && <div className="error">{error}</div>}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Updating...' : 'Update Todo'}
        </button>
      </form>
    </div>
  );
};

export default UpdateTodo;