from typing import List, Dict, Any
from dataclasses import dataclass
import json
from src.rag_retrieval.retrieval_validator import ValidationResult


@dataclass
class QueryRequest:
    """Represents the input to the retrieval system."""
    query_text: str
    top_k: int = 5
    min_score: float = 0.0


@dataclass
class RetrievedChunk:
    """A text chunk retrieved from the vector database."""
    chunk_id: str
    content: str
    url: str
    similarity_score: float
    metadata: Dict[str, Any]


@dataclass
class QueryResult:
    """Complete result of a retrieval operation."""
    query: str
    top_k: int
    retrieved_chunks: List[RetrievedChunk]
    processing_time: float
    validation_results: List[ValidationResult]


class OutputFormatter:
    """Formatter for generating clean JSON output from retrieval results."""

    def format_retrieved_chunk(self, chunk_data: Dict[str, Any]) -> RetrievedChunk:
        """
        Format raw chunk data into a RetrievedChunk object.

        Args:
            chunk_data: Raw chunk data from Qdrant

        Returns:
            RetrievedChunk object
        """
        return RetrievedChunk(
            chunk_id=chunk_data.get("chunk_id", ""),
            content=chunk_data.get("content", ""),
            url=chunk_data.get("url", ""),
            similarity_score=chunk_data.get("similarity_score", 0.0),
            metadata=chunk_data.get("metadata", {})
        )

    def format_query_result(
        self,
        query: str,
        top_k: int,
        retrieved_chunks_data: List[Dict[str, Any]],
        processing_time: float,
        validation_results: List[ValidationResult]
    ) -> QueryResult:
        """
        Format all retrieval data into a QueryResult object.

        Args:
            query: Original query text
            top_k: Number of results requested
            retrieved_chunks_data: Raw chunk data from Qdrant
            processing_time: Time taken for retrieval
            validation_results: Validation results for each chunk

        Returns:
            QueryResult object
        """
        formatted_chunks = [
            self.format_retrieved_chunk(chunk_data)
            for chunk_data in retrieved_chunks_data
        ]

        return QueryResult(
            query=query,
            top_k=top_k,
            retrieved_chunks=formatted_chunks,
            processing_time=processing_time,
            validation_results=validation_results
        )

    def format_as_json(self, query_result: QueryResult) -> str:
        """
        Format QueryResult object as clean JSON string.

        Args:
            query_result: QueryResult object to format

        Returns:
            JSON string representation
        """
        result_dict = {
            "query": query_result.query,
            "top_k": query_result.top_k,
            "retrieved_chunks": [
                {
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "url": chunk.url,
                    "similarity_score": chunk.similarity_score,
                    "metadata": chunk.metadata
                }
                for chunk in query_result.retrieved_chunks
            ],
            "processing_time": query_result.processing_time,
            "validation_results": [
                {
                    "is_content_valid": result.is_content_valid,
                    "is_metadata_valid": result.is_metadata_valid,
                    "content_diff": result.content_diff,
                    "metadata_diff": result.metadata_diff
                }
                for result in query_result.validation_results
            ]
        }

        return json.dumps(result_dict, indent=2, ensure_ascii=False)

    def validate_json_schema(self, json_string: str) -> bool:
        """
        Validate that the JSON string conforms to expected schema.

        Args:
            json_string: JSON string to validate

        Returns:
            True if JSON schema is valid, False otherwise
        """
        try:
            parsed = json.loads(json_string)

            # Check required top-level fields
            required_fields = ["query", "top_k", "retrieved_chunks", "processing_time", "validation_results"]
            for field in required_fields:
                if field not in parsed:
                    return False

            # Validate types
            if not isinstance(parsed["query"], str):
                return False
            if not isinstance(parsed["top_k"], int):
                return False
            if not isinstance(parsed["retrieved_chunks"], list):
                return False
            if not isinstance(parsed["processing_time"], (int, float)):
                return False
            if not isinstance(parsed["validation_results"], list):
                return False

            # Validate retrieved_chunks structure
            for chunk in parsed["retrieved_chunks"]:
                chunk_required_fields = ["chunk_id", "content", "url", "similarity_score", "metadata"]
                for field in chunk_required_fields:
                    if field not in chunk:
                        return False

            # Validate validation_results structure
            for result in parsed["validation_results"]:
                result_required_fields = ["is_content_valid", "is_metadata_valid"]
                for field in result_required_fields:
                    if field not in result:
                        return False

            return True
        except json.JSONDecodeError:
            return False