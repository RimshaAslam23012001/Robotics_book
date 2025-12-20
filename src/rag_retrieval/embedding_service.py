import cohere
from typing import List
from src.config.settings import Settings


class CohereEmbeddingService:
    """Service for generating embeddings using Cohere API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the embedding service.

        Args:
            api_key: Cohere API key. If not provided, uses the one from settings.
        """
        self.api_key = api_key or Settings.COHERE_API_KEY
        self.client = cohere.Client(self.api_key)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            List of float values representing the embedding vector
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        response = self.client.embed(
            texts=[text],
            model="embed-multilingual-v3.0"  # Using the same model as specified in research
        )

        # Return the first (and only) embedding
        return response.embeddings[0]

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            raise ValueError("Input texts list cannot be empty")

        # Filter out empty texts
        non_empty_texts = [text for text in texts if text.strip()]
        if not non_empty_texts:
            raise ValueError("All input texts are empty")

        response = self.client.embed(
            texts=non_empty_texts,
            model="embed-multilingual-v3.0"  # Using the same model as specified in research
        )

        return response.embeddings