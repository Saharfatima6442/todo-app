# Todo App - Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Running the Application Locally

#### Option 1: Using the start scripts (Recommended)

1. **Start the backend server:**
   ```bash
   python start_backend.py
   ```

2. **In a new terminal, start the frontend:**
   ```bash
   cd frontend
   NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 npm run dev
   ```

#### Option 2: Using the combined start script

1. **Run both servers together:**
   ```bash
   python start_app.py
   ```

#### Option 3: Using the batch file (Windows)

1. **Run the batch file:**
   ```bash
   start_app.bat
   ```

### Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: URL of the backend API (default: http://127.0.0.1:8000)

## Production Deployment

### Using Docker

1. **Build and run with docker-compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend API docs: http://localhost:8000/docs

### Manual Deployment

#### Backend (FastAPI)

1. **Deploy the Python application:**
   - Install dependencies: `pip install -r requirements.txt`
   - Run with a production ASGI server like uvicorn with gunicorn:
     ```bash
     gunicorn src.api.todo_api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
     ```

#### Frontend (Next.js)

1. **Build the application:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Start the production server:**
   ```bash
   npm start
   ```

3. **Or export as static files (if using static export):**
   ```bash
   npm run export
   ```

## API Documentation

The backend API provides the following endpoints:

- `GET /` - Health check
- `GET /todos` - Get all todos
- `GET /todos/{id}` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `PATCH /todos/{id}/toggle` - Toggle completion status
- `DELETE /todos/{id}` - Delete a todo

## Architecture

The application follows a clean architecture pattern:

- **Models** (`src/models/`): Data structures
- **Services** (`src/services/`): Business logic
- **API** (`src/api/`): API endpoints
- **Frontend** (`frontend/`): Next.js application with:
  - Components (`frontend/src/components/`)
  - Contexts (`frontend/src/contexts/`)
  - Services (`frontend/src/lib/`)
  - Types (`frontend/src/types/`)

## Troubleshooting

### Common Issues

1. **Frontend can't connect to backend:**
   - Ensure the backend is running on the correct port (8000)
   - Check that `NEXT_PUBLIC_API_BASE_URL` is set correctly

2. **Backend server won't start:**
   - Verify Python dependencies are installed
   - Check that port 8000 is available

3. **Frontend build fails:**
   - Ensure Node.js and npm are properly installed
   - Try clearing npm cache: `npm cache clean --force`

### Testing the Backend

Run the test script to verify the backend is working:
```bash
python test_backend.py
```

## Scaling Considerations

For production deployments, consider:

- Using a proper database instead of in-memory storage
- Adding authentication and authorization
- Implementing proper logging
- Adding monitoring and alerting
- Using a reverse proxy (nginx) in front of the services
- Setting up a proper CI/CD pipeline