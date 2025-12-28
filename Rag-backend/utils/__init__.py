import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from config import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_request_id():
    """Generate a unique request ID."""
    return f"req_{secrets.token_urlsafe(16)}"


def sanitize_markdown(content: str) -> str:
    """Basic sanitization of markdown content."""
    # Remove potentially dangerous content while preserving markdown structure
    # This is a simplified version - in production, use a proper markdown sanitizer
    return content


def validate_urdu_content(content: str) -> bool:
    """Basic validation of Urdu content."""
    # Check if content contains Urdu characters (Urdu Unicode range)
    urdu_chars = [char for char in content if '\u0600' <= char <= '\u06FF']
    return len(urdu_chars) > 0