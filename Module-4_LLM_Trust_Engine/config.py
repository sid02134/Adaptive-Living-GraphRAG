"""
Module 4: LLM + Trust Engine
File: config.py
Purpose: Configuration parameters for LLM client and Trust Engine calculation.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Module4Config:
    """Configuration class for Module 4 LLM and Trust Engine.

    Attributes:
        BASE_DIR (Path): Root project path.
        LOG_DIR (Path): Log directory path.
        LLM_LOG_FILE (Path): Path for LLM execution logs.
        TRUST_LOG_FILE (Path): Path for Trust score calculation logs.
        OLLAMA_BASE_URL (str): Base URL of local Ollama server instance.
        LLM_MODEL_NAME (str): Name of Ollama model (e.g. llama3).
        TEMPERATURE (float): LLM sampling temperature.
        WEIGHT_SEMANTIC_SIMILARITY (float): Trust formula weight for semantic similarity (40%).
        WEIGHT_SOURCE_RELIABILITY (float): Trust formula weight for source reliability (30%).
        WEIGHT_GRAPH_CONSISTENCY (float): Trust formula weight for graph consistency (20%).
        WEIGHT_CITATION_COVERAGE (float): Trust formula weight for citation coverage (10%).
    """

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    LLM_LOG_FILE: Path = LOG_DIR / "llm.log"
    TRUST_LOG_FILE: Path = LOG_DIR / "trust.log"

    # Ollama LLM Settings
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "llama3")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))

    # Trust Score Formula Weights
    WEIGHT_SEMANTIC_SIMILARITY: float = 0.40
    WEIGHT_SOURCE_RELIABILITY: float = 0.30
    WEIGHT_GRAPH_CONSISTENCY: float = 0.20
    WEIGHT_CITATION_COVERAGE: float = 0.10

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configurations to dictionary.

        Returns:
            Dict[str, Any]: Key-value configuration dictionary.
        """
        return {
            "OLLAMA_BASE_URL": cls.OLLAMA_BASE_URL,
            "LLM_MODEL_NAME": cls.LLM_MODEL_NAME,
            "TEMPERATURE": cls.TEMPERATURE,
            "WEIGHT_SEMANTIC_SIMILARITY": cls.WEIGHT_SEMANTIC_SIMILARITY,
            "WEIGHT_SOURCE_RELIABILITY": cls.WEIGHT_SOURCE_RELIABILITY,
            "WEIGHT_GRAPH_CONSISTENCY": cls.WEIGHT_GRAPH_CONSISTENCY,
            "WEIGHT_CITATION_COVERAGE": cls.WEIGHT_CITATION_COVERAGE,
        }
