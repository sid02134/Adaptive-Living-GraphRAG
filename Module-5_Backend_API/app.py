"""
Module 5: Backend API
File: app.py
Purpose: Main FastAPI application entrypoint with CORS, logging, and router mounts.
"""

import os
import sys
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add root directory to python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from .config import Module5Config
    from .routes import api_v1_router
    from .exceptions import global_exception_handler
except (ImportError, ValueError):
    try:
        from config import Module5Config
    except (ImportError, AttributeError):
        import importlib.util
        _cfg_path = Path(__file__).resolve().parent / "config.py"
        _spec = importlib.util.spec_from_file_location("module5_config", _cfg_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        Module5Config = _mod.Module5Config
    from routes import api_v1_router
    try:
        from exceptions import global_exception_handler
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("mod5_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        global_exception_handler = getattr(_mod, "global_exception_handler")



def setup_logger(name: str = "backend_logger") -> logging.Logger:
    """Configure logger for FastAPI backend.

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger: Configured logger logging to logs/backend.log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs(Module5Config.LOG_DIR, exist_ok=True)

        file_handler = logging.FileHandler(Module5Config.BACKEND_LOG_FILE, encoding="utf-8")
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

app = FastAPI(
    title=Module5Config.API_TITLE,
    description="Adaptive Living GraphRAG: A Trust-Aware Dynamic Knowledge Evolution Framework for Real-Time LLM Retrieval",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Module5Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Global Exception Handler
app.add_exception_handler(Exception, global_exception_handler)

# Include Versioned API Routes
app.include_router(api_v1_router)


@app.get("/", tags=["Root"])
async def root():
    """Root Endpoint returning API metadata."""
    return {
        "title": Module5Config.API_TITLE,
        "version": "1.0.0",
        "api_v1_docs": "/docs",
        "health_check": f"{Module5Config.API_VERSION}/health"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting FastAPI backend server on http://{Module5Config.HOST}:{Module5Config.PORT}")
    uvicorn.run(app, host=Module5Config.HOST, port=Module5Config.PORT)
