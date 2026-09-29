"""
Module 6: Dynamic Knowledge Evolution
File: config.py
Purpose: Central configuration for Module 6 dynamic knowledge evolution, conflict resolution,
         trust scoring, temporal aging, and adaptive retrieval.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Module6Config:
    """Configuration settings for Module 6 Dynamic Knowledge Evolution Engine."""

    # Project Root Directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Log Directory
    LOG_DIR = str(BASE_DIR / "logs")
    LOG_FILE = str(BASE_DIR / "logs" / "module6_evolution.log")

    # Audit History File (Fallback persistent history)
    AUDIT_FILE = str(BASE_DIR / "data" / "evolution_history.json")
    CONFLICT_LOG_FILE = str(BASE_DIR / "data" / "evolution_conflicts.json")

    # Conflict Resolution Policies
    # Options: "WEIGHTED_HYBRID", "LATEST_WINS", "HIGHEST_TRUST_WINS", "PRESERVE_BOTH"
    DEFAULT_CONFLICT_POLICY = os.getenv("CONFLICT_POLICY", "WEIGHTED_HYBRID")

    # Trust Engine Weights (Must sum to 1.0)
    TRUST_WEIGHTS: Dict[str, float] = {
        "source_reliability": 0.25,
        "freshness": 0.20,
        "evidence_support": 0.20,
        "graph_agreement": 0.20,
        "retrieval_relevance": 0.15,
    }

    # Default Source Reliability Ratings (0.0 to 1.0)
    SOURCE_RELIABILITY_SCORES: Dict[str, float] = {
        "peer_reviewed_journal": 0.95,
        "official_doc": 0.90,
        "verified_database": 0.85,
        "news_article": 0.70,
        "blog_post": 0.50,
        "user_input": 0.60,
        "unknown": 0.40,
    }

    # Temporal Aging Parameters
    # Lambda decay constant for exponential decay: Freshness = exp(-LAMBDA_DECAY * days_elapsed)
    # 0.01 means ~50% decay over ~69 days
    LAMBDA_DECAY: float = float(os.getenv("LAMBDA_DECAY", "0.01"))
    
    # Threshold after which a claim is marked as "outdated" if unverified
    OUTDATED_THRESHOLD_DAYS: float = float(os.getenv("OUTDATED_THRESHOLD_DAYS", "180.0"))
    
    # Threshold for automatically archiving obsolete knowledge
    ARCHIVE_THRESHOLD_DAYS: float = float(os.getenv("ARCHIVE_THRESHOLD_DAYS", "365.0"))

    # Adaptive Retrieval Weights (Must sum to 1.0)
    ADAPTIVE_RETRIEVAL_WEIGHTS: Dict[str, float] = {
        "vector_weight": float(os.getenv("ADAPTIVE_W_VECTOR", "0.35")),
        "graph_weight": float(os.getenv("ADAPTIVE_W_GRAPH", "0.25")),
        "trust_weight": float(os.getenv("ADAPTIVE_W_TRUST", "0.20")),
        "freshness_weight": float(os.getenv("ADAPTIVE_W_FRESHNESS", "0.20")),
    }

    # Similarity Thresholds for Decision Engine (0.0 to 1.0)
    SIMILARITY_EXACT_MATCH: float = 0.92  # Fact already exists -> UPDATE/NO-OP
    SIMILARITY_CONTRADICTION_MIN: float = 0.70  # Similar context but conflicting predicate/object
    SIMILARITY_NEW_KNOWLEDGE_MAX: float = 0.45  # Low similarity -> ADD

    # Fallback to local storage if Neo4j/ChromaDB unavailable
    ALLOW_FALLBACK: bool = True
