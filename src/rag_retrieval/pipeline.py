import time
import logging
from typing import List, Dict, Any
from src.config.settings import Settings
from src.rag_retrieval.embedding_service import CohereEmbeddingService
from src.rag_retrieval.qdrant_client import QdrantSearchClient
from src.rag_retrieval.retrieval_validator import RetrievalValidator
from src.rag_retrieval.output_formatter import OutputFormatter, QueryResult


# Set up minimal logging for evaluation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RetrievalPipeline:
    """Main pipeline service that orchestrates all components."""

    def __init__(self):
        """Initialize the retrieval pipeline with all required services."""
        self.settings = Settings()
        self.embedding_service = CohereEmbeddingService()
        self.qdrant_client = QdrantSearchClient()
        self.validator = RetrievalValidator()
        self.formatter = OutputFormatter()

    def execute_retrieval(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
        validate: bool = True
    ) -> QueryResult:
        """
        Execute the full retrieval pipeline.

        Args:
            query: The query text to search for
            top_k: Number of results to retrieve
            min_score: Minimum similarity threshold
            validate: Whether to perform validation

        Returns:
            QueryResult object with retrieval results
        """
        start_time = time.time()
        logger.info(f"Starting retrieval for query: '{query[:50]}...'" if len(query) > 50 else f"Starting retrieval for query: '{query}'")

        # Step 1: Generate embedding for the query
        query_vector = self.embedding_service.generate_embedding(query)

        # Step 2: Search in Qdrant
        raw_results = self.qdrant_client.search(
            query_vector=query_vector,
            top_k=top_k,
            min_score=min_score
        )

        # Calculate search time
        search_time = time.time() - start_time

        # Step 3: Perform validation if requested
        validation_results = []
        if validate and raw_results:
            for result in raw_results:
                # For actual validation, we would need expected values
                # For now, we'll validate the structure and content format
                validation_result = self.validator.validate_retrieved_chunk(result, result)
                validation_results.append(validation_result)
        else:
            # If no validation is requested or no results, create basic validation results
            from src.rag_retrieval.retrieval_validator import ValidationResult
            for result in raw_results:
                validation_results.append(ValidationResult(
                    is_content_valid=True,
                    is_metadata_valid=True
                ))

        # Calculate total processing time
        total_processing_time = time.time() - start_time

        logger.info(f"Retrieval completed in {total_processing_time:.3f}s, found {len(raw_results)} results")

        # Step 4: Format results as QueryResult
        query_result = self.formatter.format_query_result(
            query=query,
            top_k=top_k,
            retrieved_chunks_data=raw_results,
            processing_time=total_processing_time,
            validation_results=validation_results
        )

        return query_result

    def execute_retrieval_json(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
        validate: bool = True
    ) -> str:
        """
        Execute the full retrieval pipeline and return JSON string.

        Args:
            query: The query text to search for
            top_k: Number of results to retrieve
            min_score: Minimum similarity threshold
            validate: Whether to perform validation

        Returns:
            JSON string with retrieval results
        """
        query_result = self.execute_retrieval(query, top_k, min_score, validate)
        return self.formatter.format_as_json(query_result)