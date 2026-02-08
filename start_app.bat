@echo off
title Todo App Startup

echo Starting Todo App...
echo =====================

REM Start the backend server in a separate window
echo Starting backend server...
start "Todo Backend" cmd /c "cd /d C:\Users\Saeed\OneDrive\Desktop\todo-app && python start_backend.py"

REM Wait a moment for the backend to start
timeout /t 5 /nobreak >nul

REM Start the frontend server in the current window
echo Starting frontend server...
cd /d C:\Users\Saeed\OneDrive\Desktop\todo-app\frontend
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
npx next dev

pause