"""
Hugging Face Spaces entry point for the RAG Chatbot.

This file serves as the entry point for Hugging Face Spaces deployment.
It initializes the FastAPI application that handles RAG-based queries.
"""

from src.rag_agent.main import app

# The FastAPI app instance that Hugging Face Spaces will run
# This matches the configuration in README.md: app_file: app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=7860,
        reload=False  # Disable reload in production
    )