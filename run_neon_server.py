#!/usr/bin/env python3
"""
Production startup script for the JWT Authenticated Todo Application with Neon Database Support
"""

import os
import sys
import subprocess
from pathlib import Path
import threading
import time
import requests
import signal
import atexit

def check_server_health(url, timeout=5):
    """Check if the server is responding to health checks"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Starting JWT Authenticated Todo Application...")
    print("📁 Changing to backend directory...")
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("✅ Backend directory confirmed")
    
    # Add src to Python path
    src_path = str(backend_dir / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    print("🔐 Environment variables loaded")
    
    # Check if using database
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"🗄️  Database connection configured: {database_url[:50]}...")
        print("   Using Neon PostgreSQL database")
    else:
        print("💾 Using in-memory storage (data will not persist)")
        print("   To enable database, set DATABASE_URL in your .env file")
    
    print("\n🌐 Starting FastAPI server...")
    print("   API will be available at http://127.0.0.1:8000")
    print("   API docs available at http://127.0.0.1:8000/docs")
    
    # Import and run the app
    try:
        import uvicorn
        from main import app
        
        print("\n✅ Server starting successfully!")
        print("💡 Press Ctrl+C to stop the server\n")
        
        # Run the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False  # Disable reload in production
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()