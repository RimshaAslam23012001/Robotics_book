from fastapi import HTTPException
from typing import Optional, Dict, Any
import jwt
from datetime import datetime, timedelta
import os
import secrets
from pydantic import BaseModel
import hashlib

# Secret key for JWT
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("AUTH_SECRET_KEY", "your-super-secret-key-change-in-production"))
ALGORITHM = "HS256"

# Mock user storage for development
mock_users_db = {}

def hash_password(password: str) -> str:
    """Simple password hashing using SHA256 with salt"""
    # Generate a salt
    salt = secrets.token_hex(16)
    # Combine password and salt, then hash
    pwdhash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    # Return salt + hash for storage
    return f"{salt}:{pwdhash}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password"""
    try:
        salt, pwdhash = hashed_password.split(':')
        # Hash the provided password with the stored salt
        new_hash = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
        return new_hash == pwdhash
    except ValueError:
        # If the format is wrong, return False
        return False

class User(BaseModel):
    id: str
    email: str
    name: str
    hashed_password: str
    software_background: Optional[str] = "beginner"
    programming_languages: Optional[list] = []
    ai_ml_experience: Optional[str] = "learning"
    hardware_background: Optional[str] = "none"
    primary_learning_goal: Optional[str] = ""
    profile_complete: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class MockBetterAuth:
    """
    Mock Better Auth implementation for development
    """

    def __init__(self):
        self.users = mock_users_db

    async def create_user(self, email: str, password: str, name: str, **kwargs) -> Optional[User]:
        """Create a new user"""
        if email in self.users:
            raise HTTPException(status_code=400, detail="User already exists")

        user_id = f"user_{secrets.token_urlsafe(16)}"
        hashed_password = hash_password(password)

        user = User(
            id=user_id,
            email=email,
            name=name,
            hashed_password=hashed_password,
            **kwargs
        )

        self.users[email] = user
        return user

    async def sign_in_with_email_password(self, email: str, password: str):
        """Sign in with email and password"""
        user = self.users.get(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create a mock session with token
        token_data = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return type('Session', (), {
            'access_token': token,
            'token_type': 'Bearer',
            'user': user
        })()

    async def verify_token(self, token: str):
        """Verify authentication token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("email")
            if email is None:
                return None

            user = self.users.get(email)
            return user
        except jwt.PyJWTError:
            return None

    async def update_user(self, user_id: str, **kwargs):
        """Update user information"""
        for user in self.users.values():
            if user.id == user_id:
                # Update user with provided fields
                for key, value in kwargs.items():
                    if hasattr(user, key) and value is not None:
                        setattr(user, key, value)
                user.updated_at = datetime.utcnow()
                return user
        return None

# Initialize mock auth instance
auth_instance = MockBetterAuth()