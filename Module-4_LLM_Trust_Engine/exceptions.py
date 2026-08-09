"""
Module 4: LLM + Trust Engine
File: exceptions.py
Purpose: Custom exception classes for Module 4 operations.
"""


class Module4Exception(Exception):
    """Base exception for Module 4 LLM and Trust Engine errors."""
    pass


class LLMConnectionError(Module4Exception):
    """Raised when Ollama connection or generation fails."""
    pass


class TrustScoreError(Module4Exception):
    """Raised when trust evaluation or calculation fails."""
    pass


class ConflictResolutionError(Module4Exception):
    """Raised when conflict resolution fails."""
    pass
