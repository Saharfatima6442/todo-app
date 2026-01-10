'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog';
import { useTodo } from '@/contexts/todo-context';
import { Todo } from '@/types/todo';

const TodoPage = () => {
  const { todos, loading, error, addTodo, updateTodo, toggleCompletion, removeTodo } = useTodo();
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const handleSubmitNewTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    try {
      await addTodo(newTodoTitle, newTodoDescription);
      setNewTodoTitle('');
      setNewTodoDescription('');
    } catch (err) {
      console.error('Error adding todo:', err);
    }
  };

  const handleUpdateTodo = async () => {
    if (!editingTodo) return;

    try {
      await updateTodo(editingTodo.id, editTitle, editDescription);
      setEditingTodo(null);
      setEditTitle('');
      setEditDescription('');
    } catch (err) {
      console.error('Error updating todo:', err);
    }
  };

  const handleEditClick = (todo: Todo) => {
    setEditingTodo(todo);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
  };

  const handleToggleCompletion = async (id: number) => {
    try {
      await toggleCompletion(id);
    } catch (err) {
      console.error('Error toggling completion:', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await removeTodo(id);
    } catch (err) {
      console.error('Error deleting todo:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading todos...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle>Todo Application</CardTitle>
          <CardDescription>Manage your tasks efficiently</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
              Error: {error}
            </div>
          )}

          {/* Add Todo Form */}
          <form onSubmit={handleSubmitNewTodo} className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <Label htmlFor="title">Title</Label>
                <Input
                  id="title"
                  value={newTodoTitle}
                  onChange={(e) => setNewTodoTitle(e.target.value)}
                  placeholder="What needs to be done?"
                  required
                />
              </div>
              <div className="md:col-span-1">
                <Label htmlFor="description">Description</Label>
                <Input
                  id="description"
                  value={newTodoDescription}
                  onChange={(e) => setNewTodoDescription(e.target.value)}
                  placeholder="Add a description (optional)"
                />
              </div>
              <div className="md:col-span-1 flex items-end">
                <Button type="submit" className="w-full">Add Todo</Button>
              </div>
            </div>
          </form>

          {/* Todo List */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Your Todos ({todos.length})</h2>
            
            {todos.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No todos yet. Add one above!</p>
            ) : (
              <div className="space-y-3">
                {todos.map((todo) => (
                  <Card key={todo.id} className="p-4">
                    <div className="flex items-center space-x-4">
                      <Checkbox
                        id={`complete-${todo.id}`}
                        checked={todo.completed}
                        onCheckedChange={() => handleToggleCompletion(todo.id)}
                      />
                      <div className="flex-1">
                        <div className={`font-medium ${todo.completed ? 'line-through text-gray-500' : ''}`}>
                          {todo.title}
                        </div>
                        {todo.description && (
                          <div className={`text-sm ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                            {todo.description}
                          </div>
                        )}
                      </div>
                      <div className="flex space-x-2">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => handleEditClick(todo)}
                            >
                              Edit
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Edit Todo</DialogTitle>
                              <DialogDescription>
                                Make changes to your todo here. Click save when you're done.
                              </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="edit-title" className="text-right">
                                  Title
                                </Label>
                                <Input
                                  id="edit-title"
                                  value={editTitle}
                                  onChange={(e) => setEditTitle(e.target.value)}
                                  className="col-span-3"
                                />
                              </div>
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="edit-description" className="text-right">
                                  Description
                                </Label>
                                <Input
                                  id="edit-description"
                                  value={editDescription}
                                  onChange={(e) => setEditDescription(e.target.value)}
                                  className="col-span-3"
                                />
                              </div>
                            </div>
                            <DialogFooter>
                              <Button type="submit" onClick={handleUpdateTodo}>Save changes</Button>
                            </DialogFooter>
                          </DialogContent>
                        </Dialog>
                        <Button 
                          variant="destructive" 
                          size="sm"
                          onClick={() => handleDelete(todo.id)}
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <div>{todos.filter(t => t.completed).length} of {todos.length} completed</div>
          <Button 
            variant="outline"
            onClick={() => window.location.reload()}
          >
            Refresh
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default TodoPage;