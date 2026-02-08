import React, { useState } from 'react';
import { apiFetch } from '../services/api_client';

const AddTodo = ({ onAdd }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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
      
      const response = await apiFetch(`/api/${userId}/todos`, {
        method: 'POST',
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          completed: false
        })
      });
      
      if (response.ok) {
        const newTodo = await response.json();
        onAdd(newTodo); // Notify parent component of the new todo
        setTitle(''); // Clear the form
        setDescription('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add todo');
      }
    } catch (err) {
      setError('Network error occurred');
      console.error('Error adding todo:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-todo">
      <h2>Add New Todo</h2>
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
        
        {error && <div className="error">{error}</div>}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Todo'}
        </button>
      </form>
    </div>
  );
};

export default AddTodo;