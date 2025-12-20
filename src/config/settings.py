import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the RAG retrieval pipeline."""

    # Cohere settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")

    # Validation settings
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    MIN_SCORE_THRESHOLD: float = float(os.getenv("MIN_SCORE_THRESHOLD", "0.0"))

    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present."""
        required_settings = [
            cls.COHERE_API_KEY,
            cls.QDRANT_URL,
            cls.QDRANT_COLLECTION_NAME
        ]

        return all(setting for setting in required_settings)

    @classmethod
    def get_required_settings(cls) -> list:
        """Get list of required settings."""
        return [
            "COHERE_API_KEY",
            "QDRANT_URL",
            "QDRANT_COLLECTION_NAME"
        ]