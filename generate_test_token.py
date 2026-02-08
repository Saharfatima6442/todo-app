from jose import jwt
import datetime
import os

# Create a test JWT token for development
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "development-secret-key-change-in-production")
ALGORITHM = "HS256"

# Create payload with user information
payload = {
    "sub": "testuser123",  # This should match the user ID
    "email": "test@example.com",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
}

# Generate the token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print("Test JWT Token:")
print(token)
print("\nCopy this token and paste it in your browser's localStorage:")
print("localStorage.setItem('jwt_token', '" + token + "')")
print("localStorage.setItem('userId', 'testuser123')")