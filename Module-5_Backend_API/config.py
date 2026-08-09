"""
Module 5: Backend API
File: config.py
Purpose: Configuration parameters for FastAPI backend server.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Module5Config:
    """Configuration class for Module 5 Backend API.

    Attributes:
        BASE_DIR (Path): Root directory of the project.
        LOG_DIR (Path): Directory path for storing log files.
        BACKEND_LOG_FILE (Path): Path to backend operation log file.
        API_TITLE (str): FastAPI title string.
        API_VERSION (str): API version prefix string.
        HOST (str): Server host IP address.
        PORT (int): Server port number.
        CORS_ORIGINS (list): Allowed CORS origins list.
    """

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    BACKEND_LOG_FILE: Path = LOG_DIR / "backend.log"

    API_TITLE: str = "Adaptive Living GraphRAG API"
    API_VERSION: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configurations to dictionary.

        Returns:
            Dict[str, Any]: Configuration dictionary.
        """
        return {
            "API_TITLE": cls.API_TITLE,
            "API_VERSION": cls.API_VERSION,
            "HOST": cls.HOST,
            "PORT": cls.PORT,
            "CORS_ORIGINS": cls.CORS_ORIGINS,
        }
