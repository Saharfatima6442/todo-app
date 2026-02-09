'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { SendHorizonalIcon, BotIcon, UserIcon } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatComponentProps {
  userId: string;
}

const ChatComponent: React.FC<ChatComponentProps> = ({ userId }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant for managing todos. You can ask me to add, list, update, or delete your tasks.',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get the auth token
      const token = localStorage.getItem('jwt_token');

      // Call the chat API
      const response = await fetch('/api/chat/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          user_id: userId,
          message: inputValue,
          conversation_history: messages.map(msg => ({
            role: msg.role,
            content: msg.content,
          })),
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed with status ${response.status}: ${errorText}`);
      }

      const data = await response.json();

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error processing your request: ${error.message || error}`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BotIcon className="h-5 w-5" />
          AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col h-[400px]">
          <ScrollArea className="flex-grow mb-4 pr-4" ref={scrollAreaRef}>
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`flex items-start gap-2 max-w-[80%] ${
                      message.role === 'user' ? 'flex-row-reverse' : ''
                    }`}
                  >
                    {message.role === 'assistant' ? (
                      <div className="bg-blue-100 p-2 rounded-full mt-1">
                        <BotIcon className="h-4 w-4 text-blue-600" />
                      </div>
                    ) : (
                      <div className="bg-gray-100 p-2 rounded-full mt-1">
                        <UserIcon className="h-4 w-4 text-gray-600" />
                      </div>
                    )}
                    <div
                      className={`rounded-lg p-3 ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex items-start gap-2 max-w-[80%]">
                    <div className="bg-blue-100 p-2 rounded-full mt-1">
                      <BotIcon className="h-4 w-4 text-blue-600" />
                    </div>
                    <div className="bg-gray-100 text-gray-800 rounded-lg p-3">
                      Thinking...
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <Button type="submit" disabled={isLoading || !inputValue.trim()}>
              <SendHorizonalIcon className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
};

export default ChatComponent;