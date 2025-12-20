import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Dict
from src.rag_agent.api.query_router import router as query_router
from src.rag_agent.api.status_router import router as status_router
from src.rag_agent.config.settings import settings
from src.rag_agent.config.logging_config import setup_logging


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application with security measures
    """
    # Set up logging
    setup_logging()

    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        debug=settings.debug,
        # Add security-related configurations
        docs_url="/docs" if settings.debug else None,  # Disable docs in production
        redoc_url="/redoc" if settings.debug else None  # Disable redoc in production
    )

    # Add security middleware
    # CORS middleware - restrict origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.debug else ["http://localhost", "https://localhost"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted host middleware to prevent HTTP Host header attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1", settings.api_title.replace(" ", "") + ".com"]
    )

    # Include routers
    app.include_router(query_router, prefix="/api/v1", tags=["query"])
    app.include_router(status_router, tags=["status"])

    # Add a root endpoint to provide API information
    @app.get("/")
    async def root() -> Dict:
        """
        Root endpoint providing information about the API
        """
        return {
            "message": "RAG Agent Backend API",
            "description": settings.api_description,
            "version": settings.api_version,
            "endpoints": {
                "query": "/api/v1/query (POST)",
                "status": "/status (GET)",
                "docs": "/docs (GET)",
                "redoc": "/redoc (GET)"
            }
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.rag_agent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )