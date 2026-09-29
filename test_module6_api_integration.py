"""
Root Test Script: test_module6_api_integration.py
Purpose: Verify FastAPI HTTP integration for Module 6 endpoints (/api/v1/evolution/*).
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import importlib
mod_app = importlib.import_module("Module-5_Backend_API.app")
app = getattr(mod_app, "app")


def test_evolution_api_endpoints():
    print("=" * 60)
    print("Executing Module 6 FastAPI Integration Tests")
    print("=" * 60)

    client = TestClient(app)

    # 1. GET /api/v1/evolution/status
    res_status = client.get("/api/v1/evolution/status")
    print(f"GET /api/v1/evolution/status -> {res_status.status_code}")
    assert res_status.status_code == 200
    json_status = res_status.json()
    assert json_status["status"] == "active"
    assert "decisions_summary" in json_status

    # 2. POST /api/v1/evolution/update (ADD)
    payload_add = {
        "subject": "Llama 3",
        "predicate": "developed_by",
        "object": "Meta AI",
        "source": "meta_announcement.pdf",
        "source_type": "official_doc",
        "confidence": 0.9,
        "context_chunk": "Meta AI released Llama 3 open weights model."
    }
    res_update = client.post("/api/v1/evolution/update", json=payload_add)
    print(f"POST /api/v1/evolution/update -> {res_update.status_code}")
    assert res_update.status_code == 200
    json_update = res_update.json()
    assert json_update["status"] == "success"
    assert json_update["evolution_result"]["decision"] in ["ADD", "UPDATE"]

    # 3. GET /api/v1/evolution/history
    res_hist = client.get("/api/v1/evolution/history")
    print(f"GET /api/v1/evolution/history -> {res_hist.status_code}")
    assert res_hist.status_code == 200
    assert len(res_hist.json()["history"]) > 0

    # 4. GET /api/v1/evolution/conflicts
    res_conf = client.get("/api/v1/evolution/conflicts")
    print(f"GET /api/v1/evolution/conflicts -> {res_conf.status_code}")
    assert res_conf.status_code == 200

    # 5. POST /api/v1/evolution/query (4-Factor Adaptive Retrieval)
    payload_query = {
        "query": "Who developed Llama 3?",
        "top_k": 3,
        "include_historical": False,
        "vector_weight": 0.35,
        "graph_weight": 0.25,
        "trust_weight": 0.20,
        "freshness_weight": 0.20
    }
    res_query = client.post("/api/v1/evolution/query", json=payload_query)
    print(f"POST /api/v1/evolution/query -> {res_query.status_code}")
    assert res_query.status_code == 200
    assert "adaptive_retrieval" in res_query.json()

    print("\n[SUCCESS] All Module 6 FastAPI Endpoints Passed Successfully!")


if __name__ == "__main__":
    test_evolution_api_endpoints()
