from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TranslationStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TranslationQualityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class TranslationRequestBase(BaseModel):
    requestId: str
    userId: str
    chapterId: str
    status: TranslationStatusEnum = TranslationStatusEnum.pending


class TranslationRequestCreate(TranslationRequestBase):
    pass


class TranslationRequestUpdate(BaseModel):
    status: Optional[TranslationStatusEnum] = None
    translatedContent: Optional[str] = None
    processingTime: Optional[float] = None
    translationQuality: Optional[TranslationQualityEnum] = None
    completedAt: Optional[datetime] = None


class TranslationRequest(TranslationRequestBase):
    createdAt: datetime
    completedAt: Optional[datetime] = None
    translatedContent: Optional[str] = None
    processingTime: Optional[float] = None
    translationQuality: Optional[TranslationQualityEnum] = None

    class Config:
        from_attributes = True