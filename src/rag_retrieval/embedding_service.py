import cohere
from typing import List, Optional, Union
from src.config.settings import Settings

# Try to import Hugging Face libraries, make them optional
try:
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer, AutoModel
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    SentenceTransformer, AutoTokenizer, AutoModel = None, None, None
    torch = None


class EmbeddingService:
    """Service for generating embeddings using either Cohere API or Hugging Face models."""

    def __init__(self, provider: str = "cohere", api_key: str = None, model_name: str = None):
        """
        Initialize the embedding service.

        Args:
            provider: Either "cohere" or "huggingface"
            api_key: Cohere API key (required for Cohere provider)
            model_name: Hugging Face model name (defaults to "all-MiniLM-L6-v2" for HF)
        """
        self.provider = provider.lower()

        if self.provider == "cohere":
            self.api_key = api_key or Settings.COHERE_API_KEY
            if not self.api_key:
                raise ValueError("Cohere API key is required when using Cohere provider")
            self.client = cohere.Client(self.api_key)
        elif self.provider == "huggingface":
            if not HF_AVAILABLE:
                raise ImportError(
                    "Hugging Face libraries not available. Please install transformers, torch, and sentence-transformers."
                )
            self.model_name = model_name or "all-MiniLM-L6-v2"  # Default good model
            self.model = SentenceTransformer(self.model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'cohere' or 'huggingface'.")

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

        if self.provider == "cohere":
            response = self.client.embed(
                texts=[text],
                model="embed-multilingual-v3.0"  # Using the same model as specified in research
            )
            # Return the first (and only) embedding
            return response.embeddings[0]
        elif self.provider == "huggingface":
            embedding = self.model.encode([text], convert_to_numpy=True)
            # Convert numpy array to list of floats
            return embedding[0].tolist()

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

        if self.provider == "cohere":
            response = self.client.embed(
                texts=non_empty_texts,
                model="embed-multilingual-v3.0"  # Using the same model as specified in research
            )
            return response.embeddings
        elif self.provider == "huggingface":
            embeddings = self.model.encode(non_empty_texts, convert_to_numpy=True)
            # Convert numpy arrays to lists of floats
            return [embedding.tolist() for embedding in embeddings]