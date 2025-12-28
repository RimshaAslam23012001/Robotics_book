from typing import Dict, Any, Optional
from datetime import datetime
import logging
import asyncio
import time

from models.user_profile import UserProfile
from models.chapter_content import ChapterContent
from models.personalization_request import (
    PersonalizationRequest,
    PersonalizationRequestCreate,
    PersonalizationStatusEnum
)
from services.qdrant_service import qdrant_service
from services.agent_service import agent_service
from utils import generate_request_id

logger = logging.getLogger(__name__)


class PersonalizationService:
    def __init__(self):
        self.qdrant_service = qdrant_service
        self.agent_service = agent_service

    def get_user_background(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user background preferences.
        In a real implementation, this would fetch from a database.
        For now, we'll return a default profile or simulate fetching.
        """
        # In a real implementation, this would fetch from a database
        # For now, we'll return a default profile with some basic logic
        try:
            # This is a simplified implementation
            # In a real system, you'd fetch from a user profile database
            default_profile = UserProfile(
                userId=user_id,
                technicalDepth="intermediate",
                terminologyComplexity="moderate",
                exampleFocus="mixed",
                aiConceptLevel="intermediate",
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            return default_profile
        except Exception as e:
            logger.error(f"Error getting user background: {e}")
            return None

    def update_user_background(self, user_id: str, background_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update user background preferences.
        In a real implementation, this would update in a database.
        """
        try:
            # Validate the background data
            required_fields = ["technicalDepth", "terminologyComplexity", "exampleFocus", "aiConceptLevel"]
            for field in required_fields:
                if field not in background_data:
                    raise ValueError(f"Missing required field: {field}")

            # In a real implementation, this would update the database
            # For now, we'll return a profile with the updated values
            updated_profile = UserProfile(
                userId=user_id,
                technicalDepth=background_data.get("technicalDepth", "intermediate"),
                terminologyComplexity=background_data.get("terminologyComplexity", "moderate"),
                exampleFocus=background_data.get("exampleFocus", "mixed"),
                aiConceptLevel=background_data.get("aiConceptLevel", "intermediate"),
                createdAt=datetime.utcnow(),  # In real system, preserve original createdAt
                updatedAt=datetime.utcnow()
            )
            return updated_profile
        except Exception as e:
            logger.error(f"Error updating user background: {e}")
            return None

    def personalize_chapter(
        self,
        user_id: str,
        chapter_id: str,
        learning_goal: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Main method to personalize a chapter for a user.
        """
        try:
            start_time = time.time()

            # 1. Get user background
            user_profile = self.get_user_background(user_id)
            if not user_profile:
                logger.error(f"User profile not found for user_id: {user_id}")
                return None

            # 2. Get chapter content
            chapter = self.qdrant_service.retrieve_chapter_content(chapter_id)
            if not chapter:
                logger.error(f"Chapter content not found for chapter_id: {chapter_id}")
                return None

            # 3. Prepare user background data for the agent
            user_background = {
                "technicalDepth": user_profile.technicalDepth,
                "terminologyComplexity": user_profile.terminologyComplexity,
                "exampleFocus": user_profile.exampleFocus,
                "aiConceptLevel": user_profile.aiConceptLevel
            }

            # 4. Personalize the content using the agent
            personalized_content = self.agent_service.personalize_content(
                chapter.originalContent,
                user_background,
                learning_goal
            )

            if not personalized_content:
                logger.error("Failed to personalize content")
                return None

            # 5. Calculate processing time
            processing_time = time.time() - start_time

            # 6. Return the result
            result = {
                "chapterId": chapter_id,
                "personalizedContent": personalized_content,
                "processingTime": processing_time,
                "userBackgroundApplied": user_background
            }

            logger.info(f"Chapter {chapter_id} personalized successfully for user {user_id}")
            return result

        except Exception as e:
            logger.error(f"Error in personalize_chapter: {e}")
            return None

    async def personalize_chapter_async(
        self,
        user_id: str,
        chapter_id: str,
        learning_goal: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Async version of personalize_chapter for better performance.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.personalize_chapter,
            user_id,
            chapter_id,
            learning_goal
        )

    def get_chapter(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the original chapter content.
        """
        try:
            chapter = self.qdrant_service.retrieve_chapter_content(chapter_id)
            if not chapter:
                logger.error(f"Chapter content not found for chapter_id: {chapter_id}")
                return None

            result = {
                "chapterId": chapter.chapterId,
                "title": chapter.title,
                "slug": chapter.slug,
                "originalContent": chapter.originalContent,
                "metadata": chapter.metadata
            }

            return result
        except Exception as e:
            logger.error(f"Error getting chapter: {e}")
            return None


# Global instance of PersonalizationService
personalization_service = PersonalizationService()