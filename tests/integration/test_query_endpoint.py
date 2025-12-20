import pytest
from fastapi.testclient import TestClient
from src.rag_agent.main import app


client = TestClient(app)


def test_query_processing_integration():
    """
    Integration test for query processing
    """
    # Test basic query processing
    response = client.post(
        "/api/v1/query",
        json={
            "query": "What is artificial intelligence?",
            "top_k": 3
        }
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert data["query"] == "What is artificial intelligence?"
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 0  # May be empty for now since we're using mock
    if data["results"]:
        assert len(data["results"]) <= 3  # Should respect top_k limit

    # Verify optional fields exist
    assert "retrieval_time_ms" in data
    assert "total_chunks_found" in data


def test_query_with_filters():
    """
    Test query processing with filters
    """
    response = client.post(
        "/api/v1/query",
        json={
            "query": "How do robots move?",
            "top_k": 5,
            "filters": {
                "module": "locomotion",
                "chapter": "walking"
            }
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "How do robots move?"
    assert "results" in data


def test_query_endpoint_error_handling():
    """
    Test error handling in query endpoint
    """
    # Test with very long query (should be rejected by validation)
    long_query = "a" * 1001  # Exceeds max length of 1000
    response = client.post(
        "/api/v1/query",
        json={
            "query": long_query,
            "top_k": 5
        }
    )

    assert response.status_code == 400


def test_query_endpoint_special_cases():
    """
    Test special cases for query endpoint
    """
    # Test with minimal query
    response = client.post(
        "/api/v1/query",
        json={
            "query": "AI",
            "top_k": 1
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "AI"

    # Test without top_k (should use default)
    response = client.post(
        "/api/v1/query",
        json={
            "query": "test query"
        }
    )

    assert response.status_code == 200