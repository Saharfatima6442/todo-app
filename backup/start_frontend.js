// Script to start the Next.js frontend development server
const { spawn } = require('child_process');
const path = require('path');

function startFrontend() {
    const frontendDir = path.join(__dirname, 'frontend');
    
    console.log('Starting Next.js frontend server...');
    console.log('Access the Todo App at: http://localhost:3000');
    
    // Set environment variable for the API base URL
    const env = { ...process.env, NEXT_PUBLIC_API_BASE_URL: 'http://localhost:8000' };
    
    // Start the Next.js development server
    const frontendProcess = spawn('npx', ['next', 'dev'], {
        cwd: frontendDir,
        env: env,
        stdio: 'inherit'
    });
    
    frontendProcess.on('error', (err) => {
        console.error('Error starting frontend:', err.message);
    });
    
    frontendProcess.on('close', (code) => {
        console.log(`Frontend server exited with code ${code}`);
    });
}

startFrontend();