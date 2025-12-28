from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TechnicalDepthEnum(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class TerminologyComplexityEnum(str, Enum):
    simple = "simple"
    moderate = "moderate"
    complex = "complex"


class ExampleFocusEnum(str, Enum):
    hardware = "hardware"
    software = "software"
    mixed = "mixed"


class AIConceptLevelEnum(str, Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"


class UserProfileBase(BaseModel):
    userId: str
    technicalDepth: TechnicalDepthEnum = TechnicalDepthEnum.intermediate
    terminologyComplexity: TerminologyComplexityEnum = TerminologyComplexityEnum.moderate
    exampleFocus: ExampleFocusEnum = ExampleFocusEnum.mixed
    aiConceptLevel: AIConceptLevelEnum = AIConceptLevelEnum.intermediate


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    technicalDepth: Optional[TechnicalDepthEnum] = None
    terminologyComplexity: Optional[TerminologyComplexityEnum] = None
    exampleFocus: Optional[ExampleFocusEnum] = None
    aiConceptLevel: Optional[AIConceptLevelEnum] = None


class UserProfile(UserProfileBase):
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True