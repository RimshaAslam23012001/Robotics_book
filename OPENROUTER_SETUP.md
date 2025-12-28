# OpenRouter API Integration for Book Chatbot

This project integrates with OpenRouter API for enhanced chatbot functionality. Below are the setup instructions for both local development and Vercel deployment.

## Configuration

### Backend Setup

1. **Environment Variables**:
   - Copy `Rag-backend/.env.example` to `Rag-backend/.env`
   - Set your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```
   - Or use OpenAI API key as fallback:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

2. **Available Models**:
   - Default model: `openai/gpt-3.5-turbo`
   - Other supported models: `openai/gpt-4`, `google/gemini-pro`, etc.

### Frontend Setup

1. **Environment Variables**:
   - Copy `frontend-book/.env.example` to `frontend-book/.env`
   - Set backend URL:
     ```
     REACT_APP_BACKEND_URL=http://localhost:8000
     ```

## Local Development

1. **Start Backend**:
   ```bash
   cd Rag-backend
   pip install -r requirements.txt
   python start_server.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend-book
   npm install
   npm start
   ```

## Vercel Deployment

### Backend Deployment

1. **Environment Variables** (on Vercel):
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `OPENAI_API_KEY`: Fallback OpenAI API key (optional)
   - `QDRANT_URL`: Qdrant server URL (or leave empty for fallback mode)

2. **Build Command**:
   ```
   pip install -r requirements.txt
   ```

3. **Start Command**:
   ```
   python -m uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Frontend Deployment

1. **Environment Variables** (on Vercel):
   - `REACT_APP_BACKEND_URL`: Your deployed backend URL

## API Endpoints

- `/api/query` - Chat query endpoint using OpenRouter API
- `/api/chat/query` - Alternative chat query endpoint
- All endpoints require authentication via JWT token

## Fallback Mode

If Qdrant is not available, the system will run in fallback mode with limited functionality. Chapter content retrieval will return empty results, but the OpenRouter chat functionality will still work.

## Troubleshooting

1. **404 Errors**: Ensure the backend is running and the frontend `REACT_APP_BACKEND_URL` is set correctly
2. **API Key Issues**: Verify your OpenRouter or OpenAI API key is set correctly in the environment
3. **CORS Issues**: The backend allows all origins by default for development