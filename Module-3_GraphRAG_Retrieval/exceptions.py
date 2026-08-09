"""
Module 3: GraphRAG Retrieval
File: exceptions.py
Purpose: Custom exception classes for Module 3 retrieval errors.
"""


class RetrievalError(Exception):
    """Base exception raised for errors during GraphRAG retrieval."""
    pass


class VectorSearchError(RetrievalError):
    """Raised when vector search query against ChromaDB fails."""
    pass


class GraphSearchError(RetrievalError):
    """Raised when graph traversal query against Neo4j fails."""
    pass


class ContextBuildError(RetrievalError):
    """Raised when merging or formatting retrieval context fails."""
    pass
