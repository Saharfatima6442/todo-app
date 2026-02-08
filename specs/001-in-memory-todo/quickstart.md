# Quickstart: JWT Authenticated Todo Application

## Overview
This guide provides a quick start to set up and run the JWT authenticated todo application with Better Auth integration.

## Prerequisites
- Python 3.11+
- Node.js 16+ (for frontend)
- pip and npm/yarn package managers
- Docker and docker-compose (optional, for containerized deployment)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-app
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
# Or if using pyproject.toml
poetry install
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
# Or if using yarn
yarn install
```

### 4. Configure Environment Variables
Create `.env` files in both backend and frontend directories with the same `BETTER_AUTH_SECRET`:

**Backend (.env):**
```env
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
DATABASE_URL=sqlite:///./todo_app.db  # if using persistent storage later
```

**Frontend (.env):**
```env
VITE_BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
VITE_API_BASE_URL=http://localhost:8000
```

### 5. Run the Applications

#### Option A: Separate Terminals
```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

#### Option B: Using Docker Compose
```bash
docker-compose up --build
```

### 6. Verify Setup
1. Visit the frontend application (usually at http://localhost:3000)
2. Register/login using the Better Auth interface
3. Create a todo item
4. Verify that the todo is created and accessible only to the authenticated user

## API Usage Examples

### Authenticating
1. User logs in via Better Auth frontend components
2. JWT token is automatically stored and attached to API requests

### Creating a Todo
```javascript
// This is handled automatically by the frontend API client
const response = await fetch('/api/todos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${jwtToken}`  // Added automatically
  },
  body: JSON.stringify({
    title: 'Sample Todo',
    description: 'A sample todo item'
  })
});
```

### Retrieving Todos
```javascript
// Todos are filtered by authenticated user automatically
const response = await fetch('/api/todos', {
  headers: {
    'Authorization': `Bearer ${jwtToken}`  // Added automatically
  }
});
```

## Troubleshooting

### Common Issues

1. **JWT Validation Errors**
   - Ensure `BETTER_AUTH_SECRET` is identical in both frontend and backend
   - Check that JWT is properly formatted in Authorization header

2. **Cross-Origin Issues**
   - Verify CORS settings in backend
   - Ensure frontend and backend URLs are properly configured

3. **User Isolation Not Working**
   - Confirm that all API endpoints validate JWT and enforce ownership
   - Check that `owner_id` is properly set when creating todos

### Useful Commands
```bash
# Check backend API status
curl -H "Authorization: Bearer <valid-jwt-token>" http://localhost:8000/api/health

# Decode JWT to inspect contents
npm install -g jwt-decode
echo "<jwt-token>" | jwt-decode
```

## Next Steps
- Explore the API documentation at `/docs` endpoint
- Review the authentication flow in the frontend code
- Customize the UI components to match your design requirements
- Add additional user roles or permissions as needed