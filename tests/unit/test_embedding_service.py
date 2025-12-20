import pytest
from unittest.mock import Mock, patch
from src.rag_retrieval.embedding_service import CohereEmbeddingService


class TestCohereEmbeddingService:
    """Unit tests for CohereEmbeddingService."""

    @pytest.fixture
    def embedding_service(self):
        """Create a CohereEmbeddingService instance for testing."""
        with patch('cohere.Client') as mock_client:
            service = CohereEmbeddingService(api_key="test-key")
            service.client = mock_client
            return service

    def test_generate_embedding_success(self, embedding_service):
        """Test successful embedding generation for a single text."""
        # Arrange
        test_text = "This is a test sentence."
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        embedding_service.client.embed.return_value = Mock()
        embedding_service.client.embed.return_value.embeddings = [expected_embedding]

        # Act
        result = embedding_service.generate_embedding(test_text)

        # Assert
        assert result == expected_embedding
        embedding_service.client.embed.assert_called_once_with(
            texts=[test_text],
            model="embed-multilingual-v3.0"
        )

    def test_generate_embedding_empty_text_raises_error(self, embedding_service):
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            embedding_service.generate_embedding("")

    def test_generate_embedding_whitespace_text_raises_error(self, embedding_service):
        """Test that whitespace-only text raises ValueError."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            embedding_service.generate_embedding("   ")

    def test_generate_embeddings_success(self, embedding_service):
        """Test successful embedding generation for multiple texts."""
        # Arrange
        test_texts = ["Text 1", "Text 2", "Text 3"]
        expected_embeddings = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]
        embedding_service.client.embed.return_value = Mock()
        embedding_service.client.embed.return_value.embeddings = expected_embeddings

        # Act
        result = embedding_service.generate_embeddings(test_texts)

        # Assert
        assert result == expected_embeddings
        embedding_service.client.embed.assert_called_once_with(
            texts=test_texts,
            model="embed-multilingual-v3.0"
        )

    def test_generate_embeddings_empty_list_raises_error(self, embedding_service):
        """Test that empty text list raises ValueError."""
        with pytest.raises(ValueError, match="Input texts list cannot be empty"):
            embedding_service.generate_embeddings([])

    def test_generate_embeddings_all_empty_texts_raises_error(self, embedding_service):
        """Test that list with all empty texts raises ValueError."""
        with pytest.raises(ValueError, match="All input texts are empty"):
            embedding_service.generate_embeddings(["", "   ", "\t\n"])