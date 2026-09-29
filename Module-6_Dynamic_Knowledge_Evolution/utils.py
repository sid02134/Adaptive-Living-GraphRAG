"""
Module 6: Dynamic Knowledge Evolution
File: utils.py
Purpose: Utility helper functions for logging, timestamp calculations, decay math, and persistence.
"""

import os
import json
import math
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

try:
    from .config import Module6Config
except (ImportError, ValueError):
    from config import Module6Config


def setup_logger(name: str = "module6_logger") -> logging.Logger:
    """Configure logger for Module 6.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs(Module6Config.LOG_DIR, exist_ok=True)
        file_handler = logging.FileHandler(Module6Config.LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [Module-6] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def calculate_days_elapsed(timestamp_str: str) -> float:
    """Calculate days elapsed from given timestamp to now.

    Args:
        timestamp_str (str): ISO format timestamp string.

    Returns:
        float: Days elapsed (>= 0.0).
    """
    if not timestamp_str:
        return 0.0

    try:
        # Handle ISO strings with Z or timezone offsets
        ts_clean = timestamp_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts_clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        delta = now - dt
        days = delta.total_seconds() / 86400.0
        return max(0.0, days)
    except Exception as e:
        logger.warning(f"Could not parse timestamp '{timestamp_str}': {e}. Returning 0 days.")
        return 0.0


def calculate_exponential_decay(days_elapsed: float, lambda_decay: float = Module6Config.LAMBDA_DECAY) -> float:
    """Compute exponential decay score: Freshness = exp(-lambda * days).

    Args:
        days_elapsed (float): Days elapsed since creation/update.
        lambda_decay (float): Decay factor.

    Returns:
        float: Freshness score in range [0.0, 1.0].
    """
    if days_elapsed <= 0.0:
        return 1.0
    decay_score = math.exp(-abs(lambda_decay) * days_elapsed)
    return max(0.0, min(1.0, float(decay_score)))


def append_json_log(filepath: str, item: Dict[str, Any]) -> None:
    """Append a dictionary record to a local JSON log file for persistent audit history.

    Args:
        filepath (str): Path to JSON file.
        item (Dict[str, Any]): Data dict to append.
    """
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        data = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except Exception:
                    data = []
        data.append(item)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        logger.error(f"Failed to write to JSON audit log '{filepath}': {e}")


def load_json_log(filepath: str) -> List[Dict[str, Any]]:
    """Load audit history records from a JSON file.

    Args:
        filepath (str): Path to JSON file.

    Returns:
        List[Dict[str, Any]]: List of audit records.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read JSON audit log '{filepath}': {e}")
        return []
