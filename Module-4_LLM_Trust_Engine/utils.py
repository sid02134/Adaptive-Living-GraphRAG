"""
Module 4: LLM + Trust Engine
File: utils.py
Purpose: Loggers and utility formatting functions for Module 4.
"""

import logging
import os
from pathlib import Path
try:
    from config import Module4Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module4_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module4Config = _mod.Module4Config


def setup_logger(name: str, log_file: Path) -> logging.Logger:
    """Setup dedicated logger instance.

    Args:
        name (str): Logger identifier.
        log_file (Path): Path to log file.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs(Module4Config.LOG_DIR, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
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


llm_logger = setup_logger("llm_logger", Module4Config.LLM_LOG_FILE)
trust_logger = setup_logger("trust_logger", Module4Config.TRUST_LOG_FILE)


def clamp(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp float value within range [min_val, max_val].

    Args:
        val (float): Numeric value.
        min_val (float): Lower bound.
        max_val (float): Upper bound.

    Returns:
        float: Clamped value.
    """
    return max(min_val, min(max_val, val))
