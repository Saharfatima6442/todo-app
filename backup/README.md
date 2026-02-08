# Backup Files

This directory contains duplicate or redundant files that were removed from the main project to eliminate redundancy.

## Files Moved:

1. **start_backend_only.py** - Duplicate of functionality in start_backend.py
   - Purpose: Starts only the backend server
   - Reason for removal: Identical functionality to start_backend.py

2. **start_application.py** - Different approach but similar functionality to start_app.py
   - Purpose: Starts the application with virtual environment setup
   - Reason for removal: Overlapping functionality with start_app.py

3. **start_frontend_detailed.py** - Duplicate of functionality in start_frontend.py
   - Purpose: Starts only the frontend server with more detailed output
   - Reason for removal: Similar functionality to start_frontend.py

4. **start_frontend.js** - JavaScript version of frontend startup
   - Purpose: Alternative way to start the frontend server
   - Reason for removal: Redundant with start_frontend.py

## Preserved Files:

1. **start_app.py** - Starts both backend and frontend servers
2. **start_backend.py** - Starts only the backend server
3. **start_frontend.py** - Starts only the frontend server