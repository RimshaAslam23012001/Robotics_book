import json
import pytest
from src.rag_retrieval.output_formatter import OutputFormatter, ValidationResult


class TestOutputFormatter:
    """Unit tests for OutputFormatter."""

    @pytest.fixture
    def formatter(self):
        """Create an OutputFormatter instance for testing."""
        return OutputFormatter()

    def test_format_retrieved_chunk(self, formatter):
        """Test formatting raw chunk data into RetrievedChunk object."""
        # Arrange
        chunk_data = {
            "chunk_id": "test_chunk_123",
            "content": "This is test content",
            "url": "https://example.com",
            "similarity_score": 0.85,
            "metadata": {"source_title": "Test Title", "category": "science"}
        }

        # Act
        result = formatter.format_retrieved_chunk(chunk_data)

        # Assert
        assert result.chunk_id == "test_chunk_123"
        assert result.content == "This is test content"
        assert result.url == "https://example.com"
        assert result.similarity_score == 0.85
        assert result.metadata == {"source_title": "Test Title", "category": "science"}

    def test_format_query_result(self, formatter):
        """Test formatting all retrieval data into QueryResult object."""
        # Arrange
        query = "test query"
        top_k = 5
        retrieved_chunks_data = [
            {
                "chunk_id": "chunk1",
                "content": "Content 1",
                "url": "https://example.com/1",
                "similarity_score": 0.9,
                "metadata": {"source_title": "Title 1"}
            },
            {
                "chunk_id": "chunk2",
                "content": "Content 2",
                "url": "https://example.com/2",
                "similarity_score": 0.8,
                "metadata": {"source_title": "Title 2"}
            }
        ]
        processing_time = 0.123
        validation_results = [
            ValidationResult(is_content_valid=True, is_metadata_valid=True),
            ValidationResult(is_content_valid=False, is_metadata_valid=True)
        ]

        # Act
        result = formatter.format_query_result(
            query, top_k, retrieved_chunks_data, processing_time, validation_results
        )

        # Assert
        assert result.query == query
        assert result.top_k == top_k
        assert len(result.retrieved_chunks) == 2
        assert result.processing_time == processing_time
        assert len(result.validation_results) == 2
        assert result.retrieved_chunks[0].chunk_id == "chunk1"
        assert result.retrieved_chunks[1].chunk_id == "chunk2"

    def test_format_as_json(self, formatter):
        """Test formatting QueryResult object as JSON string."""
        # Arrange
        from src.rag_retrieval.output_formatter import QueryResult, RetrievedChunk
        query_result = QueryResult(
            query="test query",
            top_k=2,
            retrieved_chunks=[
                RetrievedChunk(
                    chunk_id="chunk1",
                    content="Content 1",
                    url="https://example.com/1",
                    similarity_score=0.9,
                    metadata={"source_title": "Title 1"}
                )
            ],
            processing_time=0.123,
            validation_results=[
                ValidationResult(is_content_valid=True, is_metadata_valid=True)
            ]
        )

        # Act
        json_string = formatter.format_as_json(query_result)

        # Assert
        # Check that it's valid JSON
        parsed = json.loads(json_string)
        assert parsed["query"] == "test query"
        assert parsed["top_k"] == 2
        assert len(parsed["retrieved_chunks"]) == 1
        assert parsed["retrieved_chunks"][0]["chunk_id"] == "chunk1"
        assert parsed["processing_time"] == 0.123
        assert len(parsed["validation_results"]) == 1

    def test_validate_json_schema_valid(self, formatter):
        """Test JSON schema validation with valid JSON."""
        # Arrange
        valid_json = json.dumps({
            "query": "test query",
            "top_k": 5,
            "retrieved_chunks": [
                {
                    "chunk_id": "chunk1",
                    "content": "Content 1",
                    "url": "https://example.com",
                    "similarity_score": 0.9,
                    "metadata": {"source_title": "Title 1"}
                }
            ],
            "processing_time": 0.123,
            "validation_results": [
                {
                    "is_content_valid": True,
                    "is_metadata_valid": True,
                    "content_diff": None,
                    "metadata_diff": None
                }
            ]
        })

        # Act
        result = formatter.validate_json_schema(valid_json)

        # Assert
        assert result is True

    def test_validate_json_schema_missing_field(self, formatter):
        """Test JSON schema validation with missing required field."""
        # Arrange
        invalid_json = json.dumps({
            "query": "test query",
            # Missing "top_k" field
            "retrieved_chunks": [],
            "processing_time": 0.123,
            "validation_results": []
        })

        # Act
        result = formatter.validate_json_schema(invalid_json)

        # Assert
        assert result is False

    def test_validate_json_schema_invalid_type(self, formatter):
        """Test JSON schema validation with wrong field type."""
        # Arrange
        invalid_json = json.dumps({
            "query": "test query",
            "top_k": "not_an_integer",  # Should be integer
            "retrieved_chunks": [],
            "processing_time": 0.123,
            "validation_results": []
        })

        # Act
        result = formatter.validate_json_schema(invalid_json)

        # Assert
        assert result is False

    def test_validate_json_schema_invalid_json(self, formatter):
        """Test JSON schema validation with malformed JSON."""
        # Arrange
        invalid_json = "{invalid: json}"

        # Act
        result = formatter.validate_json_schema(invalid_json)

        # Assert
        assert result is False

    def test_format_as_json_with_none_values(self, formatter):
        """Test JSON formatting when some values are None."""
        # Arrange
        from src.rag_retrieval.output_formatter import QueryResult, RetrievedChunk
        query_result = QueryResult(
            query="test query",
            top_k=1,
            retrieved_chunks=[
                RetrievedChunk(
                    chunk_id="chunk1",
                    content="Content 1",
                    url="https://example.com/1",
                    similarity_score=0.9,
                    metadata={}
                )
            ],
            processing_time=0.123,
            validation_results=[
                ValidationResult(
                    is_content_valid=True,
                    is_metadata_valid=True,
                    content_diff=None,
                    metadata_diff=None
                )
            ]
        )

        # Act
        json_string = formatter.format_as_json(query_result)

        # Assert
        parsed = json.loads(json_string)
        assert parsed["validation_results"][0]["content_diff"] is None
        assert parsed["validation_results"][0]["metadata_diff"] is None