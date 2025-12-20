import pytest
from unittest.mock import Mock, patch
from src.rag_retrieval.embedding_service import EmbeddingService


class TestEmbeddingService:
    """Unit tests for EmbeddingService."""

    @pytest.fixture
    def cohere_embedding_service(self):
        """Create a Cohere EmbeddingService instance for testing."""
        with patch('cohere.Client') as mock_client:
            # Temporarily set HF_AVAILABLE to False to test Cohere path
            import src.rag_retrieval.embedding_service as emb_service
            original_hf_available = emb_service.HF_AVAILABLE
            emb_service.HF_AVAILABLE = False

            try:
                service = EmbeddingService(provider="cohere", api_key="test-key")
                service.client = mock_client
                yield service
            finally:
                emb_service.HF_AVAILABLE = original_hf_available

    def test_init_with_cohere_provider(self):
        """Test initialization with Cohere provider."""
        with patch('cohere.Client') as mock_client:
            import src.rag_retrieval.embedding_service as emb_service
            original_hf_available = emb_service.HF_AVAILABLE
            emb_service.HF_AVAILABLE = False

            try:
                service = EmbeddingService(provider="cohere", api_key="test-key")
                assert service.provider == "cohere"
            finally:
                emb_service.HF_AVAILABLE = original_hf_available

    def test_init_with_huggingface_provider(self):
        """Test initialization with HuggingFace provider."""
        # Mock the imports to avoid requiring the actual libraries
        with patch('src.rag_retrieval.embedding_service.SentenceTransformer') as mock_model:
            import src.rag_retrieval.embedding_service as emb_service
            original_hf_available = emb_service.HF_AVAILABLE
            emb_service.HF_AVAILABLE = True

            try:
                service = EmbeddingService(provider="huggingface", model_name="all-MiniLM-L6-v2")
                assert service.provider == "huggingface"
                assert service.model_name == "all-MiniLM-L6-v2"
                mock_model.assert_called_once_with("all-MiniLM-L6-v2")
            finally:
                emb_service.HF_AVAILABLE = original_hf_available

    def test_generate_embedding_cohere_success(self, cohere_embedding_service):
        """Test successful embedding generation for a single text with Cohere."""
        # Arrange
        test_text = "This is a test sentence."
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        cohere_embedding_service.client.embed.return_value = Mock()
        cohere_embedding_service.client.embed.return_value.embeddings = [expected_embedding]

        # Act
        result = cohere_embedding_service.generate_embedding(test_text)

        # Assert
        assert result == expected_embedding
        cohere_embedding_service.client.embed.assert_called_once_with(
            texts=[test_text],
            model="embed-multilingual-v3.0"
        )

    def test_generate_embedding_hf_success(self):
        """Test successful embedding generation for a single text with HuggingFace."""
        # Mock the imports to avoid requiring the actual libraries
        with patch('src.rag_retrieval.embedding_service.SentenceTransformer') as mock_model_class:
            mock_model_instance = Mock()
            mock_model_instance.encode.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5]]  # Return array of arrays
            mock_model_class.return_value = mock_model_instance

            import src.rag_retrieval.embedding_service as emb_service
            original_hf_available = emb_service.HF_AVAILABLE
            emb_service.HF_AVAILABLE = True

            try:
                service = EmbeddingService(provider="huggingface", model_name="all-MiniLM-L6-v2")
                result = service.generate_embedding("This is a test sentence.")

                assert result == [0.1, 0.2, 0.3, 0.4, 0.5]
                mock_model_instance.encode.assert_called_once_with(
                    ["This is a test sentence."], convert_to_numpy=True
                )
            finally:
                emb_service.HF_AVAILABLE = original_hf_available

    def test_generate_embedding_empty_text_raises_error(self, cohere_embedding_service):
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            cohere_embedding_service.generate_embedding("")

    def test_generate_embedding_whitespace_text_raises_error(self, cohere_embedding_service):
        """Test that whitespace-only text raises ValueError."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            cohere_embedding_service.generate_embedding("   ")

    def test_generate_embeddings_cohere_success(self, cohere_embedding_service):
        """Test successful embedding generation for multiple texts with Cohere."""
        # Arrange
        test_texts = ["Text 1", "Text 2", "Text 3"]
        expected_embeddings = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]
        cohere_embedding_service.client.embed.return_value = Mock()
        cohere_embedding_service.client.embed.return_value.embeddings = expected_embeddings

        # Act
        result = cohere_embedding_service.generate_embeddings(test_texts)

        # Assert
        assert result == expected_embeddings
        cohere_embedding_service.client.embed.assert_called_once_with(
            texts=test_texts,
            model="embed-multilingual-v3.0"
        )

    def test_generate_embeddings_hf_success(self):
        """Test successful embedding generation for multiple texts with HuggingFace."""
        # Mock the imports to avoid requiring the actual libraries
        with patch('src.rag_retrieval.embedding_service.SentenceTransformer') as mock_model_class:
            mock_model_instance = Mock()
            mock_model_instance.encode.return_value = [
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
                [0.7, 0.8, 0.9]
            ]  # Return array of arrays
            mock_model_class.return_value = mock_model_instance

            import src.rag_retrieval.embedding_service as emb_service
            original_hf_available = emb_service.HF_AVAILABLE
            emb_service.HF_AVAILABLE = True

            try:
                service = EmbeddingService(provider="huggingface", model_name="all-MiniLM-L6-v2")
                result = service.generate_embeddings(["Text 1", "Text 2", "Text 3"])

                expected_result = [
                    [0.1, 0.2, 0.3],
                    [0.4, 0.5, 0.6],
                    [0.7, 0.8, 0.9]
                ]
                assert result == expected_result
                mock_model_instance.encode.assert_called_once_with(
                    ["Text 1", "Text 2", "Text 3"], convert_to_numpy=True
                )
            finally:
                emb_service.HF_AVAILABLE = original_hf_available

    def test_generate_embeddings_empty_list_raises_error(self, cohere_embedding_service):
        """Test that empty text list raises ValueError."""
        with pytest.raises(ValueError, match="Input texts list cannot be empty"):
            cohere_embedding_service.generate_embeddings([])

    def test_generate_embeddings_all_empty_texts_raises_error(self, cohere_embedding_service):
        """Test that list with all empty texts raises ValueError."""
        with pytest.raises(ValueError, match="All input texts are empty"):
            cohere_embedding_service.generate_embeddings(["", "   ", "\t\n"])