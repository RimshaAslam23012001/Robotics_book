# Quickstart Guide: Qdrant Vector Retrieval Pipeline

**Feature**: 1-qdrant-retrieval-test
**Date**: 2025-12-18
**Status**: Completed

## Overview

This guide provides instructions to quickly set up and run the Qdrant vector retrieval verification pipeline. The system allows you to test that stored vectors in Qdrant can be retrieved accurately using Cohere embeddings.

## Prerequisites

- Python 3.11 or higher
- Pip package manager
- Access to Cohere API (API key required)
- Access to Qdrant vector database (URL and API key if secured)

## Setup

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here  # if secured
QDRANT_COLLECTION_NAME=book_chunks
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install required packages directly:

```bash
pip install cohere qdrant-client python-dotenv pytest
```

### 3. Verify Setup

Run the setup verification:

```bash
python -c "import cohere; import qdrant_client; print('Dependencies installed successfully')"
```

## Running the Retrieval Test

### 1. Command Line Interface

Execute a retrieval test with a query:

```bash
python -m src.cli.retrieval_tester --query "your search query here" --top-k 5
```

### 2. Available Options

- `--query`: Text query for vector search (required)
- `--top-k`: Number of results to retrieve (default: 5)
- `--min-score`: Minimum similarity threshold (default: 0.0)
- `--validate`: Enable content and metadata validation (default: true)

### 3. Example Usage

```bash
# Basic retrieval
python -m src.cli.retrieval_tester --query "machine learning concepts" --top-k 3

# With minimum score threshold
python -m src.cli.retrieval_tester --query "neural networks" --top-k 5 --min-score 0.7

# Without validation (for performance testing)
python -m src.cli.retrieval_tester --query "robotics applications" --validate false
```

## Expected Output

The system returns JSON output in the following format:

```json
{
  "query": "machine learning concepts",
  "top_k": 3,
  "retrieved_chunks": [
    {
      "chunk_id": "chunk_001",
      "content": "Machine learning is a subset of artificial intelligence...",
      "url": "https://example.com/book/chapter1",
      "similarity_score": 0.89,
      "metadata": {
        "source_title": "AI Fundamentals"
      }
    }
  ],
  "processing_time": 1.23,
  "validation_results": [
    {
      "is_content_valid": true,
      "is_metadata_valid": true,
      "content_diff": null,
      "metadata_diff": null
    }
  ]
}
```

## Programmatic Usage

### 1. Initialize Services

```python
from src.rag_retrieval.pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()
```

### 2. Perform Retrieval

```python
# Execute retrieval and get QueryResult object
result = pipeline.execute_retrieval(
    query="your query",
    top_k=5,
    min_score=0.0,
    validate=True
)

# Or get JSON output directly
json_output = pipeline.execute_retrieval_json(
    query="your query",
    top_k=5,
    min_score=0.0,
    validate=True
)
```

## Testing

### 1. Run Unit Tests

```bash
pytest tests/unit/
```

### 2. Run Integration Tests

```bash
pytest tests/integration/
```

### 3. Run Complete Test Suite

```bash
pytest tests/
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Verify your `.env` file contains correct API keys
2. **Qdrant Connection**: Ensure Qdrant URL is accessible and collection exists
3. **Embedding Mismatch**: Confirm Cohere model matches the one used for vector storage

### Verification Commands

Check Cohere connectivity:
```bash
python -c "import cohere; co = cohere.Client('your_key'); print(co.embed(texts=['test'], model='embed-multilingual-v3.0'))"
```

Check Qdrant connectivity:
```bash
python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='your_url'); print(client.get_collections())"
```

## Implementation Details

The retrieval pipeline consists of the following components:

- **Pipeline Service**: `src/rag_retrieval/pipeline.py` - Orchestrates the entire process
- **Embedding Service**: `src/rag_retrieval/embedding_service.py` - Handles Cohere API calls
- **Qdrant Client**: `src/rag_retrieval/qdrant_client.py` - Manages vector search operations
- **Validator**: `src/rag_retrieval/retrieval_validator.py` - Verifies content and metadata accuracy
- **Output Formatter**: `src/rag_retrieval/output_formatter.py` - Generates clean JSON output
- **CLI Interface**: `src/cli/retrieval_tester.py` - Command-line access to the pipeline

## Next Steps

1. Run sample queries to verify retrieval accuracy
2. Test with various query types to validate semantic matching
3. Monitor performance metrics for optimization opportunities