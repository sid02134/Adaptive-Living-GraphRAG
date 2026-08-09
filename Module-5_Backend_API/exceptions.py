"""
Module 5: Backend API
File: exceptions.py
Purpose: Global exception handlers and error models for FastAPI.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("backend_logger")


class APIException(HTTPException):
    """Custom Base HTTP Exception for Backend API."""

    def __init__(self, status_code: int, detail: str) -> None:
        """Initialize APIException with HTTP status code and message.

        Args:
            status_code (int): HTTP status code.
            detail (str): Error message detail.
        """
        super().__init__(status_code=status_code, detail=detail)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler catching uncaught exceptions across all endpoints.

    Args:
        request (Request): FastAPI request object.
        exc (Exception): Caught exception.

    Returns:
        JSONResponse: Standardized error response.
    """
    logger.error(f"Global exception caught on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error",
            "detail": str(exc),
            "path": request.url.path
        }
    )
