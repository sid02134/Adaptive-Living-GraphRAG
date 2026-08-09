"""
Module 2: Knowledge Representation
File: utils.py
Purpose: Logging initialization and utility helper functions.
"""

import logging
import os
import re
from pathlib import Path
from typing import List, Any
try:
    from config import Module2Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module2_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module2Config = _mod.Module2Config


def setup_logger(name: str = "graph_logger") -> logging.Logger:
    """Set up and configure standard logger for Module 2 operations.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance logging to file and console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Create log directory if it doesn't exist
        os.makedirs(Module2Config.LOG_DIR, exist_ok=True)

        # File Handler
        file_handler = logging.FileHandler(Module2Config.GRAPH_LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
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


def clean_entity_text(text: str) -> str:
    """Normalize and clean extracted entity text.

    Args:
        text (str): Raw extracted entity string.

    Returns:
        str: Cleaned canonical entity string.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text.title()


def chunk_iterable(iterable: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into smaller chunks for batch processing.

    Args:
        iterable (List[Any]): List of items to partition.
        chunk_size (int): Size of each chunk.

    Returns:
        List[List[Any]]: List of chunked sub-lists.
    """
    return [iterable[i:i + chunk_size] for i in range(0, len(iterable), chunk_size)]
