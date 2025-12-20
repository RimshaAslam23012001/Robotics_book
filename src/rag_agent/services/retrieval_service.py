import logging
from typing import List, Optional
from pydantic import ValidationError
import cohere
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import RetrievedChunk, ChunkMetadata
from src.rag_agent.config.settings import settings


logger = logging.getLogger(__name__)


class RetrievalService:
    """
    Service for handling retrieval operations from the vector database
    This service will interface with the Spec-002 retrieval pipeline
    """

    def __init__(self):
        """
        Initialize the Retrieval Service with Cohere and Qdrant clients
        """
        # Initialize Cohere client
        if settings.cohere_api_key:
            self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)
        else:
            self.cohere_client = None
            logger.warning("Cohere API key not configured. Embedding functionality will be limited.")

        self.qdrant_host = settings.qdrant_host
        self.qdrant_port = settings.qdrant_port
        self.collection_name = settings.qdrant_collection_name
        self.cohere_model = settings.cohere_model

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

            # Generate embedding for the query using Cohere
            query_embedding = await self._generate_embedding(query_text)

            # This is a placeholder implementation
            # In a real implementation, this would query Qdrant with the embedding
            # For now, return an empty list
            # This will be enhanced when we connect to the actual Spec-002 pipeline
            retrieved_chunks = []

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
            raise

    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Cohere with performance optimizations
        """
        if not self.cohere_client:
            logger.warning("Cohere client not configured, returning mock embedding")
            # Return a mock embedding for testing purposes
            return [0.0] * 1024  # Typical embedding size

        try:
            # For performance, we could implement caching here for repeated queries
            # This is a simplified version without caching to keep the example clean
            response = self.cohere_client.embed(
                texts=[text],
                model=self.cohere_model,
                # Additional performance optimizations could be added here
                input_type="search_query"  # Specify the input type for better performance
            )
            return response.embeddings[0]  # Return the first embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            # Return a mock embedding in case of error
            return [0.0] * 1024

    def _format_retrieved_chunk(self, raw_chunk_data: dict) -> RetrievedChunk:
        """
        Format raw chunk data from the database into a RetrievedChunk object
        with proper validation and error handling
        """
        try:
            # Extract data from raw chunk with defaults
            text = raw_chunk_data.get("text", "")
            similarity_score = raw_chunk_data.get("similarity_score", 0.0)
            raw_metadata = raw_chunk_data.get("metadata", {})

            # Validate required fields
            if not text:
                raise ValueError("Chunk text cannot be empty")

            if not (0.0 <= similarity_score <= 1.0):
                raise ValueError(f"Similarity score must be between 0.0 and 1.0, got {similarity_score}")

            # Create metadata object with validation
            metadata = ChunkMetadata(
                url=raw_metadata.get("url", ""),
                chunk_id=raw_metadata.get("chunk_id", ""),
                module=raw_metadata.get("module"),
                chapter=raw_metadata.get("chapter"),
                section=raw_metadata.get("section")
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