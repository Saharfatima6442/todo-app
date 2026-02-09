from typing import Optional
from src.models.user_db import User
import bcrypt
import json
import os
from datetime import datetime


class UserService:
    """
    Service class to manage users in memory with file persistence for development.
    In a real application, this would connect to a database.
    """

    def __init__(self):
        """Initialize the service with users loaded from file if available."""
        self.users: dict[str, User] = {}  # email -> User mapping
        self.users_by_id: dict[str, User] = {}  # id -> User mapping
        self.file_path = "users.json"
        
        # Load users from file if it exists
        self.load_users_from_file()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def register_user(self, email: str, password: str) -> Optional[User]:
        """Register a new user."""
        # Check if user already exists
        if email in self.users:
            return None
        
        # Hash the password
        password_hash = self.hash_password(password)
        
        # Create a new user
        user = User.create_new(email, password_hash)
        
        # Store the user
        self.users[email] = user
        self.users_by_id[user.id] = user
        
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = self.users.get(email)
        if not user:
            return None

        if self.verify_password(password, user.password_hash):
            return user

        return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID."""
        return self.users_by_id.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        return self.users.get(email)

    def load_users_from_file(self):
        """Load users from a file if it exists."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    users_data = json.load(f)
                    for email, user_data in users_data.items():
                        # Convert string timestamps back to datetime objects
                        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
                        user_data['updated_at'] = datetime.fromisoformat(user_data['updated_at'])
                        
                        # Create User object from data
                        user = User(**user_data)
                        self.users[email] = user
                        self.users_by_id[user.id] = user
            except Exception as e:
                print(f"Error loading users from file: {e}")
    
    def save_users_to_file(self):
        """Save users to a file."""
        try:
            # Convert users to serializable format
            users_data = {}
            for email, user in self.users.items():
                user_dict = user.__dict__.copy()
                # Convert datetime objects to ISO format strings
                user_dict['created_at'] = user_dict['created_at'].isoformat()
                user_dict['updated_at'] = user_dict['updated_at'].isoformat()
                users_data[email] = user_dict
            
            with open(self.file_path, 'w') as f:
                json.dump(users_data, f, indent=2)
        except Exception as e:
            print(f"Error saving users to file: {e}")
    
    def register_user(self, email: str, password: str) -> Optional[User]:
        """Register a new user."""
        # Check if user already exists
        if email in self.users:
            return None

        # Hash the password
        password_hash = self.hash_password(password)

        # Create a new user
        user = User.create_new(email, password_hash)

        # Store the user
        self.users[email] = user
        self.users_by_id[user.id] = user
        
        # Save users to file
        self.save_users_to_file()

        return user