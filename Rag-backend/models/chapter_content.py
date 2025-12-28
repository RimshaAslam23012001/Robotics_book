from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ChapterContentBase(BaseModel):
    chapterId: str
    title: str
    slug: str
    originalContent: str
    metadata: Optional[Dict[str, Any]] = None


class ChapterContentCreate(ChapterContentBase):
    pass


class ChapterContentUpdate(BaseModel):
    title: Optional[str] = None
    originalContent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ChapterContent(ChapterContentBase):
    createdAt: datetime

    class Config:
        from_attributes = True