from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PersonalizationStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class PersonalizationRequestBase(BaseModel):
    requestId: str
    userId: str
    chapterId: str
    status: PersonalizationStatusEnum = PersonalizationStatusEnum.pending


class PersonalizationRequestCreate(PersonalizationRequestBase):
    pass


class PersonalizationRequestUpdate(BaseModel):
    status: Optional[PersonalizationStatusEnum] = None
    personalizedContent: Optional[str] = None
    userBackgroundApplied: Optional[Dict[str, Any]] = None
    processingTime: Optional[float] = None
    completedAt: Optional[datetime] = None


class PersonalizationRequest(PersonalizationRequestBase):
    createdAt: datetime
    completedAt: Optional[datetime] = None
    personalizedContent: Optional[str] = None
    userBackgroundApplied: Optional[Dict[str, Any]] = None
    processingTime: Optional[float] = None

    class Config:
        from_attributes = True