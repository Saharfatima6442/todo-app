from typing import Optional
from src.models.user_db import User
import bcrypt


class UserService:
    """
    Service class to manage users in memory.
    In a real application, this would connect to a database.
    """
    
    def __init__(self):
        """Initialize the service with an empty list of users."""
        self.users: dict[str, User] = {}  # email -> User mapping
        self.users_by_id: dict[str, User] = {}  # id -> User mapping

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