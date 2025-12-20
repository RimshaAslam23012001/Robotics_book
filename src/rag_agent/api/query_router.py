import logging
import time
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from src.rag_agent.models.query_models import QueryRequest
from src.rag_agent.models.chunk_models import QueryResponse
from src.rag_agent.services.agent_service import AgentService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=QueryResponse, tags=["query"])
async def query_endpoint(request: QueryRequest):
    """
    Process a user query and return relevant content chunks
    Handles various edge cases including:
    - No results found
    - Very long queries
    - Database unavailability
    - Invalid inputs
    """
    try:
        # Log the query request if debugging is enabled
        logger.debug(f"Processing query: {request.query[:50]}... with top_k: {request.top_k}")

        # Validate the request - this is handled by Pydantic models, but adding explicit checks
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 1000:
            raise HTTPException(status_code=400, detail="Query too long - maximum 1000 characters allowed")

        if request.top_k and (request.top_k < 1 or request.top_k > 20):
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")

        # Initialize the agent service
        agent_service = AgentService()

        # Record start time for performance tracking
        start_time = time.time()

        # Process the query using the agent service
        retrieved_chunks = await agent_service.process_query(request)

        # Calculate retrieval time
        retrieval_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Handle the case where no results are found
        if not retrieved_chunks:
            logger.info(f"No results found for query: {request.query[:50]}...")

        # Create the response
        response = QueryResponse(
            query=request.query,
            results=retrieved_chunks,
            retrieval_time_ms=retrieval_time,
            total_chunks_found=len(retrieved_chunks)
        )

        # Log successful query processing
        logger.debug(f"Query processed successfully, found {len(response.results)} results in {retrieval_time:.2f}ms")

        return response
    except HTTPException:
        # Re-raise HTTP exceptions (like 400, 422)
        raise
    except ValidationError as ve:
        logger.error(f"Validation error processing query: {str(ve)}")
        raise HTTPException(status_code=422, detail=f"Request validation error: {str(ve)}")
    except ConnectionError as ce:
        logger.error(f"Connection error to external service: {str(ce)}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except TimeoutError as te:
        logger.error(f"Timeout error processing query: {str(te)}")
        raise HTTPException(status_code=408, detail="Request timeout - please try again")
    except Exception as e:
        logger.error(f"Unexpected error processing query: {str(e)}")
        # Log the full exception for debugging but return a generic message to the user
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")