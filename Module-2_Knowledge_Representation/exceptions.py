"""
Module 2: Knowledge Representation
File: exceptions.py
Purpose: Custom exception classes for Module 2 operations.
"""


class GraphRAGException(Exception):
    """Base exception for all GraphRAG framework errors."""
    pass


class EmbeddingError(GraphRAGException):
    """Raised when text embedding generation fails."""
    pass


class ChromaDBError(GraphRAGException):
    """Raised when ChromaDB collection operations or vector storage fails."""
    pass


class Neo4jConnectionError(GraphRAGException):
    """Raised when connecting or executing Cypher queries on Neo4j fails."""
    pass


class EntityExtractionError(GraphRAGException):
    """Raised when spaCy NLP entity extraction fails."""
    pass
