# Data Model: RAG Agent Backend + FastAPI Integration

## Core Entities

### QueryRequest
**Description**: Represents a user query sent to the system
**Fields**:
- `query` (string, required): The text content of the user's query
- `top_k` (integer, optional, default: 5): Number of top results to retrieve
- `filters` (object, optional): Optional filters for the retrieval process

### RetrievedChunk
**Description**: Contains the text content, similarity score, and metadata from the vector database
**Fields**:
- `text` (string, required): The retrieved content text
- `similarity_score` (number, required): Similarity score between 0 and 1
- `metadata` (object, required): Metadata about the retrieved chunk
  - `url` (string, required): Source URL of the content
  - `chunk_id` (string, required): Unique identifier for the chunk
  - `module` (string, optional): Module name where the content belongs
  - `chapter` (string, optional): Chapter name where the content belongs
  - `section` (string, optional): Section name where the content belongs

### QueryResponse
**Description**: Well-formed JSON object containing an array of retrieved chunks and associated metadata
**Fields**:
- `query` (string, required): The original user query
- `results` (array of RetrievedChunk, required): Array of retrieved content chunks
- `retrieval_time_ms` (number, optional): Time taken for retrieval in milliseconds
- `total_chunks_found` (number, optional): Total number of chunks found before filtering

## API Request/Response Models

### Query API Request
```json
{
  "query": "How does humanoid robot locomotion work?",
  "top_k": 5,
  "filters": {
    "module": "locomotion",
    "chapter": "bipedal-walking"
  }
}
```

### Query API Response
```json
{
  "query": "How does humanoid robot locomotion work?",
  "results": [
    {
      "text": "Humanoid robot locomotion involves complex control systems that manage balance, gait patterns, and environmental adaptation. The process requires real-time processing of sensor data to maintain stability during movement.",
      "similarity_score": 0.94,
      "metadata": {
        "url": "/docs/robotics/locomotion/bipedal-walking",
        "chunk_id": "chunk_12345",
        "module": "locomotion",
        "chapter": "bipedal-walking",
        "section": "introduction"
      }
    }
  ],
  "retrieval_time_ms": 120,
  "total_chunks_found": 25
}
```

## Validation Rules

### QueryRequest Validation
- `query` must be a non-empty string with 1-1000 characters
- `top_k` must be between 1 and 20 (inclusive)
- If `filters` is provided, its keys must be valid filter types

### RetrievedChunk Validation
- `text` must be a non-empty string
- `similarity_score` must be a number between 0 and 1
- `metadata.url` must be a valid URL string
- `metadata.chunk_id` must be a non-empty string

### QueryResponse Validation
- `query` must match the original request query
- `results` must be an array with at least 1 item (or empty if no results)
- `results` array length must not exceed the requested `top_k` value

## State Transitions

The system is stateless with no state transitions between requests. Each query is processed independently without maintaining any session state.