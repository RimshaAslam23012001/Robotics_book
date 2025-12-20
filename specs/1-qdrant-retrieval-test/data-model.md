# Data Model: Qdrant Vector Retrieval Pipeline

**Feature**: 1-qdrant-retrieval-test
**Date**: 2025-12-18
**Status**: Completed

## Core Entities

### 1. QueryRequest
Represents the input to the retrieval system

**Attributes**:
- `query_text` (string): The user's search query
- `top_k` (integer): Number of results to retrieve (default: 5)
- `min_score` (float): Minimum similarity threshold (optional)

**Constraints**:
- `query_text` must not be empty
- `top_k` must be between 1 and 100
- `min_score` must be between 0.0 and 1.0 if provided

### 2. EmbeddingVector
Vector representation of text for similarity search

**Attributes**:
- `vector` (array<float>): Numerical representation of text
- `dimension` (integer): Size of the vector array

**Constraints**:
- Vector dimension must match Qdrant collection configuration
- All values must be finite numbers

### 3. RetrievedChunk
A text chunk retrieved from the vector database

**Attributes**:
- `chunk_id` (string): Unique identifier for the text chunk
- `content` (string): Original text content
- `url` (string): Source URL where the content originated
- `similarity_score` (float): Semantic similarity to query (0.0-1.0)
- `metadata` (object): Additional metadata fields

**Constraints**:
- `content` must match original stored text exactly
- `similarity_score` must be between 0.0 and 1.0
- `chunk_id` must be unique within the dataset

### 4. ValidationResult
Result of content and metadata verification

**Attributes**:
- `is_content_valid` (boolean): Whether text content matches original
- `is_metadata_valid` (boolean): Whether metadata is correct
- `content_diff` (string): Description of any content differences
- `metadata_diff` (string): Description of any metadata differences

### 5. QueryResult
Complete result of a retrieval operation

**Attributes**:
- `query` (string): Original query text
- `retrieved_chunks` (array<RetrievedChunk>): Top-k matching chunks
- `processing_time` (float): Time taken for retrieval in seconds
- `validation_results` (array<ValidationResult>): Validation for each chunk

**Constraints**:
- `retrieved_chunks` count must equal requested `top_k` or available results
- `processing_time` must be positive
- All validation results must be present for returned chunks

## Qdrant Collection Schema

### Collection: `book_chunks`

**Vector Configuration**:
- `vector_size`: 1024 (for Cohere multilingual model)
- `distance`: Cosine

**Payload Fields**:
- `content` (text): The text content of the chunk
- `url` (keyword): Source URL
- `chunk_id` (keyword): Unique chunk identifier
- `source_title` (text): Title of source document (optional)

## JSON Output Format

```json
{
  "query": "string",
  "top_k": "integer",
  "retrieved_chunks": [
    {
      "chunk_id": "string",
      "content": "string",
      "url": "string",
      "similarity_score": "float",
      "metadata": {
        "source_title": "string"
      }
    }
  ],
  "processing_time": "float",
  "validation_results": [
    {
      "is_content_valid": "boolean",
      "is_metadata_valid": "boolean",
      "content_diff": "string",
      "metadata_diff": "string"
    }
  ]
}
```

## Data Flow

1. **Input**: `QueryRequest` → `EmbeddingVector` (via Cohere API)
2. **Search**: `EmbeddingVector` → Qdrant search → raw results
3. **Processing**: Raw results → `RetrievedChunk` objects
4. **Validation**: `RetrievedChunk` → `ValidationResult`
5. **Output**: Aggregated into `QueryResult`

## Validation Rules

### Content Validation
- Character-by-character comparison between retrieved and original text
- Encoding consistency check
- No truncation or corruption verification

### Metadata Validation
- URL format validation
- Chunk ID consistency check
- Cross-reference with original source mapping

### Similarity Validation
- Score within expected range (0.0-1.0)
- Top-k results in descending order of similarity
- Minimum threshold compliance if specified