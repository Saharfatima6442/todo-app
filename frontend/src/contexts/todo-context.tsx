'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Todo } from '@/types/todo';
import { fetchTodos, createTodo, updateTodo, toggleTodoCompletion, deleteTodo } from '@/lib/todo-service';

type TodoContextType = {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  addTodo: (title: string, description?: string) => Promise<void>;
  updateTodo: (id: number, title?: string, description?: string) => Promise<void>;
  toggleCompletion: (id: number) => Promise<void>;
  removeTodo: (id: number) => Promise<void>;
  refreshTodos: () => Promise<void>;
};

const TodoContext = createContext<TodoContextType | undefined>(undefined);

export const TodoProvider = ({ children }: { children: ReactNode }) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Load todos on initial render
  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTodos = await fetchTodos();
      setTodos(fetchedTodos);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while fetching todos');
      console.error('Error loading todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (title: string, description?: string) => {
    try {
      const newTodo = await createTodo(title, description);
      setTodos(prev => [...prev, newTodo]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while adding todo');
      console.error('Error adding todo:', err);
      throw err;
    }
  };

  const updateTodoLocally = async (id: number, title?: string, description?: string) => {
    try {
      const updatedTodo = await updateTodo(id, title, description);
      setTodos(prev => prev.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while updating todo');
      console.error('Error updating todo:', err);
      throw err;
    }
  };

  const toggleCompletion = async (id: number) => {
    try {
      const updatedTodo = await toggleTodoCompletion(id);
      setTodos(prev => prev.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while toggling completion');
      console.error('Error toggling completion:', err);
      throw err;
    }
  };

  const removeTodo = async (id: number) => {
    try {
      await deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while deleting todo');
      console.error('Error deleting todo:', err);
      throw err;
    }
  };

  const refreshTodos = async () => {
    await loadTodos();
  };

  return (
    <TodoContext.Provider
      value={{
        todos,
        loading,
        error,
        addTodo,
        updateTodo: updateTodoLocally,
        toggleCompletion,
        removeTodo,
        refreshTodos,
      }}
    >
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => {
  const context = useContext(TodoContext);
  if (context === undefined) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
};