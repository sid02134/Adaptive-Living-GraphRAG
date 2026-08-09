"""
Module 5: Backend API
File: chat_api.py
Purpose: APIRouter for GraphRAG question answering and chat endpoint.
"""

from fastapi import APIRouter, HTTPException, Depends
import importlib
import logging

from models import AskRequest, AskResponse

router = APIRouter(tags=["GraphRAG Chat"])
logger = logging.getLogger("backend_logger")


def get_answer_generator():
    """Dependency injection helper for AnswerGenerator pipeline."""
    try:
        from pathlib import Path
        import sys
        mod4_path = Path(__file__).resolve().parent.parent / "Module-4_LLM_Trust_Engine"
        if str(mod4_path) not in sys.path:
            sys.path.insert(0, str(mod4_path))
        import importlib
        mod4 = importlib.import_module("answer_generator")
        AnswerGenerator = getattr(mod4, "AnswerGenerator")
        return AnswerGenerator()
    except Exception as e:
        logger.error(f"Failed to load AnswerGenerator: {e}")
        return None


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
        HTTPException: If query processing fails.
    """
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    try:
        logger.info(f"Processing API query: '{payload.query}' (top_k={payload.top_k}, alpha={payload.alpha})")
        if generator is None:
            generator = get_answer_generator()

        result = generator.generate_answer(
            query=payload.query,
            top_k=payload.top_k or 5,
            alpha=payload.alpha if payload.alpha is not None else 0.6
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
    except Exception as e:
        logger.error(f"API chat query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
