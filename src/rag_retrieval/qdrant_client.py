from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from src.config.settings import Settings


class QdrantSearchClient:
    """Client for searching vectors in Qdrant database."""

    def __init__(self, url: str = None, api_key: str = None, collection_name: str = None):
        """
        Initialize the Qdrant client.

        Args:
            url: Qdrant URL. If not provided, uses the one from settings.
            api_key: Qdrant API key. If not provided, uses the one from settings.
            collection_name: Qdrant collection name. If not provided, uses the one from settings.
        """
        self.url = url or Settings.QDRANT_URL
        self.api_key = api_key or Settings.QDRANT_API_KEY
        self.collection_name = collection_name or Settings.QDRANT_COLLECTION_NAME

        # Initialize Qdrant client
        if self.api_key:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
        else:
            self.client = QdrantClient(url=self.url)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        min_score: float = 0.0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.

        Args:
            query_vector: Vector to search for similarity
            top_k: Number of results to return
            min_score: Minimum similarity score threshold
            filters: Optional filters to apply to the search

        Returns:
            List of results with content, metadata, and similarity scores
        """
        # Prepare filters if provided
        search_filter = None
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                filter_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )
            if filter_conditions:
                search_filter = models.Filter(
                    must=filter_conditions
                )

        # Perform the search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=min_score,
            with_payload=True,  # Include payload (metadata)
            with_vectors=False,  # Don't include vectors in response to save bandwidth
            query_filter=search_filter
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_result = {
                "chunk_id": result.payload.get("chunk_id", ""),
                "content": result.payload.get("content", ""),
                "url": result.payload.get("url", ""),
                "similarity_score": result.score,
                "metadata": {
                    "source_title": result.payload.get("source_title", "")
                }
            }
            formatted_results.append(formatted_result)

        return formatted_results

    def validate_connection(self) -> bool:
        """
        Validate connection to Qdrant and check if collection exists.

        Returns:
            True if connection is valid and collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            return self.collection_name in collection_names
        except Exception:
            return False