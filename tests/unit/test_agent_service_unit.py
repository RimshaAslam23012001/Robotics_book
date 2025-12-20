import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.rag_agent.services.agent_service import AgentService
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import RetrievedChunk, ChunkMetadata


@pytest.mark.asyncio
async def test_agent_service_with_valid_request():
    """
    Test agent service with valid query request
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None  # Test without OpenAI
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        # Mock the retrieval service
        with patch.object(agent_service.retrieval_service, 'retrieve_chunks', new_callable=AsyncMock) as mock_retrieve:
            expected_chunks = [
                RetrievedChunk(
                    text="Test chunk 1",
                    similarity_score=0.9,
                    metadata=ChunkMetadata(url="/test1", chunk_id="1")
                )
            ]
            mock_retrieve.return_value = expected_chunks

            query_request = QueryRequest(query="test query", top_k=3)
            result = await agent_service.process_query(query_request)

            assert result == expected_chunks
            mock_retrieve.assert_called_once_with(query_text="test query", top_k=3, filters=None)


@pytest.mark.asyncio
async def test_agent_service_with_filters():
    """
    Test agent service with filters
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        # Mock the retrieval service
        with patch.object(agent_service.retrieval_service, 'retrieve_chunks', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = []

            query_request = QueryRequest(
                query="test query",
                top_k=5,
                filters={"module": "ai", "chapter": "intro"}
            )
            result = await agent_service.process_query(query_request)

            mock_retrieve.assert_called_once_with(
                query_text="test query",
                top_k=5,
                filters={"module": "ai", "chapter": "intro"}
            )


@pytest.mark.asyncio
async def test_agent_service_validation():
    """
    Test agent service input validation
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        # Test with empty query
        with pytest.raises(ValueError):
            await agent_service.process_query(QueryRequest(query="", top_k=3))

        # Test with invalid top_k
        with pytest.raises(ValueError):
            await agent_service.process_query(QueryRequest(query="test", top_k=0))

        with pytest.raises(ValueError):
            await agent_service.process_query(QueryRequest(query="test", top_k=25))


def test_agent_service_initialization():
    """
    Test agent service initialization
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        assert agent_service.client is not None
        assert agent_service.retrieval_service is not None


def test_agent_service_without_openai_key():
    """
    Test agent service initialization without OpenAI key
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        assert agent_service.client is None
        assert agent_service.retrieval_service is not None


@pytest.mark.asyncio
async def test_agent_process_with_agent_method():
    """
    Test the internal _process_with_agent method
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = None
        mock_settings.cohere_api_key = "test-key"

        agent_service = AgentService()

        # Mock the retrieval service
        with patch.object(agent_service.retrieval_service, 'retrieve_chunks', new_callable=AsyncMock) as mock_retrieve:
            expected_chunks = [
                RetrievedChunk(
                    text="Test chunk from agent",
                    similarity_score=0.8,
                    metadata=ChunkMetadata(url="/test", chunk_id="2")
                )
            ]
            mock_retrieve.return_value = expected_chunks

            query_request = QueryRequest(query="agent test", top_k=2)
            result = await agent_service._process_with_agent(query_request)

            assert result == expected_chunks
            mock_retrieve.assert_called_once_with(query_text="agent test", top_k=2, filters=None)