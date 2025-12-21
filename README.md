---
title: RAG Chatbot with Hugging Face Integration
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "0.25.0"
app_file: app.py
pinned: false
---

# RAG Chatbot with Hugging Face Integration

This repository contains a Retrieval-Augmented Generation (RAG) chatbot that can answer questions based on your documentation using advanced embedding techniques.

## Features

- **Multi-provider Embedding Support**: Choose between Cohere or Hugging Face models for generating embeddings
- **Qdrant Vector Storage**: Efficiently stores and retrieves document embeddings
- **Docusaurus Content Extraction**: Automatically extracts content from Docusaurus-based documentation sites
- **Configurable Parameters**: Adjustable chunk size, overlap, and retrieval settings

## Architecture

The system consists of:
- **Embedding Service**: Supports both Cohere and Hugging Face models for text embedding generation
- **Qdrant Client**: Vector database for efficient similarity search
- **Retrieval Service**: Finds relevant document chunks based on query similarity
- **API Layer**: FastAPI-based endpoints for querying and management

## Configuration

The application can be configured via environment variables:

- `COHERE_API_KEY`: Your Cohere API key (required if using Cohere provider)
- `QDRANT_URL`: URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if applicable)
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings
- `EMBEDDING_PROVIDER`: Either 'cohere' or 'huggingface'
- `HF_MODEL_NAME`: Hugging Face model name (default: 'all-MiniLM-L6-v2')

## Usage

1. **To run the embedding pipeline:**
   ```bash
   python main.py --url YOUR_DOCS_URL --embedding-provider huggingface
   ```

2. **To specify a custom Hugging Face model:**
   ```bash
   python main.py --url YOUR_DOCS_URL --embedding-provider huggingface --hf-model sentence-transformers/all-mpnet-base-v2
   ```

## Environment Setup

Create a `.env` file with your configuration:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=rag_embeddings
EMBEDDING_PROVIDER=huggingface
HF_MODEL_NAME=all-MiniLM-L6-v2
```

## Supported Embedding Models

- **Cohere**: `embed-multilingual-v3.0` (default)
- **Hugging Face**: Various sentence transformer models including:
  - `all-MiniLM-L6-v2` (default)
  - `all-mpnet-base-v2`
  - `paraphrase-multilingual-MiniLM-L12-v2`

## License

This project is licensed under the MIT License.
