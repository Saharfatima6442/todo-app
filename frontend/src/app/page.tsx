'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import * as todoService from '@/lib/todo-service';
import { Todo } from '@/types/todo';

const TodoPage = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');

  // Load todos on initial render
  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setLoading(true);
    try {
      const data = await todoService.fetchTodos();
      setTodos(data.filter((t): t is Todo => t !== null));
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  // CRUD handlers
  const handleAddTodo = async () => {
    if (!newTodoTitle.trim()) return;
    const added = await todoService.createTodo(newTodoTitle, newTodoDescription);
    setTodos(prev => [...prev, added]);
    setNewTodoTitle('');
    setNewTodoDescription('');
  };

  const handleUpdateTodo = async () => {
    if (!editingTodo) return;
    const updated = await todoService.updateTodo(editingTodo.id, editTitle, editDescription);
    setTodos(prev => prev.map(t => t.id === updated.id ? updated : t));
    setEditingTodo(null);
    setEditTitle('');
    setEditDescription('');
  };

  const handleToggleCompletion = async (id: number) => {
    const updated = await todoService.toggleTodoCompletion(id);
    setTodos(prev => prev.map(t => t.id === updated.id ? updated : t));
  };

  const handleDelete = async (id: number) => {
    await todoService.deleteTodo(id);
    setTodos(prev => prev.filter(t => t.id !== id));
  };

  // Loading screen
  if (loading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;

  // Main Todo UI (without authentication)
  return (
    <div className="container mx-auto py-10 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle>Todo Application (Stable Baseline)</CardTitle>
          <CardDescription>Manage your tasks efficiently - No Authentication Required</CardDescription>
        </CardHeader>
        <CardContent>
          {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">{error}</div>}

          {/* Add Todo */}
          <div className="mb-8 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <Input placeholder="Todo title" value={newTodoTitle} onChange={e => setNewTodoTitle(e.target.value)} />
            </div>
            <div className="md:col-span-1">
              <Input placeholder="Description (optional)" value={newTodoDescription} onChange={e => setNewTodoDescription(e.target.value)} />
            </div>
            <div className="md:col-span-1 flex items-end">
              <Button onClick={handleAddTodo} className="w-full">Add Todo</Button>
            </div>
          </div>

          {/* Todo List */}
          {todos.length === 0 ? (
            <p className="text-gray-500 text-center py-4">No todos yet!</p>
          ) : (
            <div className="space-y-3">
              {todos.map(todo => (
                <Card key={todo.id} className="p-4">
                  <div className="flex items-center space-x-4">
                    <Checkbox id={`complete-${todo.id}`} checked={todo.completed} onCheckedChange={() => handleToggleCompletion(todo.id)} />
                    <div className="flex-1">
                      <div className={`font-medium ${todo.completed ? 'line-through text-gray-500' : ''}`}>{todo.title}</div>
                      {todo.description && <div className={`text-sm ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>{todo.description}</div>}
                    </div>
                    <div className="flex space-x-2">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button variant="outline" size="sm" onClick={() => { setEditingTodo(todo); setEditTitle(todo.title); setEditDescription(todo.description || ''); }}>Edit</Button>
                        </DialogTrigger>
                        <DialogContent className="sm:max-w-[425px]">
                          <DialogHeader>
                            <DialogTitle>Edit Todo</DialogTitle>
                            <DialogDescription>Edit your todo and click save.</DialogDescription>
                          </DialogHeader>
                          <div className="grid gap-4 py-4">
                            <Input value={editTitle} onChange={e => setEditTitle(e.target.value)} />
                            <Input value={editDescription} onChange={e => setEditDescription(e.target.value)} />
                          </div>
                          <DialogFooter>
                            <Button onClick={handleUpdateTodo}>Save changes</Button>
                          </DialogFooter>
                        </DialogContent>
                      </Dialog>
                      <Button variant="destructive" size="sm" onClick={() => handleDelete(todo.id)}>Delete</Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          <div>{todos.filter(t => t.completed).length} of {todos.length} completed</div>
          <Button variant="outline" onClick={() => window.location.reload()}>Refresh</Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default TodoPage;
