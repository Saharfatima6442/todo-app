import subprocess
import os
import sys
import time

def main():
    print("Starting frontend server...")
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.chdir(frontend_dir)
    
    print(f"Changed to directory: {os.getcwd()}")
    
    # Set environment variable for API base URL
    env = os.environ.copy()
    env["NEXT_PUBLIC_API_BASE_URL"] = "http://localhost:8000"
    
    # Start the Next.js development server
    print("Running: npm run dev")
    process = subprocess.Popen([
        "npm", "run", "dev"
    ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    print(f"Frontend server started with PID: {process.pid}")
    print("Waiting for server to start...")
    
    # Print output from the process
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
            # Look for the line that indicates the server is running
            if "Local:" in output or "ready started server" in output:
                print("\n✅ Frontend server is running!")
                print("Check the above output for the actual URL and port.")
                break
        elif process.poll() is not None:
            print("❌ Frontend server failed to start properly")
            break
    
    # Keep the process running
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nStopping frontend server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()