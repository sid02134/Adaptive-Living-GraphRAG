"""
Module 3: GraphRAG Retrieval
File: utils.py
Purpose: Logging setup and score normalization utility functions.
"""

import logging
import os
from typing import List, Dict, Any
from pathlib import Path
try:
    from config import Module3Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module3_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module3Config = _mod.Module3Config


def setup_logger(name: str = "retrieval_logger") -> logging.Logger:
    """Configure logger for retrieval pipeline operations.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger logging to logs/retrieval.log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs(Module3Config.LOG_DIR, exist_ok=True)

        file_handler = logging.FileHandler(Module3Config.RETRIEVAL_LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def normalize_scores(scores: List[float]) -> List[float]:
    """Normalize a list of float scores into range [0.0, 1.0] using min-max scaling.

    Args:
        scores (List[float]): List of raw float scores.

    Returns:
        List[float]: Normalized scores.
    """
    if not scores:
        return []

    min_s = min(scores)
    max_s = max(scores)

    if max_s == min_s:
        return [1.0 if max_s > 0 else 0.0 for _ in scores]

    return [(s - min_s) / (max_s - min_s) for s in scores]
