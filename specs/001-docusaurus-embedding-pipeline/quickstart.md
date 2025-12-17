# Quickstart Guide: Docusaurus Embedding Pipeline

## Prerequisites
- Python 3.8+
- uv package manager
- Access to Cohere API (API key required)
- Qdrant instance (local or cloud)

## Setup Instructions

### 1. Clone/Access the Repository
```bash
cd E:\Book
```

### 2. Create Backend Directory and Initialize Project
```bash
mkdir backend
cd backend
uv venv  # Create virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv init  # Initialize new Python project
```

### 3. Install Dependencies
```bash
uv add cohere qdrant-client beautifulsoup4 requests python-dotenv langchain
```

### 4. Create Environment File
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=http://localhost:6333  # Optional, defaults to localhost
QDRANT_API_KEY=your_qdrant_api_key_here  # Optional
TARGET_URL=https://robotics-book-three.vercel.app/
```

### 5. Create the Main Application
Create `main.py` with the following structure:

```python
import os
import requests
import cohere
from qdrant_client import QdrantClient
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict
import time
from urllib.parse import urljoin, urlparse
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DocumentContent:
    """Represents extracted document content"""
    id: str
    url: str
    title: str
    content: str
    metadata: Dict

class DocusaurusEmbeddingPipeline:
    def __init__(self):
        # Initialize clients
        self.cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))
        qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if qdrant_api_key:
            self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            self.qdrant_client = QdrantClient(url=qdrant_url)

    def get_all_urls(self, base_url: str) -> List[str]:
        """Discover all accessible URLs from a Docusaurus site"""
        # Implementation goes here
        pass

    def extract_text_from_url(self, url: str) -> DocumentContent:
        """Extract clean text content from a single URL"""
        # Implementation goes here
        pass

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
        """Split text into overlapping chunks for embedding"""
        # Implementation goes here
        pass

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of text chunks"""
        # Implementation goes here
        pass

    def create_collection(self, collection_name: str = "rag_embeddings"):
        """Create a Qdrant collection for storing embeddings"""
        # Implementation goes here
        pass

    def save_chunk_to_qdrant(self, chunk: Dict, embedding: List[float], metadata: Dict):
        """Save a text chunk and its embedding to Qdrant"""
        # Implementation goes here
        pass

def main():
    """Main function to orchestrate the entire pipeline"""
    # Implementation goes here
    pass

if __name__ == "__main__":
    main()
```

## Running the Pipeline

1. Make sure your environment variables are set in the `.env` file
2. Run the pipeline:
```bash
cd backend
python main.py
```

## Testing the Pipeline

1. Start Qdrant locally (if using local instance):
```bash
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

2. Verify the target site is accessible:
```bash
curl -I https://robotics-book-three.vercel.app/
```

3. Run the pipeline and monitor logs for progress.

## Troubleshooting

- If you get API rate limit errors, implement or increase delays between requests
- If content extraction is poor, adjust the BeautifulSoup selectors
- If embeddings fail, verify your Cohere API key and quota
- If Qdrant connection fails, check your Qdrant instance is running