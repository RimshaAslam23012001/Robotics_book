import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.rag_agent.services.retrieval_service import RetrievalService
from src.rag_agent.models.chunk_models import RetrievedChunk, ChunkMetadata


@pytest.mark.asyncio
async def test_retrieval_service_initialization():
    """
    Test retrieval service initialization
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"
        mock_settings.qdrant_host = "localhost"
        mock_settings.qdrant_port = 6333
        mock_settings.qdrant_collection_name = "test_collection"

        service = RetrievalService()

        assert service.qdrant_host == "localhost"
        assert service.qdrant_port == 6333
        assert service.collection_name == "test_collection"
        assert service.cohere_model == "embed-multilingual-v3.0"


@pytest.mark.asyncio
async def test_retrieval_service_with_cohere():
    """
    Test retrieval service with Cohere integration
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        service = RetrievalService()

        # Mock the Cohere client
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3]]
        service.cohere_client = Mock()
        service.cohere_client.embed.return_value = mock_embed_response

        # Test embedding generation
        embedding = await service._generate_embedding("test text")

        assert embedding == [0.1, 0.2, 0.3]
        service.cohere_client.embed.assert_called_once_with(
            texts=["test text"],
            model="embed-multilingual-v3.0"
        )


@pytest.mark.asyncio
async def test_retrieval_service_without_cohere_key():
    """
    Test retrieval service without Cohere key
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = None

        service = RetrievalService()

        # Should return mock embedding
        embedding = await service._generate_embedding("test text")

        # Should return a list of floats with default length
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)


@pytest.mark.asyncio
async def test_retrieval_service_retrieve_chunks():
    """
    Test retrieve_chunks method with validation
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        service = RetrievalService()

        # Mock the embedding generation
        with patch.object(service, '_generate_embedding', new_callable=AsyncMock) as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]

            # Test with valid parameters
            chunks = await service.retrieve_chunks("test query", top_k=3)

            assert chunks == []
            mock_embed.assert_called_once_with("test query")


@pytest.mark.asyncio
async def test_retrieval_service_input_validation():
    """
    Test input validation in retrieve_chunks
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"

        service = RetrievalService()

        # Test with empty query
        with pytest.raises(ValueError):
            await service.retrieve_chunks("", top_k=3)

        # Test with query containing only whitespace
        with pytest.raises(ValueError):
            await service.retrieve_chunks("   ", top_k=3)

        # Test with invalid top_k (too low)
        with pytest.raises(ValueError):
            await service.retrieve_chunks("test", top_k=0)

        # Test with invalid top_k (too high)
        with pytest.raises(ValueError):
            await service.retrieve_chunks("test", top_k=25)


def test_format_retrieved_chunk():
    """
    Test _format_retrieved_chunk method
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"

        service = RetrievalService()

        raw_data = {
            "text": "Sample text content",
            "similarity_score": 0.85,
            "metadata": {
                "url": "/docs/sample",
                "chunk_id": "chunk_123",
                "module": "test_module",
                "chapter": "test_chapter",
                "section": "test_section"
            }
        }

        chunk = service._format_retrieved_chunk(raw_data)

        assert chunk.text == "Sample text content"
        assert chunk.similarity_score == 0.85
        assert chunk.metadata.url == "/docs/sample"
        assert chunk.metadata.chunk_id == "chunk_123"
        assert chunk.metadata.module == "test_module"
        assert chunk.metadata.chapter == "test_chapter"
        assert chunk.metadata.section == "test_section"


def test_format_retrieved_chunk_minimal():
    """
    Test _format_retrieved_chunk with minimal metadata
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"

        service = RetrievalService()

        raw_data = {
            "text": "Minimal text",
            "similarity_score": 0.7,
            "metadata": {
                "url": "/docs/minimal",
                "chunk_id": "chunk_456"
            }
        }

        chunk = service._format_retrieved_chunk(raw_data)

        assert chunk.text == "Minimal text"
        assert chunk.similarity_score == 0.7
        assert chunk.metadata.url == "/docs/minimal"
        assert chunk.metadata.chunk_id == "chunk_456"
        assert chunk.metadata.module is None
        assert chunk.metadata.chapter is None
        assert chunk.metadata.section is None


def test_format_retrieved_chunk_validation():
    """
    Test validation in _format_retrieved_chunk
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-key"

        service = RetrievalService()

        # Test with empty text
        raw_data_empty_text = {
            "text": "",
            "similarity_score": 0.8,
            "metadata": {
                "url": "/docs/empty",
                "chunk_id": "chunk_789"
            }
        }

        with pytest.raises(ValueError):
            service._format_retrieved_chunk(raw_data_empty_text)

        # Test with invalid similarity score (too high)
        raw_data_high_score = {
            "text": "Valid text",
            "similarity_score": 1.5,
            "metadata": {
                "url": "/docs/high",
                "chunk_id": "chunk_999"
            }
        }

        with pytest.raises(ValueError):
            service._format_retrieved_chunk(raw_data_high_score)

        # Test with invalid similarity score (too low)
        raw_data_low_score = {
            "text": "Valid text",
            "similarity_score": -0.1,
            "metadata": {
                "url": "/docs/low",
                "chunk_id": "chunk_888"
            }
        }

        with pytest.raises(ValueError):
            service._format_retrieved_chunk(raw_data_low_score)