"""
Module 5: Backend API
File: health_api.py
Purpose: APIRouter for system health check endpoints.
"""

from fastapi import APIRouter
import urllib.request
import logging

from models import HealthResponse, ComponentStatus

router = APIRouter(tags=["Health"])
logger = logging.getLogger("backend_logger")


@router.get("/health", response_model=HealthResponse)
async def get_health_status() -> HealthResponse:
    """Get real-time operational status for Neo4j, ChromaDB, Ollama, and Backend API.

    Returns:
        HealthResponse: Health status overview of all system components.
    """
    components = {}

    # 1. API Status
    components["api"] = ComponentStatus(status="online", details="FastAPI server running smoothly")

    # 2. ChromaDB Status
    try:
        import importlib
        mod2_c = importlib.import_module("Module-2_Knowledge_Representation.chroma_manager")
        ChromaManager = getattr(mod2_c, "ChromaManager")
        cm = ChromaManager()
        stats = cm.get_stats()
        components["chromadb"] = ComponentStatus(
            status="online",
            details=f"Collection: {stats['collection_name']} ({stats['total_chunks']} chunks)"
        )
    except Exception as e:
        components["chromadb"] = ComponentStatus(status="degraded", details=f"Fallback vector mode: {e}")

    # 3. Neo4j Status
    try:
        import importlib
        mod2_n = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
        Neo4jManager = getattr(mod2_n, "Neo4jManager")
        nm = Neo4jManager()
        if nm._fallback_mode:
            components["neo4j"] = ComponentStatus(status="degraded", details="In-memory graph fallback active")
        else:
            components["neo4j"] = ComponentStatus(status="online", details="Neo4j bolt database connected")
    except Exception as e:
        components["neo4j"] = ComponentStatus(status="offline", details=str(e))

    # 4. Ollama Status
    try:
        url = "http://localhost:11434/api/tags"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                components["ollama"] = ComponentStatus(status="online", details="Ollama Llama 3 server active")
            else:
                components["ollama"] = ComponentStatus(status="degraded", details=f"HTTP {response.status}")
    except Exception as e:
        components["ollama"] = ComponentStatus(status="offline", details=f"Ollama server offline: {e}")

    overall_status = "healthy" if all(c.status == "online" for c in components.values()) else "degraded"

    return HealthResponse(
        status=overall_status,
        api_version="/api/v1",
        components=components
    )
