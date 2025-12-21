import logging
from typing import List, Optional
from pydantic import ValidationError
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import RetrievedChunk, ChunkMetadata
from src.rag_agent.config.settings import settings
from src.rag_retrieval.qdrant_client import QdrantSearchClient
from src.rag_retrieval.embedding_service import EmbeddingService


logger = logging.getLogger(__name__)


class RetrievalService:
    """
    Service for handling retrieval operations from the vector database
    This service interfaces with the actual Qdrant database and embedding service
    """

    def __init__(self):
        """
        Initialize the Retrieval Service with Qdrant client and embedding service
        """
        # Initialize Qdrant client
        try:
            self.qdrant_client = QdrantSearchClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                collection_name=settings.qdrant_collection_name
            )
        except Exception as e:
            logger.warning(f"Failed to initialize Qdrant client: {e}")
            self.qdrant_client = None

        # Initialize embedding service
        cohere_api_key = settings.cohere_api_key if settings.cohere_api_key else None
        embedding_provider = "cohere" if settings.cohere_api_key else "huggingface"
        self.embedding_service = EmbeddingService(
            provider=embedding_provider,
            api_key=cohere_api_key,
            model_name=getattr(settings, 'hf_model_name', None)
        )

    async def retrieve_chunks(
        self,
        query_text: str,
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks from the vector database based on the query
        """
        try:
            logger.debug(f"Retrieving chunks for query: {query_text[:50]}... with top_k: {top_k}")

            # Validate inputs
            if not query_text or len(query_text.strip()) == 0:
                raise ValueError("Query text cannot be empty")

            if top_k < 1 or top_k > 20:
                raise ValueError("top_k must be between 1 and 20")

            # Check if Qdrant client is available
            if self.qdrant_client is None:
                logger.warning("Qdrant client not available, returning empty results")
                return []

            # Generate embedding for the query using the embedding service
            query_embeddings = self.embedding_service.generate_embeddings([query_text])
            if not query_embeddings or len(query_embeddings) == 0:
                logger.warning("Failed to generate embeddings for query")
                return []

            query_embedding = query_embeddings[0]

            # Search in Qdrant
            search_results = self.qdrant_client.search(
                query_vector=query_embedding,
                top_k=top_k,
                min_score=settings.retrieval_similarity_threshold,
                filters=filters
            )

            # Convert search results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                chunk = self._format_retrieved_chunk(result)
                retrieved_chunks.append(chunk)

            logger.debug(f"Retrieved {len(retrieved_chunks)} chunks")
            return retrieved_chunks

        except ValueError as ve:
            logger.error(f"Validation error in retrieval: {str(ve)}")
            raise
        except ValidationError as ve:
            logger.error(f"Pydantic validation error in retrieval: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in retrieval: {str(e)}")
            # Return empty list instead of raising to prevent 400/500 errors
            return []

    def _format_retrieved_chunk(self, raw_chunk_data: dict) -> RetrievedChunk:
        """
        Format raw chunk data from Qdrant into a RetrievedChunk object
        with proper validation and error handling
        """
        try:
            # Extract data from raw chunk with defaults
            text = raw_chunk_data.get("content", "")
            similarity_score = raw_chunk_data.get("similarity_score", 0.0)

            # Validate required fields
            if not text:
                raise ValueError("Chunk content cannot be empty")

            if not (0.0 <= similarity_score <= 1.0):
                raise ValueError(f"Similarity score must be between 0.0 and 1.0, got {similarity_score}")

            # Create metadata object with validation
            metadata = ChunkMetadata(
                url=raw_chunk_data.get("url", ""),
                chunk_id=raw_chunk_data.get("chunk_id", ""),
                module=raw_chunk_data.get("module"),
                chapter=raw_chunk_data.get("chapter"),
                section=raw_chunk_data.get("section")
            )

            # Create and validate the chunk
            chunk = RetrievedChunk(
                text=text,
                similarity_score=similarity_score,
                metadata=metadata
            )

            return chunk

        except ValidationError as ve:
            logger.error(f"Error validating chunk data: {str(ve)}")
            raise ValueError(f"Invalid chunk data: {str(ve)}")
        except Exception as e:
            logger.error(f"Error formatting retrieved chunk: {str(e)}")
            raise