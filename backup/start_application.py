#!/usr/bin/env python3
"""
Application startup script for the JWT Authenticated Todo Application
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("Starting JWT Authenticated Todo Application...")
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Check if virtual environment exists, if not create and activate it
    venv_path = backend_dir / ".venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    
    # Activate virtual environment and install dependencies
    if sys.platform.startswith("win"):
        pip_path = venv_path / "Scripts" / "pip.exe"
        uvicorn_path = venv_path / "Scripts" / "uvicorn.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
        uvicorn_path = venv_path / "bin" / "uvicorn"
    
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"])
    
    # Start the FastAPI application
    print("Starting the application...")
    cmd = [str(uvicorn_path), "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    
    # Add environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir / "src")
    
    subprocess.run(cmd, env=env)

if __name__ == "__main__":
    main()