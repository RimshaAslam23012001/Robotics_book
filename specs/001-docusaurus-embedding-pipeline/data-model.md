# System Architecture: Docusaurus Embedding Pipeline

## Overview
The Docusaurus Embedding Pipeline is designed as a single Python script (`main.py`) that implements an ETL (Extract, Transform, Load) process to crawl Docusaurus sites, generate embeddings, and store them in a vector database.

## Architecture Components

### 1. URL Discovery Layer
- **Purpose**: Discover and validate Docusaurus site URLs
- **Function**: `get_all_urls(base_url)`
- **Responsibility**: Generate a list of all accessible URLs from the Docusaurus site, handling sitemaps, navigation, and internal linking

### 2. Content Extraction Layer
- **Purpose**: Extract clean text content from web pages
- **Function**: `extract_text_from_url(url)`
- **Responsibility**: Fetch HTML content, parse with BeautifulSoup, extract meaningful text while filtering out navigation, headers, footers, and other non-content elements

### 3. Text Processing Layer
- **Purpose**: Split large documents into manageable chunks
- **Function**: `chunk_text(text, chunk_size=1000, overlap=200)`
- **Responsibility**: Use recursive character splitting to divide content into appropriate sizes for embedding generation

### 4. Embedding Generation Layer
- **Purpose**: Convert text chunks into vector embeddings
- **Function**: `embed(texts)`
- **Responsibility**: Call Cohere API to generate embeddings, handle rate limiting and errors

### 5. Vector Storage Layer
- **Purpose**: Store embeddings in Qdrant vector database
- **Function**: `save_chunk_to_qdrant(chunk, embedding, metadata)`
- **Responsibility**: Create Qdrant collection if needed, upsert embeddings with metadata

### 6. Collection Management
- **Purpose**: Initialize and manage the Qdrant collection
- **Function**: `create_collection(collection_name="rag_embeddings")`
- **Responsibility**: Set up the vector database collection with appropriate parameters

## Data Flow

```
[Base URL]
    ↓
[get_all_urls()] → [List of URLs]
    ↓
[extract_text_from_url()] → [Raw Text Content]
    ↓
[chunk_text()] → [Text Chunks]
    ↓
[embed()] → [Vector Embeddings]
    ↓
[save_chunk_to_qdrant()] → [Stored in Qdrant DB]
```

## Configuration Architecture

### Environment Variables
- `COHERE_API_KEY`: API key for Cohere embedding service
- `QDRANT_URL`: URL for Qdrant instance (optional, defaults to localhost)
- `QDRANT_API_KEY`: API key for Qdrant (optional)
- `TARGET_URL`: Base URL of the Docusaurus site to crawl

### Dependencies
- cohere: For embedding generation
- qdrant-client: For vector database interaction
- beautifulsoup4: For HTML parsing
- requests: For HTTP requests
- langchain: For text splitting utilities

## Error Handling & Resilience

### Retry Mechanisms
- HTTP request retries for failed URL fetches
- Exponential backoff for API rate limiting
- Graceful degradation when individual URLs fail

### Logging & Monitoring
- Structured logging for pipeline progress
- Error reporting for failed extractions/embeddings
- Performance metrics for processing speed

## Scalability Considerations

### Batching
- Process URLs in batches to respect rate limits
- Batch embeddings for efficient API usage
- Parallel processing of independent URLs (optional future enhancement)

### Resource Management
- Memory-efficient processing of large documents
- Connection pooling for database and API calls
- Cleanup of temporary resources