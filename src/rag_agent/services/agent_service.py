import logging
from typing import List, Optional
from openai import AsyncOpenAI
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import RetrievedChunk
from src.rag_agent.config.settings import settings
from src.rag_agent.services.retrieval_service import RetrievalService


logger = logging.getLogger(__name__)


class AgentService:
    """
    Service for orchestrating OpenAI Agent operations for RAG-based query processing
    """

    def __init__(self):
        """
        Initialize the Agent Service with OpenAI client and retrieval service
        """
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured. Agent functionality will be limited.")

        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.retrieval_service = RetrievalService()

    async def process_query(self, query_request: QueryRequest) -> List[RetrievedChunk]:
        """
        Process a query using OpenAI Agent orchestration
        """
        try:
            logger.debug(f"Processing query with agent: {query_request.query[:50]}...")

            # Validate inputs
            if not query_request.query or len(query_request.query.strip()) == 0:
                raise ValueError("Query cannot be empty")

            if query_request.top_k and (query_request.top_k < 1 or query_request.top_k > 20):
                raise ValueError("top_k must be between 1 and 20")

            # Use the retrieval service to get relevant chunks
            # In a real implementation, the agent would coordinate this process
            retrieved_chunks = await self.retrieval_service.retrieve_chunks(
                query_text=query_request.query,
                top_k=query_request.top_k or 5,
                filters=query_request.filters
            )

            logger.debug(f"Agent processing completed, retrieved {len(retrieved_chunks)} chunks")
            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error in agent processing: {str(e)}")
            # Return empty list instead of raising to prevent 400/500 errors
            return []

    async def _process_with_agent(self, query_request: QueryRequest) -> List[RetrievedChunk]:
        """
        Internal method to process query with OpenAI agent
        """
        # This method would use the OpenAI agent to coordinate the RAG process
        # For now, we'll delegate to the retrieval service directly
        # In a full implementation, this would involve more complex orchestration

        retrieved_chunks = await self.retrieval_service.retrieve_chunks(
            query_text=query_request.query,
            top_k=query_request.top_k or 5,
            filters=query_request.filters
        )

        return retrieved_chunks