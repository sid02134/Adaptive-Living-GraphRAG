"""
Adaptive Living GraphRAG Framework
Full End-to-End Backend Integration Test (Modules 1 -> 2 -> 3 -> 4 -> 5)
"""

import sys
import importlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient


def run_full_integration_test():
    print("\n" + "=" * 60)
    print("FULL GRAPH RAG BACKEND INTEGRATION TEST (MODULES 1-5)")
    print("=" * 60)

    # 1. Package Import Verification
    print("\n[STEP 1] Verifying Root-Level Module Package Imports (Modules 1-5)...")
    mod1 = importlib.import_module("Module-1_Document_Ingestion")
    mod2 = importlib.import_module("Module-2_Knowledge_Representation")
    mod3 = importlib.import_module("Module-3_GraphRAG_Retrieval")
    mod4 = importlib.import_module("Module-4_LLM_Trust_Engine")
    mod5 = importlib.import_module("Module-5_Backend_API")

    app = mod5.app
    client = TestClient(app)
    print(" -> All 5 root package modules imported cleanly!")

    # 2. GET / Root API Status
    print("\n[STEP 2] Testing GET / Root API Status...")
    res_root = client.get("/")
    assert res_root.status_code == 200
    print(f" -> Root Endpoint Output: {res_root.json()['title']}")

    # 3. GET /api/v1/health API Health Check
    print("\n[STEP 3] Testing GET /api/v1/health Component Health Status...")
    res_health = client.get("/api/v1/health")
    assert res_health.status_code == 200
    health_data = res_health.json()
    print(f" -> Health Status: {health_data['status'].upper()}")

    for comp, info in health_data['components'].items():
        print(f"    - {comp}: {info['status']}")

    # 4. POST /api/v1/ask Full End-to-End GraphRAG Chat Request
    print("\n[STEP 4] Testing POST /api/v1/ask GraphRAG Pipeline (Module 1->2->3->4->5)...")
    payload = {
        "query": "How does Adaptive Living GraphRAG achieve trust-aware knowledge evolution?",
        "top_k": 3,
        "alpha": 0.6
    }
    res_ask = client.post("/api/v1/ask", json=payload)
    assert res_ask.status_code == 200
    ask_data = res_ask.json()

    print(f" -> Query: '{ask_data['query']}'")
    print(f" -> Answer Synthesis: {ask_data['answer'][:120]}...")
    print(f" -> Trust Score: {ask_data['trust_score'] * 100:.1f}% ({ask_data['confidence_level']})")
    print(f" -> Citations Returned: {len(ask_data['citations'])} source document(s)")

    # 5. GET /api/v1/graph Knowledge Graph Data
    print("\n[STEP 5] Testing GET /api/v1/graph Knowledge Graph Endpoint...")
    res_graph = client.get("/api/v1/graph")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    print(f" -> Graph Visualizer Nodes: {graph_data['total_nodes']}, Edges: {graph_data['total_edges']}")

    # 6. GET /api/v1/dashboard Analytics Dashboard
    print("\n[STEP 6] Testing GET /api/v1/dashboard Statistics...")
    res_dash = client.get("/api/v1/dashboard")
    assert res_dash.status_code == 200
    dash_data = res_dash.json()
    print(f" -> Total Documents: {dash_data['total_documents']}, Total Chunks: {dash_data['total_chunks']}")
    print(f" -> Average System Trust: {dash_data['avg_trust_score']}%")


    print("\n" + "=" * 60)
    print("FULL GRAPH RAG BACKEND INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    run_full_integration_test()
