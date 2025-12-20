import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.rag_agent.services.agent_service import AgentService
from src.rag_agent.models.query_models import QueryRequest


@pytest.mark.asyncio
async def test_agent_service_initialization():
    """
    Test AgentService initialization
    """
    # Mock the settings for testing
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        # Verify initialization
        assert agent_service is not None


@pytest.mark.asyncio
async def test_agent_process_query():
    """
    Test agent processing of a query
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        # Since we're not actually calling OpenAI APIs in tests,
        # we'll test the structure and flow
        query_request = QueryRequest(
            query="What is artificial intelligence?",
            top_k=3
        )

        # Mock the actual processing to avoid external API calls
        with patch.object(agent_service, '_process_with_agent', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = []

            result = await agent_service.process_query(query_request)

            # Verify the method was called
            mock_process.assert_called_once()
            assert result == []


@pytest.mark.asyncio
async def test_agent_error_handling():
    """
    Test error handling in agent service
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        # Test with empty query
        with pytest.raises(ValueError):
            await agent_service.process_query(QueryRequest(query=""))