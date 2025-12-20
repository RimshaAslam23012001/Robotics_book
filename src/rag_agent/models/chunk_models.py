from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from typing import List


class ChunkMetadata(BaseModel):
    """
    Metadata about the retrieved chunk
    """
    url: str = Field(..., description="Source URL of the content")
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    module: Optional[str] = Field(None, description="Module name where the content belongs")
    chapter: Optional[str] = Field(None, description="Chapter name where the content belongs")
    section: Optional[str] = Field(None, description="Section name where the content belongs")


class RetrievedChunk(BaseModel):
    """
    Contains the text content, similarity score, and metadata from the vector database
    """
    text: str = Field(..., description="The retrieved content text")
    similarity_score: float = Field(
        ...,
        description="Similarity score between 0 and 1",
        ge=0.0,
        le=1.0
    )
    metadata: ChunkMetadata = Field(..., description="Metadata about the retrieved chunk")


class QueryResponse(BaseModel):
    """
    Well-formed JSON object containing an array of retrieved chunks and associated metadata
    """
    query: str = Field(..., description="The original user query")
    results: List[RetrievedChunk] = Field(
        ...,
        description="Array of retrieved content chunks",
        min_length=0
    )
    retrieval_time_ms: Optional[float] = Field(
        None,
        description="Time taken for retrieval in milliseconds"
    )
    total_chunks_found: Optional[int] = Field(
        None,
        description="Total number of chunks found before filtering"
    )