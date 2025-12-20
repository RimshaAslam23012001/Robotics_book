import pytest
from jsonschema import validate, ValidationError
from src.rag_agent.models.chunk_models import QueryResponse, RetrievedChunk, ChunkMetadata


# Define the expected JSON schema for QueryResponse
QUERY_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "similarity_score": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "chunk_id": {"type": "string"},
                            "module": {"type": ["string", "null"]},
                            "chapter": {"type": ["string", "null"]},
                            "section": {"type": ["string", "null"]}
                        },
                        "required": ["url", "chunk_id"]
                    }
                },
                "required": ["text", "similarity_score", "metadata"]
            }
        },
        "retrieval_time_ms": {"type": ["number", "null"]},
        "total_chunks_found": {"type": ["integer", "null"]}
    },
    "required": ["query", "results"]
}


def test_response_schema_compliance():
    """
    Contract test for response schema compliance
    """
    # Create a sample response using the Pydantic models
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

    response = QueryResponse(
        query="Test query",
        results=[chunk],
        retrieval_time_ms=120.5,
        total_chunks_found=1
    )

    # Convert to dict to validate against JSON schema
    response_dict = response.model_dump()

    # Validate against the schema
    try:
        validate(instance=response_dict, schema=QUERY_RESPONSE_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Response does not comply with schema: {e}")


def test_response_schema_with_multiple_chunks():
    """
    Test response schema compliance with multiple chunks
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

    response_dict = response.model_dump()

    try:
        validate(instance=response_dict, schema=QUERY_RESPONSE_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Multi-chunk response does not comply with schema: {e}")


def test_response_schema_with_empty_results():
    """
    Test response schema compliance with empty results
    """
    response = QueryResponse(
        query="No results query",
        results=[],
        retrieval_time_ms=50.0,
        total_chunks_found=0
    )

    response_dict = response.model_dump()

    try:
        validate(instance=response_dict, schema=QUERY_RESPONSE_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Empty results response does not comply with schema: {e}")


def test_response_schema_with_null_optional_fields():
    """
    Test response schema compliance with null optional fields
    """
    response = QueryResponse(
        query="Test query with nulls",
        results=[],
        retrieval_time_ms=None,
        total_chunks_found=None
    )

    response_dict = response.model_dump()

    try:
        validate(instance=response_dict, schema=QUERY_RESPONSE_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Response with null optional fields does not comply with schema: {e}")


def test_chunk_metadata_schema():
    """
    Test that chunk metadata follows the expected schema
    """
    # Test with all optional fields present
    metadata_full = ChunkMetadata(
        url="/docs/full",
        chunk_id="full_123",
        module="full_module",
        chapter="full_chapter",
        section="full_section"
    )

    # Test with only required fields
    metadata_minimal = ChunkMetadata(
        url="/docs/minimal",
        chunk_id="minimal_123"
    )

    # Both should be valid
    assert metadata_full.url == "/docs/full"
    assert metadata_full.chunk_id == "full_123"
    assert metadata_minimal.url == "/docs/minimal"
    assert metadata_minimal.chunk_id == "minimal_123"


def test_similarity_score_schema():
    """
    Test that similarity scores comply with schema constraints
    """
    metadata = ChunkMetadata(url="/docs/test", chunk_id="test_123")

    # Valid scores should work
    valid_scores = [0.0, 0.25, 0.5, 0.75, 1.0]
    for score in valid_scores:
        chunk = RetrievedChunk(text="test", similarity_score=score, metadata=metadata)
        assert chunk.similarity_score == score

    # Invalid scores should raise validation errors when creating the model
    # (Pydantic validation happens at creation time)
    with pytest.raises(ValueError):
        RetrievedChunk(text="test", similarity_score=-0.1, metadata=metadata)

    with pytest.raises(ValueError):
        RetrievedChunk(text="test", similarity_score=1.1, metadata=metadata)