import pytest
from src.rag_agent.models.chunk_models import QueryResponse, RetrievedChunk, ChunkMetadata


def test_response_structure():
    """
    Unit test for response structure
    """
    # Create a sample chunk
    metadata = ChunkMetadata(
        url="/docs/test",
        chunk_id="chunk_123",
        module="test_module",
        chapter="test_chapter",
        section="test_section"
    )

    chunk = RetrievedChunk(
        text="This is a test chunk.",
        similarity_score=0.85,
        metadata=metadata
    )

    # Create a response
    response = QueryResponse(
        query="Test query",
        results=[chunk],
        retrieval_time_ms=120.5,
        total_chunks_found=1
    )

    # Verify response structure
    assert response.query == "Test query"
    assert len(response.results) == 1
    assert response.results[0].text == "This is a test chunk."
    assert response.results[0].similarity_score == 0.85
    assert response.results[0].metadata.url == "/docs/test"
    assert response.results[0].metadata.chunk_id == "chunk_123"
    assert response.results[0].metadata.module == "test_module"
    assert response.results[0].metadata.chapter == "test_chapter"
    assert response.results[0].metadata.section == "test_section"
    assert response.retrieval_time_ms == 120.5
    assert response.total_chunks_found == 1


def test_response_with_multiple_chunks():
    """
    Test response with multiple chunks
    """
    metadata1 = ChunkMetadata(url="/docs/ai", chunk_id="chunk_001")
    metadata2 = ChunkMetadata(url="/docs/ml", chunk_id="chunk_002")

    chunk1 = RetrievedChunk(text="First chunk", similarity_score=0.9, metadata=metadata1)
    chunk2 = RetrievedChunk(text="Second chunk", similarity_score=0.8, metadata=metadata2)

    response = QueryResponse(
        query="Multi-chunk query",
        results=[chunk1, chunk2],
        retrieval_time_ms=250.0,
        total_chunks_found=2
    )

    assert len(response.results) == 2
    assert response.results[0].text == "First chunk"
    assert response.results[1].text == "Second chunk"
    assert response.results[0].similarity_score == 0.9
    assert response.results[1].similarity_score == 0.8


def test_response_with_empty_results():
    """
    Test response with empty results
    """
    response = QueryResponse(
        query="No results query",
        results=[],
        retrieval_time_ms=50.0,
        total_chunks_found=0
    )

    assert response.query == "No results query"
    assert len(response.results) == 0
    assert response.retrieval_time_ms == 50.0
    assert response.total_chunks_found == 0


def test_response_optional_fields():
    """
    Test response with optional fields
    """
    # Test with None values for optional fields
    response = QueryResponse(
        query="Test query",
        results=[],
        retrieval_time_ms=None,
        total_chunks_found=None
    )

    assert response.retrieval_time_ms is None
    assert response.total_chunks_found is None


def test_chunk_metadata_completeness():
    """
    Test that chunk metadata contains all required fields
    """
    metadata = ChunkMetadata(
        url="/docs/complete",
        chunk_id="complete_123",
        module="complete_module",
        chapter="complete_chapter",
        section="complete_section"
    )

    # Verify all fields are present
    assert hasattr(metadata, 'url')
    assert hasattr(metadata, 'chunk_id')
    assert hasattr(metadata, 'module')
    assert hasattr(metadata, 'chapter')
    assert hasattr(metadata, 'section')

    assert metadata.url == "/docs/complete"
    assert metadata.chunk_id == "complete_123"
    assert metadata.module == "complete_module"
    assert metadata.chapter == "complete_chapter"
    assert metadata.section == "complete_section"


def test_similarity_score_range():
    """
    Test that similarity scores are within valid range
    """
    metadata = ChunkMetadata(url="/docs/test", chunk_id="test_123")

    # Valid scores
    valid_chunk = RetrievedChunk(text="test", similarity_score=0.5, metadata=metadata)
    assert valid_chunk.similarity_score == 0.5

    # Boundary values
    min_chunk = RetrievedChunk(text="test", similarity_score=0.0, metadata=metadata)
    max_chunk = RetrievedChunk(text="test", similarity_score=1.0, metadata=metadata)

    assert min_chunk.similarity_score == 0.0
    assert max_chunk.similarity_score == 1.0

    # Invalid scores should raise an error (handled by Pydantic validation)
    with pytest.raises(ValueError):
        RetrievedChunk(text="test", similarity_score=-0.1, metadata=metadata)

    with pytest.raises(ValueError):
        RetrievedChunk(text="test", similarity_score=1.1, metadata=metadata)