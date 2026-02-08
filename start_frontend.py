"""
Script to start the Next.js frontend development server
"""
import subprocess
import os
import sys
import time

def start_frontend():
    """Start the Next.js development server"""
    frontend_dir = os.path.join(os.getcwd(), "frontend")

    if not os.path.exists(frontend_dir):
        print("Error: Frontend directory not found!")
        return

    print("Starting Next.js frontend server...")
    print("Changing to frontend directory:", frontend_dir)

    # Set environment variable for the API base URL
    env = os.environ.copy()
    env["NEXT_PUBLIC_API_BASE_URL"] = "http://localhost:8000"

    # Change to frontend directory and run the dev server
    os.chdir(frontend_dir)

    print("Running: npm run dev")
    print("Access the Todo App at: http://localhost:3000")

    try:
        # Start the Next.js development server
        result = subprocess.run(["npm", "run", "dev"], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting frontend: {e}")
    except KeyboardInterrupt:
        print("\nFrontend server stopped by user.")

if __name__ == "__main__":
    start_frontend()