# Connecting to Neon PostgreSQL Database

This guide explains how to connect your Todo application to a Neon PostgreSQL database.

## Setting Up Neon Database

1. Go to [Neon Console](https://console.neon.tech/) and create an account
2. Create a new project
3. Once created, go to the project dashboard
4. Copy the connection string from the "Connection Details" section

## Configuring the Application

1. Make a copy of the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder with your actual Neon connection string:
   ```bash
   # Example:
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

3. Set your JWT secret:
   ```bash
   BETTER_AUTH_SECRET=77d558d953953fc76c9f7d4164c8caefc0d12c105c42d68538ad7d685ff9efed
   ```

## Running with Neon Database

Once you've configured the DATABASE_URL in your .env file, the application will automatically switch from in-memory storage to using the Neon database when you restart the application.

## Testing the Connection

To verify that your application is connected to Neon:

1. Add a todo item via the API
2. Check your Neon database to confirm the data was stored
3. Restart the application - your data should persist

## Local Development vs Production

- When `DATABASE_URL` is not set in environment variables, the app uses in-memory storage (ideal for development)
- When `DATABASE_URL` is set, the app connects to the specified database (Neon or any PostgreSQL database)

## API Documentation

Visit `http://localhost:8000/docs` when the server is running to see the interactive API documentation.