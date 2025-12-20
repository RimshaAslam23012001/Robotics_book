import pytest
from src.rag_agent.models.query_models import QueryRequest, RetrievedChunk, ChunkMetadata, QueryResponse


def test_query_request_model():
    """
    Unit test for QueryRequest model validation
    """
    # Test valid query request
    request = QueryRequest(
        query="What is machine learning?",
        top_k=5,
        filters={"module": "ml_basics"}
    )

    assert request.query == "What is machine learning?"
    assert request.top_k == 5
    assert request.filters == {"module": "ml_basics"}

    # Test default values
    request_default = QueryRequest(query="test query")
    assert request_default.top_k == 5  # Default value
    assert request_default.filters is None  # Default value


def test_query_request_validation():
    """
    Test QueryRequest validation constraints
    """
    # Valid case
    QueryRequest(query="valid query", top_k=10)

    # Test query length constraints
    with pytest.raises(ValueError):
        QueryRequest(query="", top_k=5)  # Empty query

    with pytest.raises(ValueError):
        QueryRequest(query="a", top_k=5)  # Minimum length check

    long_query = "a" * 1001
    with pytest.raises(ValueError):
        QueryRequest(query=long_query, top_k=5)  # Too long

    # Test top_k constraints
    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=0)  # Less than minimum

    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=21)  # Greater than maximum


def test_chunk_metadata_model():
    """
    Unit test for ChunkMetadata model
    """
    metadata = ChunkMetadata(
        url="/docs/ai/intro",
        chunk_id="chunk_123",
        module="artificial_intelligence",
        chapter="introduction",
        section="overview"
    )

    assert metadata.url == "/docs/ai/intro"
    assert metadata.chunk_id == "chunk_123"
    assert metadata.module == "artificial_intelligence"
    assert metadata.chapter == "introduction"
    assert metadata.section == "overview"

    # Test with optional fields omitted
    minimal_metadata = ChunkMetadata(
        url="/docs/test",
        chunk_id="chunk_456"
    )

    assert minimal_metadata.url == "/docs/test"
    assert minimal_metadata.chunk_id == "chunk_456"
    assert minimal_metadata.module is None
    assert minimal_metadata.chapter is None
    assert minimal_metadata.section is None


def test_retrieved_chunk_model():
    """
    Unit test for RetrievedChunk model
    """
    metadata = ChunkMetadata(
        url="/docs/test",
        chunk_id="chunk_789"
    )

    chunk = RetrievedChunk(
        text="This is a test chunk of text for retrieval.",
        similarity_score=0.85,
        metadata=metadata
    )

    assert chunk.text == "This is a test chunk of text for retrieval."
    assert chunk.similarity_score == 0.85
    assert chunk.metadata.url == "/docs/test"
    assert chunk.metadata.chunk_id == "chunk_789"

    # Test similarity score constraints
    with pytest.raises(ValueError):
        RetrievedChunk(
            text="test",
            similarity_score=-0.1,  # Less than 0
            metadata=metadata
        )

    with pytest.raises(ValueError):
        RetrievedChunk(
            text="test",
            similarity_score=1.5,  # Greater than 1
            metadata=metadata
        )


def test_query_response_model():
    """
    Unit test for QueryResponse model
    """
    metadata = ChunkMetadata(
        url="/docs/test",
        chunk_id="chunk_101"
    )

    chunk = RetrievedChunk(
        text="Sample chunk text",
        similarity_score=0.9,
        metadata=metadata
    )

    response = QueryResponse(
        query="Test query",
        results=[chunk],
        retrieval_time_ms=120.5,
        total_chunks_found=25
    )

    assert response.query == "Test query"
    assert len(response.results) == 1
    assert response.results[0].text == "Sample chunk text"
    assert response.retrieval_time_ms == 120.5
    assert response.total_chunks_found == 25

    # Test with empty results
    empty_response = QueryResponse(
        query="Empty test",
        results=[],
        retrieval_time_ms=None,
        total_chunks_found=None
    )

    assert empty_response.query == "Empty test"
    assert len(empty_response.results) == 0
    assert empty_response.retrieval_time_ms is None
    assert empty_response.total_chunks_found is None