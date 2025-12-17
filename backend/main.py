"""
Docusaurus Embedding Pipeline
Extract text from deployed Docusaurus URLs, generate embeddings using Cohere, and store them in Qdrant.
"""
import os
import requests
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
import argparse


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
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
        cohere_api_key = os.getenv('COHERE_API_KEY')
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.cohere_client = cohere.Client(cohere_api_key)

        qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if qdrant_api_key:
            self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            self.qdrant_client = QdrantClient(url=qdrant_url)

        logger.info("Pipeline initialized successfully")

    def get_all_urls(self, base_url: str) -> List[str]:
        """
        Discover all accessible URLs from a Docusaurus site
        Handles sitemap.xml and internal linking
        """
        logger.info(f"Starting URL discovery for: {base_url}")
        urls = set()

        # Add the base URL
        urls.add(base_url)

        # Try to get URLs from sitemap
        sitemap_url = urljoin(base_url, 'sitemap.xml')
        try:
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                for loc in soup.find_all('loc'):
                    url = loc.text.strip()
                    if url.startswith(base_url):
                        urls.add(url)
                logger.info(f"Found {len(urls)} URLs from sitemap")
        except Exception as e:
            logger.warning(f"Sitemap not accessible or error occurred: {e}")

        # Crawl internal links (simple breadth-first approach)
        visited = set()
        to_visit = [base_url]
        max_pages = 100  # Prevent infinite crawling

        while to_visit and len(visited) < max_pages:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)

            try:
                response = requests.get(current_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all internal links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)

                        # Only add URLs that are within the same domain
                        if urlparse(full_url).netloc == urlparse(base_url).netloc:
                            if full_url not in visited and full_url not in to_visit:
                                # Check if it's a valid page (not an external link or file)
                                if not any(full_url.lower().endswith(ext) for ext in ['.pdf', '.doc', '.zip', '.jpg', '.png']):
                                    to_visit.append(full_url)
                                    urls.add(full_url)

            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")

        logger.info(f"Discovered total of {len(urls)} unique URLs")
        return list(urls)

    def extract_text_from_url(self, url: str) -> DocumentContent:
        """
        Extract clean text content from a single URL
        Filters out navigation, headers, footers, and other non-content elements
        """
        logger.info(f"Extracting content from: {url}")

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove unwanted elements (navigation, headers, footers, etc.)
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'button']):
            element.decompose()

        # Try to find main content areas typical in Docusaurus sites
        main_content = None
        for selector in ['.main-wrapper', 'main', '.container', '.theme-doc-markdown', '.markdown', '.doc-content']:
            main_content = soup.select_one(selector)
            if main_content:
                break

        # If no specific content container found, use the body
        if not main_content:
            main_content = soup.find('body') or soup

        # Extract text content
        text_content = main_content.get_text(separator=' ', strip=True)

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else urlparse(url).path.split('/')[-1] or 'Untitled'

        # Create document ID
        doc_id = str(uuid.uuid4())

        # Prepare metadata
        metadata = {
            'url': url,
            'title': title,
            'source': 'docusaurus',
            'created_at': time.time()
        }

        logger.info(f"Successfully extracted content from {url} ({len(text_content)} chars)")

        return DocumentContent(
            id=doc_id,
            url=url,
            title=title,
            content=text_content,
            metadata=metadata
        )

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks for embedding
        Uses recursive character splitting to maintain context
        """
        logger.info(f"Chunking text of length {len(text)} with size {chunk_size} and overlap {overlap}")

        # Simple recursive character splitting
        chunks = []
        start = 0

        while start < len(text):
            # Determine the end position
            end = start + chunk_size

            # If we're at the end, adjust the end position
            if end > len(text):
                end = len(text)
            else:
                # Try to break at a sentence or word boundary if possible
                # Look for a good breaking point near the end
                search_start = end - overlap if start > 0 else end
                for separator in ['\n\n', '\n', '. ', '! ', '? ', '; ', ': ', ' ']:
                    last_sep = text.rfind(separator, search_start, end)
                    if last_sep != -1 and last_sep > start:
                        end = last_sep + len(separator)
                        break

            # Extract the chunk
            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)

            # Move start position, considering overlap
            if start == end:  # In case we can't make progress
                start = end + 1
            else:
                start = end - overlap if end < len(text) else end

        chunk_dicts = []
        for i, chunk in enumerate(chunks):
            chunk_dict = {
                'id': str(uuid.uuid4()),
                'content': chunk,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            chunk_dicts.append(chunk_dict)

        logger.info(f"Text chunked into {len(chunk_dicts)} pieces")
        return chunk_dicts

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks using Cohere
        Handles rate limiting with retry logic and processes in batches
        """
        if not texts:
            return []

        logger.info(f"Generating embeddings for {len(texts)} text chunks")

        # Process in batches to respect API limits
        batch_size = 96  # Cohere's limit is typically 96 texts per request
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            retry_attempts = 3
            for attempt in range(retry_attempts):
                try:
                    response = self.cohere_client.embed(
                        texts=batch,
                        model="embed-multilingual-v3.0",  # Using multilingual model for broader coverage
                        input_type="search_document"
                    )

                    batch_embeddings = response.embeddings
                    all_embeddings.extend(batch_embeddings)
                    logger.debug(f"Completed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
                    break  # Success, break retry loop

                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed for batch: {e}")
                    if attempt == retry_attempts - 1:
                        raise  # Last attempt failed, re-raise the exception
                    time.sleep(2 ** attempt)  # Exponential backoff

        logger.info(f"Successfully generated {len(all_embeddings)} embeddings")
        return all_embeddings

    def create_collection(self, collection_name: str = "rag_embeddings"):
        """
        Create a Qdrant collection for storing embeddings
        Configures with appropriate parameters for text embeddings
        """
        logger.info(f"Creating Qdrant collection: {collection_name}")

        try:
            # Try to get collection info to see if it exists
            self.qdrant_client.get_collection(collection_name)
            logger.info(f"Collection {collection_name} already exists")
            return
        except:
            # Collection doesn't exist, create it
            pass

        # Assuming Cohere's multilingual model produces 1024-dimensional vectors
        vector_size = 1024

        self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

        logger.info(f"Successfully created collection {collection_name} with {vector_size}-dimensional vectors")

    def save_chunk_to_qdrant(self, chunk: Dict, embedding: List[float], metadata: Dict, collection_name: str = "rag_embeddings"):
        """
        Save a text chunk and its embedding to Qdrant with associated metadata
        """
        point = PointStruct(
            id=chunk['id'],
            vector=embedding,
            payload={
                "content": chunk['content'],
                "url": metadata.get('url', ''),
                "title": metadata.get('title', ''),
                "source": metadata.get('source', ''),
                "chunk_index": chunk.get('chunk_index', 0),
                "total_chunks": chunk.get('total_chunks', 1),
                **metadata  # Add any additional metadata
            }
        )

        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        logger.debug(f"Saved chunk {chunk['id']} to Qdrant collection {collection_name}")


def main():
    """Main function to orchestrate the entire pipeline"""
    parser = argparse.ArgumentParser(description='Docusaurus Embedding Pipeline')
    parser.add_argument('--url', type=str, default=os.getenv('TARGET_URL'),
                       help='Target Docusaurus site URL (defaults to TARGET_URL env var)')
    parser.add_argument('--chunk-size', type=int, default=int(os.getenv('CHUNK_SIZE', '1000')),
                       help='Size of text chunks (defaults to CHUNK_SIZE env var)')
    parser.add_argument('--chunk-overlap', type=int, default=int(os.getenv('CHUNK_OVERLAP', '200')),
                       help='Overlap between chunks (defaults to CHUNK_OVERLAP env var)')
    parser.add_argument('--collection', type=str, default='rag_embeddings',
                       help='Qdrant collection name')

    args = parser.parse_args()

    if not args.url:
        print("Error: No URL provided. Use --url argument or set TARGET_URL environment variable.")
        return

    logger.info(f"Starting Docusaurus Embedding Pipeline for: {args.url}")

    # Initialize pipeline
    pipeline = DocusaurusEmbeddingPipeline()

    try:
        # 1. Create collection
        pipeline.create_collection(args.collection)

        # 2. Get all URLs
        urls = pipeline.get_all_urls(args.url)
        logger.info(f"Discovered {len(urls)} URLs to process")

        # 3. Process each URL
        for i, url in enumerate(urls):
            logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

            try:
                # Extract content
                doc_content = pipeline.extract_text_from_url(url)

                # Chunk text
                chunks = pipeline.chunk_text(doc_content.content, args.chunk_size, args.chunk_overlap)

                # Process each chunk
                for chunk in chunks:
                    # Generate embedding for the chunk content
                    embeddings = pipeline.embed([chunk['content']])

                    if embeddings:
                        # Save to Qdrant
                        pipeline.save_chunk_to_qdrant(
                            chunk=chunk,
                            embedding=embeddings[0],
                            metadata=doc_content.metadata,
                            collection_name=args.collection
                        )

            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue  # Continue with next URL

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
