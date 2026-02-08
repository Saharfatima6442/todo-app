/*
 * ChatInterface component for integrating with OpenAI ChatKit
 */
import { useState, useEffect } from 'react';
import { useChat } from 'ai/react';

const ChatInterface = ({ userId, initialConversationId = null }) => {
  const [conversationId, setConversationId] = useState(initialConversationId);
  const [confirmationNeeded, setConfirmationNeeded] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);
  const [availableConversations, setAvailableConversations] = useState([]);

  // Using the useChat hook from Vercel AI SDK
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    setMessages,
    isLoading,
    error
  } = useChat({
    body: {
      user_id: userId,
      ...(conversationId ? { conversation_id: conversationId } : {})
    },
    onResponse: (response) => {
      // Handle response from the backend
      if (response.headers.get('content-type')?.includes('application/json')) {
        response.json().then(data => {
          if (data.conversation_id && !conversationId) {
            setConversationId(data.conversation_id);
          }

          // Check if confirmation is needed for any tool calls
          if (data.tool_calls && data.tool_calls.length > 0) {
            const confirmationRequired = data.tool_calls.some(call =>
              ['complete_task', 'delete_task', 'update_task'].includes(call.name)
            );

            if (confirmationRequired) {
              setConfirmationNeeded(true);
              setPendingAction(data.tool_calls);
            }
          }
        });
      }
    }
  });

  // Load conversation history when component mounts or conversationId changes
  useEffect(() => {
    if (conversationId) {
      loadConversationHistory();
    }
  }, [conversationId]);

  // Load conversation history from backend
  const loadConversationHistory = async () => {
    try {
      const response = await fetch(`/api/${userId}/conversations/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}` // Assuming auth token is stored
        }
      });

      if (response.ok) {
        const data = await response.json();
        // Set the messages to show conversation history
        setMessages(data.messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          content: msg.content
        })));
      }
    } catch (err) {
      console.error('Error loading conversation history:', err);
    }
  };

  // Load available conversations for the user
  useEffect(() => {
    loadAvailableConversations();
  }, []);

  const loadAvailableConversations = async () => {
    try {
      const response = await fetch(`/api/${userId}/conversations`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableConversations(data.conversations);
      }
    } catch (err) {
      console.error('Error loading conversations:', err);
    }
  };

  // Handle conversation selection
  const handleSelectConversation = (selectedId) => {
    setConversationId(selectedId);
    // Reset messages to show the selected conversation
    setMessages([]);
  };

  // Handle sending a confirmation
  const handleConfirm = () => {
    if (pendingAction) {
      // Send confirmation to backend
      fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: 'yes',
          conversation_id: conversationId,
        }),
      })
      .then(response => response.json())
      .then(data => {
        setConfirmationNeeded(false);
        setPendingAction(null);
      })
      .catch(error => {
        console.error('Error confirming action:', error);
        setConfirmationNeeded(false);
        setPendingAction(null);
      });
    }
  };

  // Handle declining an action
  const handleDecline = () => {
    setConfirmationNeeded(false);
    setPendingAction(null);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Todo Assistant</h2>
        {conversationId && <span className="conversation-id">Session: {conversationId.substring(0, 8)}...</span>}

        {/* Conversation selector */}
        <div className="conversation-selector">
          <select
            value={conversationId || ''}
            onChange={(e) => handleSelectConversation(e.target.value)}
            className="conversation-dropdown"
          >
            <option value="">Select a conversation</option>
            {availableConversations.map(conv => (
              <option key={conv.id} value={conv.id}>
                {conv.title || `Conversation ${conv.created_at}`}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              Thinking...
            </div>
          </div>
        )}

        {error && (
          <div className="message error">
            <div className="message-content">
              Error: {error.message}
            </div>
          </div>
        )}

        {confirmationNeeded && (
          <div className="message confirmation-prompt">
            <div className="message-content">
              <p>To proceed with this action, I need your confirmation. Would you like me to continue?</p>
              <div className="confirmation-buttons">
                <button onClick={handleConfirm} className="btn btn-confirm">Yes, proceed</button>
                <button onClick={handleDecline} className="btn btn-decline">No, cancel</button>
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Ask me to add, list, complete, or delete tasks..."
          disabled={isLoading || confirmationNeeded}
        />
        <button type="submit" disabled={isLoading || confirmationNeeded}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;