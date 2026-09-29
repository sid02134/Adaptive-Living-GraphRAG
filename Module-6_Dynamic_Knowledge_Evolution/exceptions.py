"""
Module 6: Dynamic Knowledge Evolution
File: exceptions.py
Purpose: Custom exception classes for Module 6 errors.
"""


class Module6BaseException(Exception):
    """Base exception class for Module 6."""
    pass


class EvolutionEngineError(Module6BaseException):
    """Raised when knowledge evolution evaluation fails."""
    pass


class ConflictResolutionError(Module6BaseException):
    """Raised when conflict resolution engine fails to resolve competing claims."""
    pass


class TrustCalculationError(Module6BaseException):
    """Raised when trust and confidence calculation fails."""
    pass


class TemporalAgingError(Module6BaseException):
    """Raised when temporal aging processing fails."""
    pass


class AdaptiveRetrievalError(Module6BaseException):
    """Raised when adaptive retrieval fails."""
    pass


class IncrementalUpdateError(Module6BaseException):
    """Raised when incremental graph/vector updates fail."""
    pass
