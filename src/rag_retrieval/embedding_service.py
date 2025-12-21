import cohere
import logging
from typing import List, Optional, Union
from src.rag_agent.config.settings import settings

logger = logging.getLogger(__name__)

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
            self.api_key = api_key or settings.cohere_api_key
            if not self.api_key:
                logger.warning("Cohere API key not provided, falling back to Hugging Face")
                self.provider = "huggingface"
                # Fall through to huggingface setup
            else:
                try:
                    self.client = cohere.Client(self.api_key)
                except Exception as e:
                    logger.warning(f"Cohere client initialization failed: {e}, falling back to Hugging Face")
                    self.provider = "huggingface"

        if self.provider == "huggingface":
            if not HF_AVAILABLE:
                logger.warning("Hugging Face libraries not available, using mock embeddings")
                self.use_mock = True
            else:
                try:
                    self.model_name = model_name or "all-MiniLM-L6-v2"  # Default good model
                    self.model = SentenceTransformer(self.model_name)
                    self.use_mock = False
                except Exception as e:
                    logger.warning(f"Hugging Face model initialization failed: {e}, using mock embeddings")
                    self.use_mock = True
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

        if hasattr(self, 'use_mock') and self.use_mock:
            # Return a mock embedding when no provider is available
            logger.warning("Using mock embedding due to provider unavailability")
            return [0.01] * 384  # Standard size for sentence transformer models

        if self.provider == "cohere":
            try:
                response = self.client.embed(
                    texts=[text],
                    model="embed-multilingual-v3.0"  # Using the same model as specified in research
                )
                # Return the first (and only) embedding
                return response.embeddings[0]
            except Exception as e:
                logger.warning(f"Cohere embedding generation failed: {e}, using mock embedding")
                return [0.01] * 1024  # Standard size for Cohere models
        elif self.provider == "huggingface":
            try:
                embedding = self.model.encode([text], convert_to_numpy=True)
                # Convert numpy array to list of floats
                return embedding[0].tolist()
            except Exception as e:
                logger.warning(f"Hugging Face embedding generation failed: {e}, using mock embedding")
                return [0.01] * 384  # Standard size for sentence transformer models

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

        if hasattr(self, 'use_mock') and self.use_mock:
            # Return mock embeddings when no provider is available
            logger.warning("Using mock embeddings due to provider unavailability")
            embedding_size = 384  # Standard for sentence transformer models
            return [[0.01] * embedding_size for _ in non_empty_texts]

        if self.provider == "cohere":
            try:
                response = self.client.embed(
                    texts=non_empty_texts,
                    model="embed-multilingual-v3.0"  # Using the same model as specified in research
                )
                return response.embeddings
            except Exception as e:
                logger.warning(f"Cohere embeddings generation failed: {e}, using mock embeddings")
                embedding_size = 1024  # Standard for Cohere models
                return [[0.01] * embedding_size for _ in non_empty_texts]
        elif self.provider == "huggingface":
            try:
                embeddings = self.model.encode(non_empty_texts, convert_to_numpy=True)
                # Convert numpy arrays to lists of floats
                return [embedding.tolist() for embedding in embeddings]
            except Exception as e:
                logger.warning(f"Hugging Face embeddings generation failed: {e}, using mock embeddings")
                embedding_size = 384  # Standard for sentence transformer models
                return [[0.01] * embedding_size for _ in non_empty_texts]