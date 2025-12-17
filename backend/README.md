# Docusaurus Embedding Pipeline

This project implements a Docusaurus embedding pipeline that crawls Docusaurus sites, generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval.

## Features

- Crawls Docusaurus sites to discover all accessible URLs
- Extracts clean text content while filtering out navigation elements
- Chunks text with overlap to maintain context
- Generates embeddings using Cohere API
- Stores embeddings in Qdrant vector database with metadata
- Handles rate limiting and error scenarios gracefully
- Supports command-line configuration

## Prerequisites

- Python 3.8+
- uv package manager
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment and install dependencies:

```bash
cd backend
uv venv
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
uv pip install cohere qdrant-client beautifulsoup4 requests python-dotenv langchain
```

4. Create a `.env` file with your configuration:

```env
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Configuration
QDRANT_URL=http://localhost:6333  # Optional, defaults to localhost
QDRANT_API_KEY=your_qdrant_api_key_here  # Optional

# Target Site Configuration
TARGET_URL=https://robotics-book-three.vercel.app/

# Processing Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Usage

### Basic Usage

```bash
python main.py
```

This will use the URL specified in the `TARGET_URL` environment variable.

### With Command Line Arguments

```bash
python main.py --url "https://your-docusaurus-site.com" --chunk-size 1500 --chunk-overlap 300 --collection "my_embeddings"
```

### Available Options

- `--url`: Target Docusaurus site URL (defaults to TARGET_URL env var)
- `--chunk-size`: Size of text chunks (defaults to CHUNK_SIZE env var)
- `--chunk-overlap`: Overlap between chunks (defaults to CHUNK_OVERLAP env var)
- `--collection`: Qdrant collection name (defaults to 'rag_embeddings')

## Architecture

The pipeline consists of the following components:

1. **URL Discovery**: Discovers all accessible URLs from the target Docusaurus site, including from sitemap.xml
2. **Content Extraction**: Extracts clean text content while filtering out navigation, headers, and footers
3. **Text Chunking**: Splits large documents into manageable chunks with overlap
4. **Embedding Generation**: Creates vector embeddings using Cohere API with rate limiting
5. **Vector Storage**: Stores embeddings in Qdrant with associated metadata

## Configuration

The pipeline can be configured via:

- Environment variables in `.env` file
- Command-line arguments (which override environment variables)

## Error Handling

- Network request failures are retried with exponential backoff
- Cohere API rate limits are handled with retry logic
- Individual URL processing failures don't stop the entire pipeline
- Comprehensive logging for debugging and monitoring

## Testing

To test the pipeline with the target site:

```bash
python main.py --url "https://robotics-book-three.vercel.app/"
```

## Integration with RAG Applications

The embeddings are stored in Qdrant with the following metadata:
- Content text
- Source URL
- Page title
- Chunk index and total chunks
- Additional metadata fields

This allows for semantic search and retrieval in RAG applications.

## Limitations

- The crawler respects a maximum of 100 pages to prevent infinite crawling
- Large documents are processed in chunks which may break up related content
- Rate limits from external services may slow down processing

## Future Enhancements

- Parallel processing of URLs for faster execution
- Support for additional embedding providers
- More sophisticated content filtering for Docusaurus-specific elements
- Web interface for configuration and monitoring