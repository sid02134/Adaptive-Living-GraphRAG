"""
Adaptive Living GraphRAG Framework
Full-Stack HTTP Integration & Endpoint Verification Test
Verifies all React Frontend API calls against Module 5 FastAPI backend routes.
"""

import io
import sys
import importlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient


def run_fullstack_verification():
    print("\n" + "=" * 60)
    print("FULL-STACK FRONTEND <-> BACKEND INTEGRATION VERIFICATION")
    print("=" * 60)

    # 1. Load FastAPI Application
    mod5 = importlib.import_module("Module-5_Backend_API")
    app = mod5.app
    client = TestClient(app)
    print("[SUCCESS] FastAPI Application initialized successfully!")

    # 2. Health Service Integration (GET /api/v1/health)
    print("\n[1. HEALTH SERVICE] GET /api/v1/health ...")
    res_health = client.get("/api/v1/health")
    assert res_health.status_code == 200
    health_data = res_health.json()
    print(" -> AppContext health state received:", health_data['status'])
    print(" -> Components:", list(health_data['components'].keys()))

    # 3. Dashboard Stats Integration (GET /api/v1/dashboard)
    print("\n[2. DASHBOARD SERVICE] GET /api/v1/dashboard ...")
    res_dash = client.get("/api/v1/dashboard")
    assert res_dash.status_code == 200
    dash_data = res_dash.json()
    print(f" -> Dashboard Stats: {dash_data['total_documents']} Docs | {dash_data['total_chunks']} Chunks | {dash_data['avg_trust_score']}% Avg Trust")

    # 4. Trust Breakdown Integration (GET /api/v1/trust)
    print("\n[3. TRUST SERVICE] GET /api/v1/trust ...")
    res_trust = client.get("/api/v1/trust")
    assert res_trust.status_code == 200
    trust_data = res_trust.json()
    print(f" -> Trust Metrics: Semantic={trust_data['semantic_similarity']}%, Source={trust_data['source_reliability']}%, Graph={trust_data['graph_consistency']}%, Citation={trust_data['citation_coverage']}%")

    # 5. Knowledge Graph Integration (GET /api/v1/graph)
    print("\n[4. GRAPH SERVICE] GET /api/v1/graph ...")
    res_graph = client.get("/api/v1/graph")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    print(f" -> KnowledgeGraph.jsx payload: {graph_data['total_nodes']} Nodes, {graph_data['total_edges']} Edges")

    # 6. AI Chat Service Integration (POST /api/v1/ask)
    print("\n[5. CHAT SERVICE] POST /api/v1/ask ...")
    ask_payload = {
        "query": "What are the core components of the Adaptive Living GraphRAG framework?",
        "top_k": 3,
        "alpha": 0.6
    }
    res_chat = client.post("/api/v1/ask", json=ask_payload)
    assert res_chat.status_code == 200
    chat_data = res_chat.json()
    print(f" -> AIChat.jsx Response: {chat_data['answer'][:100]}...")
    print(f" -> Trust Score: {chat_data['trust_percentage']}% ({chat_data['confidence_level']})")
    print(f" -> Citations Count: {len(chat_data['citations'])}")

    # 7. Document Upload Service Integration (POST /api/v1/upload)
    print("\n[6. DOCUMENT SERVICE] POST /api/v1/upload ...")
    valid_pdf_path = ROOT_DIR / "data" / "pdfs" / "2005.11401v4.pdf"
    with open(valid_pdf_path, "rb") as f:
        file_payload = {"file": ("2005.11401v4.pdf", f, "application/pdf")}
        res_upload = client.post("/api/v1/upload", files=file_payload)
    assert res_upload.status_code == 200
    upload_data = res_upload.json()

    print(f" -> PDFUploader.jsx Response: Status '{upload_data['status']}' for '{upload_data['filename']}' ({upload_data['chunks_processed']} chunks, {upload_data['entities_extracted']} entities)")

    print("\n" + "=" * 60)
    print("ALL FRONTEND <-> BACKEND SERVICE INTEGRATIONS VERIFIED 100%!")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    run_fullstack_verification()
