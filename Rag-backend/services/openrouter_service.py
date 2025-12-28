import os
import httpx
from typing import Dict, Any, Optional
from config import OPENAI_API_KEY

class OpenRouterService:
    """
    Service to handle OpenRouter API calls for chat completions
    """

    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Use OpenRouter API key if available, otherwise use OpenAI API key
        if self.openrouter_api_key:
            self.api_key = self.openrouter_api_key
            self.base_url = "https://openrouter.ai/api/v1"
        elif self.openai_api_key:
            self.api_key = self.openai_api_key
            self.base_url = "https://api.openai.com/v1"  # Fallback to OpenAI
        else:
            self.api_key = None
            self.base_url = "https://openrouter.ai/api/v1"  # Default to OpenRouter

        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

    async def chat_completion(
        self,
        messages: list,
        model: str = "openai/gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Make a chat completion request to OpenRouter API (or OpenAI if using OpenAI key)
        """
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY or OPENAI_API_KEY environment variable is required")

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }

        # If using OpenAI API key, adjust the model name (OpenRouter uses different format)
        if self.openai_api_key and self.api_key == self.openai_api_key:
            # Remove the "openai/" prefix for OpenAI API
            if model.startswith("openai/"):
                payload["model"] = model.replace("openai/", "")

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance
openrouter_service = OpenRouterService()