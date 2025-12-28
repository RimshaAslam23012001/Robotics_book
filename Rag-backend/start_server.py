"""
Simple startup script for the Chapter Urdu Translation API
"""

import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Starting Chapter Urdu Translation API...")
    print("Loading configuration from environment variables...")

    # Check for required environment variables
    # Either OPENROUTER_API_KEY or OPENAI_API_KEY should be provided
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    if not openrouter_key and not openai_key:
        print("Warning: Neither OPENROUTER_API_KEY nor OPENAI_API_KEY environment variables are set")
        print("Please set at least one of these variables in your .env file.")
        print("Using example values for testing...")

    # Run the FastAPI application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()