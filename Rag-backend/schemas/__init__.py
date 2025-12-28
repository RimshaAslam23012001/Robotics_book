from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TranslateChapterResponse(BaseModel):
    chapterId: str
    translatedContent: str
    processingTime: float
    translationQuality: str


class GetChapterResponse(BaseModel):
    chapterId: str
    title: str
    slug: str
    originalContent: str
    metadata: Optional[Dict[str, Any]] = None


class TranslationStatusResponse(BaseModel):
    requestId: str
    status: str
    processingTime: Optional[float] = None
    translatedContent: Optional[str] = None