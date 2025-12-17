# Data Models: Docusaurus Embedding Pipeline

## Core Entities

### Document Content
Represents the extracted text from Docusaurus pages, including metadata like URL, title, and document hierarchy

```python
class DocumentContent:
    id: str                    # Unique identifier for the document
    url: str                   # Original URL of the page
    title: str                 # Page title extracted from HTML
    content: str              # Clean text content
    metadata: dict            # Additional metadata (section, category, etc.)
    created_at: datetime      # Timestamp of extraction
```

### Embedding Vector
Represents the numerical vector representation of text content, stored with associated metadata for retrieval

```python
class EmbeddingVector:
    id: str                  # Unique identifier for the embedding
    document_id: str         # Reference to source document
    vector: List[float]      # Numerical embedding vector
    text_content: str        # Original text chunk
    metadata: dict          # Metadata including URL, title, etc.
    created_at: datetime    # Timestamp of embedding generation
```

### Processing Job
Represents an individual pipeline execution with status, input URLs, and processing results

```python
class ProcessingJob:
    id: str                    # Unique identifier for the job
    status: str               # Current status (pending, running, completed, failed)
    input_urls: List[str]     # List of URLs to process
    processed_count: int      # Number of URLs successfully processed
    failed_count: int         # Number of URLs that failed
    start_time: datetime      # When the job started
    end_time: datetime        # When the job completed
    error_log: List[str]      # Log of any errors encountered
```

## Function Signatures

### URL Discovery
```python
def get_all_urls(base_url: str) -> List[str]:
    """
    Discover all accessible URLs from a Docusaurus site

    Args:
        base_url: The base URL of the Docusaurus site

    Returns:
        List of all discoverable URLs

    Raises:
        ValueError: If base_url is invalid
        ConnectionError: If unable to reach the site
    """
```

### Content Extraction
```python
def extract_text_from_url(url: str) -> DocumentContent:
    """
    Extract clean text content from a single URL

    Args:
        url: The URL to extract content from

    Returns:
        DocumentContent object with extracted content and metadata

    Raises:
        HTTPError: If URL returns non-success status
        ValueError: If content cannot be parsed
    """
```

### Text Chunking
```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
    """
    Split text into overlapping chunks for embedding

    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk
        overlap: Overlap between chunks to preserve context

    Returns:
        List of dictionaries containing text chunks and metadata
    """
```

### Embedding Generation
```python
def embed(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of text chunks

    Args:
        texts: List of text chunks to embed

    Returns:
        List of embedding vectors (each a list of floats)

    Raises:
        APIError: If Cohere API call fails
        RateLimitError: If rate limits exceeded
    """
```

### Collection Creation
```python
def create_collection(collection_name: str = "rag_embeddings"):
    """
    Create a Qdrant collection for storing embeddings

    Args:
        collection_name: Name of the collection to create
    """
```

### Vector Storage
```python
def save_chunk_to_qdrant(chunk: Dict, embedding: List[float], metadata: Dict):
    """
    Save a text chunk and its embedding to Qdrant

    Args:
        chunk: Dictionary containing the text chunk
        embedding: The embedding vector
        metadata: Additional metadata to store with the embedding
    """
```

## API Contract (Internal Functions)

The main pipeline orchestrates these functions in the following sequence:

1. `create_collection()` - Initialize vector database
2. `get_all_urls(target_url)` - Discover all pages
3. For each URL:
   - `extract_text_from_url(url)` - Extract content
   - `chunk_text(content)` - Split into chunks
   - For each chunk:
     - `embed([chunk_text])` - Generate embedding
     - `save_chunk_to_qdrant(chunk, embedding, metadata)` - Store in DB

## Error Types

### Expected Errors
- `ConnectionError`: Network connectivity issues
- `HTTPError`: HTTP status errors from target sites
- `APIError`: Issues with external APIs (Cohere, Qdrant)
- `RateLimitError`: API rate limiting
- `ValidationError`: Invalid input data
- `ParsingError`: Issues parsing HTML content

### Recovery Strategies
- Retry with exponential backoff
- Skip failed items and continue processing
- Log errors for diagnostic purposes
- Graceful degradation of functionality