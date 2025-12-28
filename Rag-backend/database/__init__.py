"""
Database utilities for the translation service.

Note: For this implementation, we're using Qdrant for content storage
and a simplified approach for user sessions. In a production system,
you would likely use a traditional database like PostgreSQL or MongoDB
for user sessions and other structured data.
"""

from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# For this implementation, we're focusing on the Qdrant service
# which is already implemented in the services/qdrant_service.py
# The database module would contain traditional database operations
# if we were using SQL databases for user profiles

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./translation.db")

# For this implementation, we're focusing on the Qdrant service
# which is already implemented in the services/qdrant_service.py
# The database module would contain traditional database operations
# if we were using SQL databases for user profiles

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency for getting database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()