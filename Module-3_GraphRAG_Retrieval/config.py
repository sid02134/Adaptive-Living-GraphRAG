"""
Module 3: GraphRAG Retrieval
File: config.py
Purpose: Configuration settings for Module 3 retrieval pipeline.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Module3Config:
    """Configuration class for Module 3 GraphRAG Retrieval.

    Attributes:
        BASE_DIR (Path): Root directory of the project.
        LOG_DIR (Path): Directory path for storing log files.
        RETRIEVAL_LOG_FILE (Path): Path to retrieval log file.
        TOP_K (int): Number of top documents/chunks to retrieve.
        HYBRID_ALPHA (float): Weight alpha for vector score (1-alpha for graph score).
        MIN_RELEVANCE_SCORE (float): Minimum relevance score threshold.
    """

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    RETRIEVAL_LOG_FILE: Path = LOG_DIR / "retrieval.log"

    # Retrieval Defaults
    TOP_K: int = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    HYBRID_ALPHA: float = float(os.getenv("HYBRID_ALPHA", "0.6"))
    MIN_RELEVANCE_SCORE: float = float(os.getenv("MIN_RELEVANCE_SCORE", "0.1"))

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert retrieval configuration to dictionary.

        Returns:
            Dict[str, Any]: Key-value pair configurations.
        """
        return {
            "TOP_K": cls.TOP_K,
            "HYBRID_ALPHA": cls.HYBRID_ALPHA,
            "MIN_RELEVANCE_SCORE": cls.MIN_RELEVANCE_SCORE,
        }
