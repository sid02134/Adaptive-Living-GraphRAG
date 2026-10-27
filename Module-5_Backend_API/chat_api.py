"""
Module 5: Backend API
File: chat_api.py
Purpose: APIRouter for GraphRAG question answering and chat endpoint.
"""

from fastapi import APIRouter, HTTPException, Depends
import importlib
import logging

try:
    from .models import AskRequest, AskResponse
except (ImportError, ValueError):
    from models import AskRequest, AskResponse

router = APIRouter(tags=["GraphRAG Chat"])
logger = logging.getLogger("backend_logger")


_answer_generator = None


def get_answer_generator():
    """Dependency injection helper for AnswerGenerator pipeline.

    Reuses a cached singleton instance to avoid duplicate model initialization.
    """
    global _answer_generator
    if _answer_generator is None:
        try:
            import importlib
            mod4 = importlib.import_module("Module-4_LLM_Trust_Engine.answer_generator")
            AnswerGenerator = getattr(mod4, "AnswerGenerator")
            _answer_generator = AnswerGenerator()
            logger.info("Initialized shared AnswerGenerator singleton instance.")
        except Exception as e:
            logger.error(f"Failed to load AnswerGenerator: {e}")
            return None
    return _answer_generator


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,
    generator=Depends(get_answer_generator)
) -> AskResponse:
    """Execute GraphRAG retrieval, LLM synthesis, and trust evaluation for user query.

    Args:
        payload (AskRequest): JSON request payload containing query, top_k, and alpha.
        generator: Injected AnswerGenerator pipeline instance.

    Returns:
        AskResponse: Structured JSON response containing answer, trust breakdown, and citations.

    Raises:
        HTTPException: If query processing fails or service is unavailable.
    """
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    gen = generator if generator is not None else get_answer_generator()
    if gen is None:
        raise HTTPException(
            status_code=503,
            detail="Answer generation service is currently unavailable. Please verify LLM and retrieval service configuration."
        )

    try:
        logger.info(f"Processing API query: '{payload.query}' (top_k={payload.top_k}, alpha={payload.alpha})")
        top_k = payload.top_k if payload.top_k is not None else 5
        alpha = payload.alpha if payload.alpha is not None else 0.6

        result = gen.generate_answer(
            query=payload.query.strip(),
            top_k=top_k,
            alpha=alpha
        )

        if not result or "answer" not in result:
            raise HTTPException(
                status_code=500,
                detail="Answer generation pipeline failed to return a valid response."
            )

        return AskResponse(
            query=result["query"],
            answer=result["answer"],
            markdown_response=result["markdown_response"],
            trust_score=result["trust_score"],
            trust_percentage=result["trust_percentage"],
            confidence_level=result["confidence_level"],
            trust_breakdown=result["trust_breakdown"],
            citations=result["citations"],
            sources=result["sources"],
            processing_time_ms=result["processing_time_ms"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API chat query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
