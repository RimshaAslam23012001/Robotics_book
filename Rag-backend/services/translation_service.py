from typing import Dict, Any, Optional
from datetime import datetime
import logging
import asyncio
import time

from models.translation_request import (
    TranslationRequest,
    TranslationRequestCreate,
    TranslationStatusEnum
)
from services.qdrant_service import qdrant_service
from services.agent_service import agent_service
from utils import generate_request_id, validate_urdu_content

logger = logging.getLogger(__name__)


class TranslationService:
    def __init__(self):
        self.qdrant_service = qdrant_service
        self.agent_service = agent_service

    def translate_chapter_to_urdu(
        self,
        user_id: str,
        chapter_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Main method to translate a chapter to Urdu for a user.
        """
        try:
            start_time = time.time()

            # 1. Get chapter content
            chapter = self.qdrant_service.retrieve_chapter_content(chapter_id)
            if not chapter:
                logger.error(f"Chapter content not found for chapter_id: {chapter_id}")
                return None

            # 2. Translate the content using the agent
            translated_content = self.agent_service.translate_to_urdu(
                chapter.originalContent,
                preserve_code_blocks=True
            )

            if not translated_content:
                logger.error("Failed to translate content to Urdu")
                return None

            # 3. Validate that the content is in Urdu
            if not validate_urdu_content(translated_content):
                logger.warning("Translated content may not be in Urdu")
                # We'll still return it but log the warning

            # 4. Calculate processing time
            processing_time = time.time() - start_time

            # 5. Determine translation quality (simplified)
            translation_quality = self._determine_translation_quality(
                chapter.originalContent,
                translated_content
            )

            # 6. Return the result
            result = {
                "chapterId": chapter_id,
                "translatedContent": translated_content,
                "processingTime": processing_time,
                "translationQuality": translation_quality
            }

            logger.info(f"Chapter {chapter_id} translated to Urdu successfully for user {user_id}")
            return result

        except Exception as e:
            logger.error(f"Error in translate_chapter_to_urdu: {e}")
            return None

    async def translate_chapter_to_urdu_async(
        self,
        user_id: str,
        chapter_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Async version of translate_chapter_to_urdu for better performance.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.translate_chapter_to_urdu,
            user_id,
            chapter_id
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

    def _determine_translation_quality(
        self,
        original_content: str,
        translated_content: str
    ) -> str:
        """
        Simple method to determine translation quality based on content comparison.
        """
        try:
            # Compare character counts as a simple metric
            original_len = len(original_content)
            translated_len = len(translated_content)

            # If the translated content is less than 50% of original, it might be low quality
            if translated_len < original_len * 0.5:
                return "low"
            elif translated_len < original_len * 0.8:
                return "medium"
            else:
                return "high"
        except:
            # If comparison fails, default to medium
            return "medium"


# Global instance of TranslationService
translation_service = TranslationService()