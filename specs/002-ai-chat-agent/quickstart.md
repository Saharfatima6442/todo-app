# Quickstart Guide: AI Chat Agent with MCP Integration

## Prerequisites
- Python 3.9+
- Node.js 18+
- Neon PostgreSQL database
- Better Auth credentials
- OpenAI API key

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd todo-app
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following:
```env
DATABASE_URL=<your-neon-postgres-url>
BETTER_AUTH_SECRET=<your-better-auth-secret>
OPENAI_API_KEY=<your-openai-api-key>
MCP_SERVER_PORT=8001
```

### 5. Run Migrations
```bash
cd backend
python -m alembic upgrade head
```

### 6. Start the Services
Terminal 1 - MCP Server:
```bash
cd backend
python -m mcp.server
```

Terminal 2 - Main Backend:
```bash
cd backend
python main.py
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

## Usage
1. Visit the frontend at `http://localhost:3000`
2. Authenticate using Better Auth
3. Start chatting with the AI assistant to manage your tasks
4. Examples:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Complete task #1"
   - "Update task #2 to 'buy milk and eggs'"

## Architecture Overview
- **Frontend**: Next.js app with OpenAI ChatKit integration
- **Backend**: FastAPI server with stateless design
- **MCP Server**: Separate service exposing tools for AI agent
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth