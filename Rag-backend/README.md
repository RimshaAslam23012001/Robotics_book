# Chapter Urdu Translation API

This is the backend service for the chapter Urdu translation feature. It provides endpoints for translating book chapters to Urdu based on user authentication.

## Features

- Chapter content retrieval from Qdrant
- Urdu translation using OpenAI API
- Authentication middleware for secure access
- FastAPI-based REST API with automatic documentation

## Prerequisites

- Python 3.9+
- Qdrant vector database
- OpenAI API key
- Node.js 18+ (for frontend integration)

## Installation

1. Install Python dependencies:
```bash
cd Rag-backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

3. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

## API Documentation

The API documentation is available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Endpoints

### Chapter Content
- `GET /api/chapter/{chapterId}` - Get original chapter content

### Translation
- `GET /api/chapter/{chapterId}/translate/urdu` - Translate a chapter to Urdu

## Configuration

The service can be configured using environment variables in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL for the Qdrant service
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `AUTH_SECRET_KEY`: Secret key for JWT token signing
- `TRANSLATION_TIMEOUT`: Timeout for translation requests in seconds
- `MAX_CONTENT_SIZE`: Maximum content size in characters

## Running Tests

```bash
python -m pytest tests/
```

## Architecture

The service follows a clean architecture pattern:

- **Models**: Data models using Pydantic
- **Services**: Business logic in service classes
- **Routers**: API endpoints using FastAPI
- **Middleware**: Authentication and other middleware
- **Utils**: Utility functions and helpers
- **Schemas**: API response schemas

## Integration

This service is designed to integrate with a Docusaurus-based frontend. The frontend can use the `/api/translation` endpoints to translate chapter content to Urdu based on user authentication.