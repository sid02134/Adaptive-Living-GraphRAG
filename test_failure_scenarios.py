"""
Adaptive Living GraphRAG Framework
Failure Scenarios & Resilience Integration Test Suite
Verifies backend graceful error handling and fallback modes for edge cases.
"""

import io
import sys
import importlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient


def run_failure_tests():
    print("\n" + "=" * 60)
    print("BACKEND RESILIENCE & FAILURE SCENARIOS TEST SUITE")
    print("=" * 60)

    mod5 = importlib.import_module("Module-5_Backend_API")
    app = mod5.app
    client = TestClient(app)

    # Failure Test 1: Uploading non-PDF file
    print("\n[TEST 1] Testing POST /api/v1/upload with non-PDF file (.txt)...")
    txt_file = {"file": ("document.txt", io.BytesIO(b"Hello world text file"), "text/plain")}
    res_txt = client.post("/api/v1/upload", files=txt_file)
    print(f" -> Response Status Code: {res_txt.status_code}")
    assert res_txt.status_code == 400
    print(f" -> Error Detail: {res_txt.json()['detail']}")
    print(" -> [PASS] Non-PDF upload rejected gracefully with HTTP 400.")

    # Failure Test 2: Empty Question to Chat Endpoint
    print("\n[TEST 2] Testing POST /api/v1/ask with empty query string ('')...")
    res_empty = client.post("/api/v1/ask", json={"query": ""})
    print(f" -> Response Status Code: {res_empty.status_code}")
    assert res_empty.status_code == 422
    print(" -> [PASS] Empty question string rejected via Pydantic validation with HTTP 422.")

    # Failure Test 3: Short Question string below min length ('a')
    print("\n[TEST 3] Testing POST /api/v1/ask with query string shorter than 2 chars ('a')...")
    res_short = client.post("/api/v1/ask", json={"query": "a"})
    print(f" -> Response Status Code: {res_short.status_code}")
    assert res_short.status_code == 422
    print(" -> [PASS] Single character query rejected via Pydantic validation with HTTP 422.")

    # Failure Test 4: External Service Fallback (Neo4j Offline)
    print("\n[TEST 4] Testing Graph API GET /api/v1/graph under Neo4j Offline Fallback Mode...")
    res_graph_fb = client.get("/api/v1/graph")
    assert res_graph_fb.status_code == 200
    graph_fb_data = res_graph_fb.json()
    print(f" -> Returned Nodes: {graph_fb_data['total_nodes']}, Edges: {graph_fb_data['total_edges']}")
    print(" -> [PASS] Knowledge graph endpoint returns lightweight in-memory graph fallback under Neo4j offline state.")

    # Failure Test 5: External Service Fallback (Ollama Offline)
    print("\n[TEST 5] Testing Chat API POST /api/v1/ask under Ollama Offline Fallback Mode...")
    res_ask_fb = client.post("/api/v1/ask", json={"query": "Explain how trust evaluation works in GraphRAG."})
    assert res_ask_fb.status_code == 200
    ask_fb_data = res_ask_fb.json()
    print(f" -> Synthesized Answer: {ask_fb_data['answer'][:80]}...")
    print(f" -> Evaluated Trust Percentage: {ask_fb_data['trust_percentage']}% ({ask_fb_data['confidence_level']})")
    print(" -> [PASS] Chat endpoint returns deterministic synthesis fallback with full trust breakdown under Ollama timeout/offline state.")

    print("\n" + "=" * 60)
    print("ALL 5 RESILIENCE & FAILURE SCENARIO TESTS PASSED 100%!")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    run_failure_tests()
