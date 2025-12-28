import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authentication settings
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Qdrant settings
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# OpenRouter settings (with fallback to OpenAI)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Application settings
TRANSLATION_TIMEOUT = int(os.getenv("TRANSLATION_TIMEOUT", "30"))
MAX_CONTENT_SIZE = int(os.getenv("MAX_CONTENT_SIZE", "100000"))