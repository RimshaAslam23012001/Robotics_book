from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from config import SECRET_KEY, ALGORITHM


security = HTTPBearer()


class TokenData(BaseModel):
    userId: str


def verify_token(token: str) -> TokenData:
    """
    Verify the JWT token and return the user ID
    In a real implementation, this would verify against your authentication system
    """
    try:
        # This is a simplified implementation
        # In a real system, you'd verify the token against your auth provider
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        token_data = TokenData(userId=user_id)
        return token_data
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user from the token
    """
    token_data = verify_token(credentials.credentials)
    return token_data.userId