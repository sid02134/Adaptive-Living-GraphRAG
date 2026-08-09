"""
Module 2: Knowledge Representation
File: config.py
Purpose: Centralized configuration settings for Module 2.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Module2Config:
    """Configuration class for Module 2 Knowledge Representation.

    Attributes:
        BASE_DIR (Path): Root directory of the project.
        LOG_DIR (Path): Directory path for storing log files.
        GRAPH_LOG_FILE (Path): Path to the graph operation log file.
        CHROMADB_PATH (str): Path to ChromaDB persistent storage.
        COLLECTION_NAME (str): Name of the ChromaDB vector collection.
        EMBEDDING_MODEL_NAME (str): SentenceTransformer model name.
        NEO4J_URI (str): Neo4j database bolt URI.
        NEO4J_USERNAME (str): Neo4j database username.
        NEO4J_PASSWORD (str): Neo4j database password.
        SPACY_MODEL (str): spaCy NLP pipeline model name.
        BATCH_SIZE (int): Batch size for database and embedding operations.
    """

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    GRAPH_LOG_FILE: Path = LOG_DIR / "graph.log"

    # ChromaDB Settings
    CHROMADB_PATH: str = os.getenv("CHROMADB_PATH", str(BASE_DIR / "data" / "chromadb"))
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "graphrag_chunks")

    # Embedding Model Settings
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # Neo4j Graph Settings
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")

    # NLP / Entity Extraction Settings
    SPACY_MODEL: str = os.getenv("SPACY_MODEL", "en_core_web_sm")

    # Processing Settings
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "64"))

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary representation.

        Returns:
            Dict[str, Any]: Key-value pairs of configurations.
        """
        return {
            "CHROMADB_PATH": cls.CHROMADB_PATH,
            "COLLECTION_NAME": cls.COLLECTION_NAME,
            "EMBEDDING_MODEL_NAME": cls.EMBEDDING_MODEL_NAME,
            "NEO4J_URI": cls.NEO4J_URI,
            "SPACY_MODEL": cls.SPACY_MODEL,
            "BATCH_SIZE": cls.BATCH_SIZE,
        }
