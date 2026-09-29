# Adaptive Living GraphRAG

## Project Title
**Adaptive Living GraphRAG: A Trust-Aware Dynamic Knowledge Evolution Framework for Real-Time LLM Retrieval**

---

## System Architecture Overview

### CURRENT IMPLEMENTATION (Modules 1–5)
- **Module 1 – Document Ingestion**: PDF document loading, cleaning, and text chunking (`pdf_loader.py`, `text_cleaner.py`, `chunker.py`, `document_manager.py`).
- **Module 2 – Knowledge Representation**: 384-dimensional vector embeddings (`all-MiniLM-L6-v2`), ChromaDB storage, spaCy NLP entity/relationship extraction, and Neo4j Knowledge Graph construction.
- **Module 3 – GraphRAG Retrieval**: 2-Factor Hybrid Retrieval combining vector search and knowledge subgraphs ($S_{\text{hybrid}} = \alpha S_{\text{vector}} + (1-\alpha) S_{\text{graph}}$).
- **Module 4 – LLM & Trust Engine**: Answer generation with Ollama/Llama 3, inline citation generation, source ranking, and multi-tier trust score calculation.
- **Module 5 – FastAPI Backend & React Frontend**: REST API server (`/api/v1/*`), OpenAPI documentation, and interactive React + Vite web dashboard.

---

### NEW IMPLEMENTATION (Module 6: Dynamic Knowledge Evolution)
Module 6 extends the system so the Knowledge Graph evolves dynamically as new information arrives instead of remaining static.

It consists of **5 Modular Functional Engines**:
1. **Adaptive Knowledge Evolution Engine** (`evolution_engine.py`): Evaluates incoming information and decides: `ADD`, `UPDATE`, `REPLACE`, `ARCHIVE`, or `REJECT`.
2. **Conflict Resolution Engine** (`conflict_engine.py`): Detects contradictory claims and applies configurable resolution policies (`WEIGHTED_HYBRID`, `LATEST_WINS`, `HIGHEST_TRUST_WINS`, `PRESERVE_BOTH`).
3. **Trust & Confidence Engine** (`trust_confidence_engine.py`): Calculates system-level confidence based on Source Reliability ($S_{\text{rel}}$), Freshness ($S_{\text{fresh}}$), Evidence ($S_{\text{evid}}$), Graph Agreement ($S_{\text{agree}}$), and Retrieval Relevance ($S_{\text{relv}}$).
4. **Temporal Knowledge Aging Engine** (`temporal_aging_engine.py`): Time-aware knowledge metadata (`created_at`, `updated_at`, `validity_status`) with exponential time decay ($S_{\text{fresh}} = e^{-\lambda t}$) and historical retrieval support.
5. **Adaptive Retrieval Engine** (`adaptive_retriever.py`): 4-Factor Adaptive Retrieval ($w_1 \text{Vector} + w_2 \text{Graph} + w_3 \text{Trust} + w_4 \text{Freshness}$).

Additionally, **Incremental Graph Updater** (`incremental_graph_updater.py`) performs fine-grained Cypher `MERGE`/`SET` mutations in Neo4j and ChromaDB vector updates without rebuilding the entire graph.

---

## FastAPI Endpoints (`/api/v1/evolution/*`)

- `POST /api/v1/evolution/update` — Submit new knowledge claims for evolution evaluation.
- `POST /api/v1/evolution/feedback` — Submit manual conflict resolution feedback.
- `GET  /api/v1/evolution/history` — Retrieve knowledge evolution decision audit log.
- `GET  /api/v1/evolution/conflicts` — Retrieve flagged knowledge conflicts.
- `GET  /api/v1/evolution/status` — Retrieve Module 6 engine status & configuration.
- `POST /api/v1/evolution/query` — Execute 4-Factor Adaptive Retrieval query.

---

## Commands to Run the Project

### 1. Run FastAPI Backend Server
```bash
# Activate virtual environment and start server
venv\Scripts\python.exe main.py
```
The FastAPI backend will start at `http://127.0.0.1:8000` with interactive docs at `http://127.0.0.1:8000/docs`.

### 2. Run React Frontend Dashboard
```bash
cd frontend
npm run dev
```
The React UI will run at `http://localhost:5173`.

### 3. Run All Test Suites
```bash
# Run Module 6 Unittests
venv\Scripts\python.exe -m unittest Module-6_Dynamic_Knowledge_Evolution/test_module6.py

# Run Module 6 API Integration Tests
venv\Scripts\python.exe test_module6_api_integration.py

# Run Complete Pytest Suite Across All Modules 1-6
venv\Scripts\python.exe -m pytest
```

---

## Team
- Siddhant Ukarde
- Riya Thopate
- Bhavesh Uchade
- Vansh Zalpuri
