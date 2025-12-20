# Quickstart: RAG Agent Backend + FastAPI Integration

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Access to OpenAI API key
- Access to Cohere API key
- Qdrant vector database instance (from Spec-002)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_HOST=your_qdrant_host
   QDRANT_PORT=6333
   QDRANT_COLLECTION_NAME=your_collection_name
   ```

## Running the Service

1. **Start the FastAPI application**:
   ```bash
   uvicorn src.rag_agent.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify the service is running**:
   - Visit `http://localhost:8000/status` to check the health endpoint
   - Visit `http://localhost:8000/docs` to access the interactive API documentation

## Making a Query

1. **Send a query to the API**:
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "How do humanoid robots maintain balance?",
       "top_k": 5
     }'
   ```

2. **Expected response**:
   ```json
   {
     "query": "How do humanoid robots maintain balance?",
     "results": [
       {
         "text": "Humanoid robots maintain balance using a combination of sensors including gyroscopes, accelerometers, and force sensors. The control system processes this data in real-time to adjust the robot's posture and prevent falls.",
         "similarity_score": 0.94,
         "metadata": {
           "url": "/docs/robotics/balance/control-systems",
           "chunk_id": "chunk_12345",
           "module": "balance",
           "chapter": "control-systems",
           "section": "sensors"
         }
       }
     ],
     "retrieval_time_ms": 120,
     "total_chunks_found": 25
   }
   ```

## API Endpoints

### GET /status
Health check endpoint to verify the service is running.

### POST /query
Main endpoint for submitting queries and receiving RAG results.

**Request body**:
```json
{
  "query": "Your query text here",
  "top_k": 5,
  "filters": {
    "module": "optional filter"
  }
}
```

**Response**:
See the example response format above.

## Testing

Run the complete test suite:
```bash
pytest tests/
```

Run specific test types:
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Contract tests
pytest tests/contract/
```

## Configuration

The service can be configured through environment variables in the `.env` file:
- `OPENAI_API_KEY`: API key for OpenAI services
- `COHERE_API_KEY`: API key for Cohere embedding services
- `QDRANT_HOST`: Host address of the Qdrant vector database
- `QDRANT_PORT`: Port of the Qdrant vector database (default: 6333)
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant to query
- `DEBUG`: Set to "True" to enable debug logging (default: "False")