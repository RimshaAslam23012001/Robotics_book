import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.rag_agent.services.retrieval_service import RetrievalService
from src.rag_agent.services.agent_service import AgentService
from src.rag_agent.models.query_models import QueryRequest


@pytest.mark.asyncio
async def test_cohere_integration():
    """
    Test that Cohere embedding integration works properly
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-cohere-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        service = RetrievalService()

        # Mock the Cohere client
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        service.cohere_client = Mock()
        service.cohere_client.embed.return_value = mock_embed_response

        # Test embedding generation
        embedding = await service._generate_embedding("test query")

        # Verify the embedding was generated
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        service.cohere_client.embed.assert_called_once()


@pytest.mark.asyncio
async def test_retrieval_service_with_cohere():
    """
    Test retrieval service integration with Cohere
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-cohere-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"
        mock_settings.qdrant_host = "localhost"
        mock_settings.qdrant_port = 6333
        mock_settings.qdrant_collection_name = "documents"

        service = RetrievalService()

        # Mock the Cohere client
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        service.cohere_client = Mock()
        service.cohere_client.embed.return_value = mock_embed_response

        # Test retrieval with mocked embedding
        chunks = await service.retrieve_chunks("test query", top_k=3)

        # Should return empty list since we don't have Qdrant integration yet
        # but the embedding generation should work
        assert chunks == []


@pytest.mark.asyncio
async def test_agent_service_integration():
    """
    Test agent service integration with retrieval pipeline
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None  # Test without OpenAI
        mock_settings.cohere_api_key = "test-cohere-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        agent_service = AgentService()

        # Mock the retrieval service
        with patch.object(agent_service.retrieval_service, 'retrieve_chunks', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = []

            query_request = QueryRequest(query="test query", top_k=3)
            result = await agent_service.process_query(query_request)

            # Verify the retrieval service was called
            mock_retrieve.assert_called_once()
            assert result == []


def test_settings_integration():
    """
    Test that settings are properly configured for Spec-002 integration
    """
    from src.rag_agent.config.settings import settings

    # Verify that the required settings for integration exist
    assert hasattr(settings, 'cohere_api_key')
    assert hasattr(settings, 'cohere_model')
    assert hasattr(settings, 'qdrant_host')
    assert hasattr(settings, 'qdrant_port')
    assert hasattr(settings, 'qdrant_collection_name')
    assert hasattr(settings, 'retrieval_top_k_default')
    assert hasattr(settings, 'retrieval_similarity_threshold')


@pytest.mark.asyncio
async def test_retrieval_service_error_handling():
    """
    Test error handling in retrieval service with Cohere integration
    """
    with patch('src.rag_agent.services.retrieval_service.settings') as mock_settings:
        mock_settings.cohere_api_key = "test-cohere-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        service = RetrievalService()

        # Mock the Cohere client to raise an exception
        service.cohere_client = Mock()
        service.cohere_client.embed.side_effect = Exception("Cohere API error")

        # Should handle the error gracefully and return mock embedding
        embedding = await service._generate_embedding("test query")

        # Should return mock embedding despite the error
        assert isinstance(embedding, list)
        assert len(embedding) > 0


@pytest.mark.asyncio
async def test_agent_with_filters():
    """
    Test that agent properly passes filters to retrieval service
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None  # Test without OpenAI
        mock_settings.cohere_api_key = "test-cohere-key"
        mock_settings.cohere_model = "embed-multilingual-v3.0"

        agent_service = AgentService()

        # Mock the retrieval service
        with patch.object(agent_service.retrieval_service, 'retrieve_chunks', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = []

            query_request = QueryRequest(
                query="test query",
                top_k=3,
                filters={"module": "test_module"}
            )
            result = await agent_service.process_query(query_request)

            # Verify the retrieval service was called with correct parameters
            mock_retrieve.assert_called_once_with(
                query_text="test query",
                top_k=3,
                filters={"module": "test_module"}
            )
            assert result == []