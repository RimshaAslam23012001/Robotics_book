from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import time
from services.openrouter_service import openrouter_service
from middleware.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    model: Optional[str] = "openai/gpt-3.5-turbo"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    query: str
    retrieval_time_ms: float
    total_chunks_found: int

@router.post("/chat/query", response_model=Dict[str, Any])
async def chat_query_endpoint(
    request: ChatRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Chat endpoint using OpenRouter API for RAG-based responses
    """
    try:
        start_time = time.time()
        logger.info(f"Processing chat query: {request.query[:50]}...")

        # Validate inputs
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long - maximum 2000 characters allowed")

        # Create messages for OpenRouter API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for a book about Physical AI & Humanoid Robotics. Answer questions based on the provided context and be concise but informative."
            },
            {
                "role": "user",
                "content": request.query
            }
        ]

        # Call OpenRouter API
        result = await openrouter_service.chat_completion(
            messages=messages,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Extract the response
        response_text = result["choices"][0]["message"]["content"] if result.get("choices") else "No response generated."

        # Calculate retrieval time
        retrieval_time = (time.time() - start_time) * 1000

        # Return response in the format expected by frontend
        response = {
            "query": request.query,
            "results": [{
                "text": response_text,
                "content": response_text,
                "similarity_score": 1.0,  # Not applicable for OpenRouter response
                "metadata": {
                    "source": "openrouter",
                    "model": request.model
                }
            }],
            "retrieval_time_ms": retrieval_time,
            "total_chunks_found": 1
        }

        logger.info(f"Chat query processed successfully in {retrieval_time:.2f}ms")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Compatibility endpoint that matches the frontend expectation
@router.post("/query", response_model=Dict[str, Any])
async def query_endpoint(
    request: ChatRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Query endpoint that matches the frontend's expected API format
    """
    try:
        start_time = time.time()
        logger.info(f"Processing query: {request.query[:50]}...")

        # Validate inputs
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long - maximum 2000 characters allowed")

        # Create messages for OpenRouter API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for a book about Physical AI & Humanoid Robotics. Answer questions based on the provided context and be concise but informative."
            },
            {
                "role": "user",
                "content": request.query
            }
        ]

        # Call OpenRouter API
        result = await openrouter_service.chat_completion(
            messages=messages,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Extract the response
        response_text = result["choices"][0]["message"]["content"] if result.get("choices") else "No response generated."

        # Calculate retrieval time
        retrieval_time = (time.time() - start_time) * 1000

        # Return response in the format expected by frontend
        response = {
            "query": request.query,
            "results": [{
                "text": response_text,
                "content": response_text,
                "similarity_score": 1.0,
                "metadata": {
                    "source": "openrouter",
                    "model": request.model
                }
            }],
            "retrieval_time_ms": retrieval_time,
            "total_chunks_found": 1
        }

        logger.info(f"Query processed successfully in {retrieval_time:.2f}ms")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")