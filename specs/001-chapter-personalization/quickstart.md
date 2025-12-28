# Quickstart Guide: Chapter-Level Content Personalization

## Prerequisites

Before setting up the personalization system, ensure you have:

- **Node.js 18+** for frontend development
- **Python 3.9+** for backend development
- **Qdrant vector database** running (version 1.0+)
- **OpenAI API key** with appropriate permissions
- **Authentication system** configured and running
- **Docusaurus-based book application** set up

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Frontend Dependencies

Navigate to the frontend directory and install dependencies:

```bash
cd frontend-book
npm install
```

### 3. Install Backend Dependencies

Navigate to the backend directory and install dependencies:

```bash
cd ../Rag-backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_if_needed

# Authentication Configuration
AUTH_SECRET_KEY=your_auth_secret_key
AUTH_ALGORITHM=HS256

# Application Configuration
PERSONALIZATION_TIMEOUT=30  # seconds
MAX_CONTENT_SIZE=100000     # characters
```

### 5. Run the Development Servers

Start the Qdrant database (if not already running):

```bash
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

Start the backend server:

```bash
cd Rag-backend
python -m uvicorn main:app --reload --port 8000
```

Start the frontend server:

```bash
cd frontend-book
npm start
```

### 6. Verify Setup

1. Access the Docusaurus application at `http://localhost:3000`
2. Log in with your credentials
3. Navigate to any chapter
4. Verify that the "Personalize This Chapter" button appears
5. Click the button and verify that personalization works

## Development Workflow

### Running Tests

Backend tests:
```bash
cd Rag-backend
python -m pytest tests/
```

Frontend tests:
```bash
cd frontend-book
npm test
```

### API Documentation

The backend API documentation is available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

### Common Development Tasks

#### Update User Background Preferences
```bash
curl -X PUT http://localhost:8000/api/user/background \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "technicalDepth": "intermediate",
    "terminologyComplexity": "moderate",
    "exampleFocus": "mixed",
    "aiConceptLevel": "intermediate"
  }'
```

#### Request Chapter Personalization
```bash
curl -X GET http://localhost:8000/api/chapter/intro-to-robotics/personalize \
  -H "Authorization: Bearer <your-token>"
```

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
- Verify that your auth token is valid and not expired
- Check that the `AUTH_SECRET_KEY` is correctly configured

#### 2. Qdrant Connection Issues
- Ensure Qdrant is running and accessible at the configured URL
- Check that the API key (if required) is correct

#### 3. OpenAI API Errors
- Verify that your OpenAI API key is valid and has sufficient quota
- Check that your account has access to the required models

#### 4. Chapter Content Not Found
- Verify that the chapter ID exists in the Qdrant database
- Check that the chapter content is properly indexed

### Debugging Tips

1. Enable debug logging by setting `LOG_LEVEL=DEBUG` in your environment
2. Check the backend logs for detailed error information
3. Use the API documentation to test endpoints interactively
4. Verify that all required services (Qdrant, authentication) are running

## Next Steps

1. **Customize Personalization Prompts**: Modify the prompt templates in the backend to better suit your content
2. **Configure User Preferences**: Set up default user preferences based on registration information
3. **Performance Tuning**: Adjust timeout values and caching strategies based on your requirements
4. **Monitoring**: Set up monitoring and alerting for the personalization service
5. **Testing**: Add comprehensive tests for your specific use cases