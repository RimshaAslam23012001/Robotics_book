import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Chapter Urdu Translation API"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

# Note: The following tests would require authentication and proper setup
# They are included as examples of what tests might look like

def test_translation_endpoint():
    """Test translation endpoint (would need auth token in real implementation)"""
    # This is just a structure example - would need proper auth setup
    pass

def test_chapter_endpoint():
    """Test chapter endpoint (would need auth token in real implementation)"""
    # This is just a structure example - would need proper auth setup
    pass