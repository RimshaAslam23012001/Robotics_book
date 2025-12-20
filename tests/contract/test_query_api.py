import pytest
from fastapi.testclient import TestClient
from src.rag_agent.main import app
from src.rag_agent.models.query_models import QueryRequest


client = TestClient(app)


def test_query_endpoint_contract():
    """
    Contract test for /query endpoint to ensure it meets API specification
    """
    # Test valid request
    response = client.post(
        "/api/v1/query",
        json={
            "query": "test query",
            "top_k": 5
        }
    )

    # Should return 200 OK
    assert response.status_code == 200

    # Response should have required fields
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    # Test with different top_k values
    response = client.post(
        "/api/v1/query",
        json={
            "query": "another test",
            "top_k": 10
        }
    )
    assert response.status_code == 200


def test_query_endpoint_invalid_request():
    """
    Test that invalid requests return appropriate error responses
    """
    # Test with empty query
    response = client.post(
        "/api/v1/query",
        json={
            "query": "",
            "top_k": 5
        }
    )
    assert response.status_code == 400

    # Test with invalid top_k
    response = client.post(
        "/api/v1/query",
        json={
            "query": "test query",
            "top_k": 0  # Should be >= 1
        }
    )
    assert response.status_code == 400

    response = client.post(
        "/api/v1/query",
        json={
            "query": "test query",
            "top_k": 25  # Should be <= 20
        }
    )
    assert response.status_code == 400


def test_query_request_model_validation():
    """
    Test QueryRequest model validation
    """
    # Valid request
    valid_request = QueryRequest(query="test query", top_k=5)
    assert valid_request.query == "test query"
    assert valid_request.top_k == 5

    # Test validation constraints
    with pytest.raises(ValueError):
        QueryRequest(query="", top_k=5)  # Empty query

    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=0)  # top_k < 1

    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=25)  # top_k > 20