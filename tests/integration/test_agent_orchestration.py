import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.rag_agent.services.agent_service import AgentService
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import QueryResponse


@pytest.mark.asyncio
async def test_agent_orchestration_integration():
    """
    Integration test for agent orchestration
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        query_request = QueryRequest(
            query="How do humanoid robots maintain balance?",
            top_k=5
        )

        # Mock the agent processing to avoid external API calls
        with patch.object(agent_service, '_process_with_agent', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = []

            response = await agent_service.process_query(query_request)

            # Verify the response structure
            assert isinstance(response, list)  # This will be enhanced later


@pytest.mark.asyncio
async def test_agent_with_filters():
    """
    Test agent orchestration with filters
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        query_request = QueryRequest(
            query="What are the principles of locomotion?",
            top_k=3,
            filters={"module": "locomotion", "chapter": "principles"}
        )

        # Mock the agent processing
        with patch.object(agent_service, '_process_with_agent', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = []

            response = await agent_service.process_query(query_request)

            # Verify the response
            assert isinstance(response, list)


@pytest.mark.asyncio
async def test_agent_integration_error_handling():
    """
    Test error handling in agent orchestration
    """
    with patch('src.rag_agent.services.agent_service.settings') as mock_settings:
        mock_settings.openai_api_key = "test-key"

        agent_service = AgentService()

        # Test with invalid top_k value
        query_request = QueryRequest(
            query="Test query",
            top_k=0  # Invalid
        )

        with pytest.raises(ValueError):
            await agent_service.process_query(query_request)