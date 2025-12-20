import pytest
from unittest.mock import Mock, patch, MagicMock
from qdrant_client.http import models
from src.rag_retrieval.qdrant_client import QdrantSearchClient


class TestQdrantSearchClient:
    """Unit tests for QdrantSearchClient."""

    @pytest.fixture
    def qdrant_client(self):
        """Create a QdrantSearchClient instance for testing."""
        with patch('qdrant_client.QdrantClient') as mock_client:
            client = QdrantSearchClient(
                url="http://test-url",
                api_key="test-key",
                collection_name="test_collection"
            )
            client.client = mock_client
            return client

    def test_search_success(self, qdrant_client):
        """Test successful search operation."""
        # Arrange
        query_vector = [0.1, 0.2, 0.3]
        mock_result = Mock()
        mock_result.payload = {"chunk_id": "1", "content": "test content", "url": "http://example.com", "source_title": "Test Title"}
        mock_result.score = 0.85
        qdrant_client.client.search.return_value = [mock_result]

        # Act
        results = qdrant_client.search(query_vector, top_k=5, min_score=0.5)

        # Assert
        assert len(results) == 1
        assert results[0]["chunk_id"] == "1"
        assert results[0]["content"] == "test content"
        assert results[0]["url"] == "http://example.com"
        assert results[0]["similarity_score"] == 0.85
        assert results[0]["metadata"]["source_title"] == "Test Title"

        qdrant_client.client.search.assert_called_once_with(
            collection_name="test_collection",
            query_vector=query_vector,
            limit=5,
            score_threshold=0.5,
            with_payload=True,
            with_vectors=False,
            query_filter=None
        )

    def test_search_with_filters(self, qdrant_client):
        """Test search operation with filters."""
        # Arrange
        query_vector = [0.1, 0.2, 0.3]
        filters = {"category": "science", "author": "test_author"}
        mock_result = Mock()
        mock_result.payload = {"chunk_id": "1", "content": "test content", "url": "http://example.com", "source_title": "Test Title"}
        mock_result.score = 0.85
        qdrant_client.client.search.return_value = [mock_result]

        # Act
        results = qdrant_client.search(query_vector, top_k=3, min_score=0.0, filters=filters)

        # Assert
        assert len(results) == 1
        # Check that the filter was properly constructed
        call_args = qdrant_client.client.search.call_args
        assert call_args is not None
        assert call_args[1]["query_filter"] is not None

    def test_validate_connection_success(self, qdrant_client):
        """Test successful connection validation."""
        # Arrange
        mock_collection = Mock()
        mock_collection.name = "test_collection"
        mock_collections = Mock()
        mock_collections.collections = [mock_collection]
        qdrant_client.client.get_collections.return_value = mock_collections

        # Act
        result = qdrant_client.validate_connection()

        # Assert
        assert result is True

    def test_validate_connection_failure(self, qdrant_client):
        """Test failed connection validation."""
        # Arrange
        mock_collection = Mock()
        mock_collection.name = "other_collection"
        mock_collections = Mock()
        mock_collections.collections = [mock_collection]
        qdrant_client.client.get_collections.return_value = mock_collections

        # Act
        result = qdrant_client.validate_connection()

        # Assert
        assert result is False

    def test_validate_connection_exception(self, qdrant_client):
        """Test connection validation when exception occurs."""
        # Arrange
        qdrant_client.client.get_collections.side_effect = Exception("Connection failed")

        # Act
        result = qdrant_client.validate_connection()

        # Assert
        assert result is False