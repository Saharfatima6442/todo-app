# Todo AI Chatbot

An AI-powered chat interface for managing todos using natural language processing.

## Features

- Natural language processing for todo management
- Conversation history persistence
- Secure user authentication
- MCP (Model Context Protocol) integration for AI tool usage
- Real-time chat interface with confirmation for destructive actions

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: React with OpenAI ChatKit
- **Database**: Neon PostgreSQL
- **ORM**: SQLModel
- **AI Framework**: OpenAI Agents SDK style logic
- **MCP Server**: Official MCP SDK
- **Authentication**: Better Auth

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+
- Neon PostgreSQL database
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy `.env.example` to `.env` and fill in values):
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_better_auth_secret
OPENAI_API_KEY=your_openai_api_key
TODO_API_BASE_URL=http://localhost:8000/api
```

## API Endpoints

- `POST /api/{user_id}/chat` - Chat endpoint for AI interactions
- `GET /api/{user_id}/conversations` - Get user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get specific conversation details

## Architecture

The application follows a stateless design where:

- All conversation history is stored in the database
- The AI agent uses MCP tools for all todo operations
- Authentication is handled via Better Auth
- The frontend integrates with ChatKit for the chat interface

## MCP Tools

The AI agent has access to the following tools via MCP:

- `add_task`: Add a new task
- `list_tasks`: List all tasks
- `complete_task`: Mark a task as complete
- `delete_task`: Delete a task
- `update_task`: Update a task

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Specify license here]