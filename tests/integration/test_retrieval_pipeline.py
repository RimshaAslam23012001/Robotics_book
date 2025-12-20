import pytest
import os
from unittest.mock import Mock, patch
from src.rag_retrieval.embedding_service import CohereEmbeddingService
from src.rag_retrieval.qdrant_client import QdrantSearchClient
from src.rag_retrieval.retrieval_validator import RetrievalValidator
from src.rag_retrieval.output_formatter import OutputFormatter


class TestRetrievalPipelineIntegration:
    """Integration tests for the retrieval pipeline."""

    @pytest.fixture
    def mock_services(self):
        """Create mocked services for integration testing."""
        with patch('cohere.Client'), patch('qdrant_client.QdrantClient'):
            embedding_service = CohereEmbeddingService(api_key="test-key")
            qdrant_client = QdrantSearchClient(
                url="http://test-url",
                api_key="test-key",
                collection_name="test_collection"
            )
            validator = RetrievalValidator()
            formatter = OutputFormatter()

            # Mock the actual service calls
            embedding_service.client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            mock_result = Mock()
            mock_result.payload = {
                "chunk_id": "test_chunk_1",
                "content": "This is test content for integration",
                "url": "https://example.com/test",
                "source_title": "Test Document"
            }
            mock_result.score = 0.85
            qdrant_client.client.search.return_value = [mock_result]

            return {
                'embedding': embedding_service,
                'qdrant': qdrant_client,
                'validator': validator,
                'formatter': formatter
            }

    def test_end_to_end_retrieval_pipeline(self, mock_services):
        """Test the complete retrieval pipeline from query to JSON output."""
        # Arrange
        query = "test query for integration"
        embedding_service = mock_services['embedding']
        qdrant_client = mock_services['qdrant']
        validator = mock_services['validator']
        formatter = mock_services['formatter']

        # Act: Execute the full pipeline
        # Step 1: Generate embedding
        query_vector = embedding_service.generate_embedding(query)

        # Step 2: Search in Qdrant
        raw_results = qdrant_client.search(query_vector, top_k=5, min_score=0.5)

        # Step 3: Validate results
        validation_results = []
        for result in raw_results:
            # For this test, we'll validate against the same result as expected
            validation_result = validator.validate_retrieved_chunk(result, result)
            validation_results.append(validation_result)

        # Step 4: Format as JSON
        query_result = formatter.format_query_result(
            query=query,
            top_k=5,
            retrieved_chunks_data=raw_results,
            processing_time=0.1,  # Simulated processing time
            validation_results=validation_results
        )
        json_output = formatter.format_as_json(query_result)

        # Assert
        assert json_output is not None
        assert query in json_output
        assert "test_chunk_1" in json_output
        assert "This is test content for integration" in json_output
        assert "https://example.com/test" in json_output

        # Verify JSON schema is valid
        assert formatter.validate_json_schema(json_output) is True

    def test_content_fidelity_verification(self, mock_services):
        """Test that retrieved content matches original content as expected."""
        # Arrange
        embedding_service = mock_services['embedding']
        qdrant_client = mock_services['qdrant']
        validator = mock_services['validator']

        # Set up mock with specific content
        original_content = "This is the original content that should be retrieved accurately."
        mock_result = Mock()
        mock_result.payload = {
            "chunk_id": "fidelity_test_chunk",
            "content": original_content,
            "url": "https://example.com/fidelity",
            "source_title": "Fidelity Test"
        }
        mock_result.score = 0.9
        qdrant_client.client.search.return_value = [mock_result]

        # Act: Retrieve and validate
        query_vector = embedding_service.generate_embedding("fidelity test")
        raw_results = qdrant_client.search(query_vector)

        # Validate the retrieved content against original
        validation_result = validator.validate_retrieved_chunk(
            raw_results[0],
            {"content": original_content, "url": "https://example.com/fidelity", "chunk_id": "fidelity_test_chunk"}
        )

        # Assert
        assert validation_result.is_content_valid is True
        assert validation_result.is_metadata_valid is True

    def test_metadata_preservation(self, mock_services):
        """Test that metadata is preserved correctly through the pipeline."""
        # Arrange
        expected_metadata = {
            "chunk_id": "metadata_test_chunk",
            "content": "Content for metadata test",
            "url": "https://example.com/metadata-test",
            "source_title": "Metadata Test Document"
        }

        mock_result = Mock()
        mock_result.payload = expected_metadata
        mock_result.score = 0.88
        mock_services['qdrant'].client.search.return_value = [mock_result]

        # Act: Process through pipeline
        query_vector = mock_services['embedding'].generate_embedding("metadata test")
        raw_results = mock_services['qdrant'].search(query_vector)

        # Validate metadata
        validation_result = mock_services['validator'].validate_retrieved_chunk(raw_results[0], expected_metadata)

        # Assert
        assert validation_result.is_metadata_valid is True
        assert raw_results[0]["url"] == expected_metadata["url"]
        assert raw_results[0]["chunk_id"] == expected_metadata["chunk_id"]
        assert raw_results[0]["metadata"]["source_title"] == expected_metadata["source_title"]

    def test_json_output_format_consistency(self, mock_services):
        """Test that JSON output format is consistent and valid."""
        # Arrange
        query = "format test query"
        expected_fields = ["query", "top_k", "retrieved_chunks", "processing_time", "validation_results"]

        # Act: Generate JSON output
        query_vector = mock_services['embedding'].generate_embedding(query)
        raw_results = mock_services['qdrant'].search(query_vector, top_k=3)

        # Validate results
        validation_results = [
            mock_services['validator'].validate_retrieved_chunk(result, result)
            for result in raw_results
        ]

        query_result = mock_services['formatter'].format_query_result(
            query=query,
            top_k=3,
            retrieved_chunks_data=raw_results,
            processing_time=0.05,
            validation_results=validation_results
        )
        json_output = mock_services['formatter'].format_as_json(query_result)

        # Assert
        parsed_json = mock_services['formatter'].validate_json_schema(json_output)
        assert parsed_json is True  # Schema validation passes

        # Parse and check structure
        import json
        data = json.loads(json_output)
        for field in expected_fields:
            assert field in data

        # Check that retrieved_chunks has expected structure
        assert isinstance(data["retrieved_chunks"], list)
        if data["retrieved_chunks"]:
            chunk = data["retrieved_chunks"][0]
            assert "chunk_id" in chunk
            assert "content" in chunk
            assert "url" in chunk
            assert "similarity_score" in chunk
            assert "metadata" in chunk

        # Check that validation_results has expected structure
        assert isinstance(data["validation_results"], list)
        if data["validation_results"]:
            validation = data["validation_results"][0]
            assert "is_content_valid" in validation
            assert "is_metadata_valid" in validation