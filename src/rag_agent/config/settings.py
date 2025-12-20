from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Configuration
    api_title: str = "RAG Agent Backend API"
    api_description: str = "Backend service for RAG-based query processing"
    api_version: str = "1.0.0"

    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo"  # Model to use for agent orchestration

    # Cohere Configuration
    cohere_api_key: Optional[str] = None
    cohere_model: str = "embed-multilingual-v3.0"  # Model for embedding generation

    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"
    qdrant_api_key: Optional[str] = None
    qdrant_url: Optional[str] = None  # For cloud instances

    # Retrieval Configuration
    retrieval_top_k_default: int = 5
    retrieval_similarity_threshold: float = 0.5  # Minimum similarity score

    # Agent Configuration
    agent_timeout: int = 30  # Timeout for agent operations in seconds
    agent_max_retries: int = 3  # Maximum number of retries for agent operations

    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# Create a singleton instance
settings = Settings()