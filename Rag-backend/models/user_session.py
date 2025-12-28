from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSessionBase(BaseModel):
    userId: str
    authToken: str
    translationPreferences: Optional[dict] = None


class UserSessionCreate(UserSessionBase):
    pass


class UserSessionUpdate(BaseModel):
    translationPreferences: Optional[dict] = None


class UserSession(UserSessionBase):
    createdAt: datetime

    class Config:
        from_attributes = True