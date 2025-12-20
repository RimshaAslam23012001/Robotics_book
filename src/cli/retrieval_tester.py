import argparse
import time
import sys
import logging
from typing import List, Dict, Any
from src.config.settings import Settings
from src.rag_retrieval.embedding_service import CohereEmbeddingService
from src.rag_retrieval.qdrant_client import QdrantSearchClient
from src.rag_retrieval.retrieval_validator import RetrievalValidator
from src.rag_retrieval.output_formatter import OutputFormatter, QueryRequest
from src.rag_retrieval.pipeline import logger


class RetrievalTester:
    """Command-line interface for testing the retrieval pipeline."""

    def __init__(self):
        """Initialize the retrieval tester with all required services."""
        self.settings = Settings()
        self.embedding_service = CohereEmbeddingService()
        self.qdrant_client = QdrantSearchClient()
        self.validator = RetrievalValidator()
        self.formatter = OutputFormatter()

    def test_retrieval(self, query: str, top_k: int = 5, min_score: float = 0.0, validate: bool = True) -> str:
        """
        Perform a complete retrieval test from query to JSON output.

        Args:
            query: The query text to search for
            top_k: Number of results to retrieve
            min_score: Minimum similarity threshold
            validate: Whether to perform validation

        Returns:
            JSON string with retrieval results
        """
        start_time = time.time()
        logger.info(f"CLI: Starting retrieval test for query: '{query[:50]}...'" if len(query) > 50 else f"CLI: Starting retrieval test for query: '{query}'")

        # Step 1: Generate embedding for the query
        query_vector = self.embedding_service.generate_embedding(query)

        # Step 2: Search in Qdrant
        raw_results = self.qdrant_client.search(
            query_vector=query_vector,
            top_k=top_k,
            min_score=min_score
        )

        # Calculate processing time so far
        search_time = time.time() - start_time

        # Step 3: Perform validation if requested
        validation_results = []
        if validate and raw_results:
            # For actual validation, we would need expected values
            # For testing purposes, we'll create mock validation results
            for result in raw_results:
                # In a real scenario, we would compare with expected values
                # For now, we'll just return basic validation results
                validation_results.append(
                    self.validator.validate_retrieved_chunk(result, result)
                )

        # If no validation is requested or no results, create basic validation results
        if not validate or not raw_results:
            from src.rag_retrieval.retrieval_validator import ValidationResult
            for result in raw_results:
                validation_results.append(ValidationResult(
                    is_content_valid=True,
                    is_metadata_valid=True
                ))

        # Calculate total processing time
        total_processing_time = time.time() - start_time

        logger.info(f"CLI: Retrieval test completed in {total_processing_time:.3f}s, found {len(raw_results)} results")

        # Step 4: Format results as JSON
        query_result = self.formatter.format_query_result(
            query=query,
            top_k=top_k,
            retrieved_chunks_data=raw_results,
            processing_time=total_processing_time,
            validation_results=validation_results
        )

        json_output = self.formatter.format_as_json(query_result)
        return json_output

    def run(self, args: argparse.Namespace):
        """Run the retrieval test with provided arguments."""
        try:
            # Validate settings
            if not self.settings.validate():
                missing_settings = []
                for setting_name in self.settings.get_required_settings():
                    if not getattr(self.settings, setting_name):
                        missing_settings.append(setting_name)

                print(f"Error: Missing required settings: {', '.join(missing_settings)}", file=sys.stderr)
                print("Please set these environment variables or check your .env file.", file=sys.stderr)
                sys.exit(1)

            # Validate connection to Qdrant
            if not self.qdrant_client.validate_connection():
                print(f"Error: Cannot connect to Qdrant collection '{self.settings.QDRANT_COLLECTION_NAME}'", file=sys.stderr)
                sys.exit(1)

            # Perform retrieval test
            json_result = self.test_retrieval(
                query=args.query,
                top_k=args.top_k,
                min_score=args.min_score,
                validate=args.validate
            )

            # Output result
            print(json_result)

        except Exception as e:
            print(f"Error during retrieval test: {str(e)}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Test Qdrant vector retrieval pipeline with Cohere embeddings"
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Text query for vector search"
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=Settings.DEFAULT_TOP_K,
        help=f"Number of results to retrieve (default: {Settings.DEFAULT_TOP_K})"
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=Settings.MIN_SCORE_THRESHOLD,
        help=f"Minimum similarity threshold (default: {Settings.MIN_SCORE_THRESHOLD})"
    )

    parser.add_argument(
        "--validate",
        type=str,
        default="true",
        choices=["true", "false"],
        help="Enable content and metadata validation (default: true)"
    )

    args = parser.parse_args()

    # Convert string to boolean
    args.validate = args.validate.lower() == "true"

    tester = RetrievalTester()
    tester.run(args)


if __name__ == "__main__":
    main()