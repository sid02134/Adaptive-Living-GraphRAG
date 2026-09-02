"""
Module 5: Backend API
File: test_module5.py
Purpose: Unit and integration tests for FastAPI backend routes.
"""

import sys
import asyncio
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import importlib

try:
    mod5_app = importlib.import_module("Module-5_Backend_API.app")
    app = getattr(mod5_app, "app")
    mod5_ha = importlib.import_module("Module-5_Backend_API.health_api")
    get_health_status = getattr(mod5_ha, "get_health_status")
    mod5_ca = importlib.import_module("Module-5_Backend_API.chat_api")
    ask_question = getattr(mod5_ca, "ask_question")
    mod5_ga = importlib.import_module("Module-5_Backend_API.graph_api")
    get_knowledge_graph = getattr(mod5_ga, "get_knowledge_graph")
    mod5_ta = importlib.import_module("Module-5_Backend_API.trust_api")
    get_dashboard_statistics = getattr(mod5_ta, "get_dashboard_statistics")
    get_trust_breakdown = getattr(mod5_ta, "get_trust_breakdown")
    mod5_m = importlib.import_module("Module-5_Backend_API.models")
    AskRequest = getattr(mod5_m, "AskRequest")
except Exception:
    from app import app
    from health_api import get_health_status
    from chat_api import ask_question
    from graph_api import get_knowledge_graph
    from trust_api import get_dashboard_statistics, get_trust_breakdown
    from models import AskRequest



def test_root_endpoint():
    """Test Root endpoint route."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    root_route = [r for r in app.routes if getattr(r, "path", "") == "/"][0]
    res = loop.run_until_complete(root_route.endpoint())
    assert "title" in res
    assert "health_check" in res
    print("\n[PASSED] GET / Root test")


def test_health_endpoint():
    """Test GET /api/v1/health endpoint handler."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(get_health_status())
    assert res.status in ["healthy", "degraded"]
    assert "api" in res.components
    print("[PASSED] GET /api/v1/health test")


def test_ask_endpoint():
    """Test POST /api/v1/ask endpoint handler."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    payload = AskRequest(query="What is Adaptive Living GraphRAG?", top_k=3, alpha=0.6)
    res = loop.run_until_complete(ask_question(payload, generator=None))
    assert res.query == payload.query
    assert hasattr(res, "answer")
    assert hasattr(res, "trust_score")
    assert hasattr(res, "trust_breakdown")
    print("[PASSED] POST /api/v1/ask test")


def test_graph_endpoint():
    """Test GET /api/v1/graph endpoint handler."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(get_knowledge_graph(query_entity="GraphRAG"))
    assert hasattr(res, "nodes")
    assert hasattr(res, "edges")
    assert len(res.nodes) >= 1
    print("[PASSED] GET /api/v1/graph test")


def test_dashboard_endpoint():
    """Test GET /api/v1/dashboard endpoint handler."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(get_dashboard_statistics())
    assert res.total_documents >= 1
    assert res.avg_trust_score > 0
    print("[PASSED] GET /api/v1/dashboard test")


def test_trust_endpoint():
    """Test GET /api/v1/trust endpoint handler."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(get_trust_breakdown())
    assert res.semantic_similarity > 0
    assert res.citation_coverage > 0
    print("[PASSED] GET /api/v1/trust test")


if __name__ == "__main__":
    print("\nRunning Module 5 API Integration Tests...\n" + "=" * 50)
    test_root_endpoint()
    test_health_endpoint()
    test_ask_endpoint()
    test_graph_endpoint()
    test_dashboard_endpoint()
    test_trust_endpoint()
    print("=" * 50 + "\nAll Module 5 API Tests Passed Successfully!\n")
