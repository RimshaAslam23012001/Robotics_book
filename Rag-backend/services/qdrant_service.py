from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional, List, Dict, Any
from config import QDRANT_URL, QDRANT_API_KEY
from models.chapter_content import ChapterContent
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_available = True
        try:
            if QDRANT_API_KEY:
                self.client = QdrantClient(
                    url=QDRANT_URL,
                    api_key=QDRANT_API_KEY,
                    timeout=10
                )
            else:
                self.client = QdrantClient(
                    url=QDRANT_URL,
                    timeout=10
                )

            # Collection name for chapter content
            self.collection_name = "chapter_content"

            # Initialize the collection if it doesn't exist
            self._init_collection()
        except Exception as e:
            logger.warning(f"Qdrant is not available: {e}. Running in fallback mode.")
            self.qdrant_available = False
            # In fallback mode, we'll return None for all operations

    def _init_collection(self):
        """Initialize the chapter content collection if it doesn't exist."""
        if not self.qdrant_available:
            logger.warning("Qdrant is not available, skipping collection initialization")
            return

        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with default configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1,  # We're not using vector search for chapter content, just storing
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload index for chapterId
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chapterId",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info(f"Created collection '{self.collection_name}'")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            # Don't raise the exception to allow the service to continue in fallback mode
            logger.warning("Continuing in fallback mode due to Qdrant initialization error")
            self.qdrant_available = False

    def store_chapter_content(self, chapter: ChapterContent) -> bool:
        """Store chapter content in Qdrant."""
        if not self.qdrant_available:
            logger.warning("Qdrant is not available, skipping store operation")
            return False

        try:
            points = [
                models.PointStruct(
                    id=chapter.chapterId,
                    payload={
                        "chapterId": chapter.chapterId,
                        "title": chapter.title,
                        "slug": chapter.slug,
                        "originalContent": chapter.originalContent,
                        "metadata": chapter.metadata or {},
                        "createdAt": chapter.createdAt.isoformat() if hasattr(chapter, 'createdAt') else None
                    },
                    vector=[0.0]  # Placeholder vector since we're doing exact match
                )
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Stored chapter content for {chapter.chapterId}")
            return True
        except Exception as e:
            logger.error(f"Error storing chapter content: {e}")
            return False

    def retrieve_chapter_content(self, chapter_id: str) -> Optional[ChapterContent]:
        """Retrieve chapter content by chapter ID."""
        if not self.qdrant_available:
            logger.warning("Qdrant is not available, skipping retrieve operation")
            return None

        try:
            # Search for the specific chapter by ID
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="chapterId",
                            match=models.MatchValue(value=chapter_id)
                        )
                    ]
                ),
                limit=1
            )

            if results[0]:  # If we have results
                point = results[0][0]  # Get the first result
                payload = point.payload

                # Create ChapterContent object from payload
                chapter = ChapterContent(
                    chapterId=payload["chapterId"],
                    title=payload["title"],
                    slug=payload["slug"],
                    originalContent=payload["originalContent"],
                    metadata=payload.get("metadata"),
                    createdAt=payload.get("createdAt")
                )

                logger.info(f"Retrieved chapter content for {chapter_id}")
                return chapter
            else:
                logger.warning(f"Chapter content not found for {chapter_id}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving chapter content: {e}")
            return None

    def update_chapter_content(self, chapter_id: str, content: str) -> bool:
        """Update chapter content in Qdrant."""
        if not self.qdrant_available:
            logger.warning("Qdrant is not available, skipping update operation")
            return False

        try:
            # First retrieve the existing chapter to get all data
            existing_chapter = self.retrieve_chapter_content(chapter_id)
            if not existing_chapter:
                logger.warning(f"Cannot update chapter {chapter_id}, not found")
                return False

            # Update the content and store again
            updated_chapter = ChapterContent(
                chapterId=existing_chapter.chapterId,
                title=existing_chapter.title,
                slug=existing_chapter.slug,
                originalContent=content,
                metadata=existing_chapter.metadata,
                createdAt=existing_chapter.createdAt
            )

            return self.store_chapter_content(updated_chapter)
        except Exception as e:
            logger.error(f"Error updating chapter content: {e}")
            return False

    def delete_chapter_content(self, chapter_id: str) -> bool:
        """Delete chapter content from Qdrant."""
        if not self.qdrant_available:
            logger.warning("Qdrant is not available, skipping delete operation")
            return False

        try:
            # Delete by ID
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[chapter_id]
                )
            )

            logger.info(f"Deleted chapter content for {chapter_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting chapter content: {e}")
            return False


# Global instance of QdrantService
qdrant_service = QdrantService()