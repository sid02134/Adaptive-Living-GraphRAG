# Module 5: Backend API (FastAPI)

## Purpose
Module 5 provides production-level RESTful API endpoints for PDF document uploading, GraphRAG chat querying, knowledge graph visualization, real-time trust metrics, dashboard analytics, and health status monitoring.

---

## API Router Architecture

```
FastAPI Application (app.py)
           │
           ▼
 API Version Prefix (/api/v1)
           │
 ┌─────────┼──────────────┬──────────────┬──────────────┐
 ▼         ▼              ▼              ▼              ▼
Health    Upload         Chat           Graph         Trust & Dashboard
(/health) (/upload)      (/ask)         (/graph)      (/trust, /dashboard)
```

---

## Endpoint Reference

| HTTP Method | Endpoint Path | Description |
|---|---|---|
| `GET` | `/` | Root API Metadata |
| `GET` | `/api/v1/health` | Live connection status (Neo4j, ChromaDB, Ollama, API) |
| `POST` | `/api/v1/upload` | Upload PDF and trigger ingestion & graph building |
| `POST` | `/api/v1/ask` | GraphRAG retrieval + LLM synthesis + Trust scoring |
| `GET` | `/api/v1/graph` | Fetch graph node-edge visualization data |
| `GET` | `/api/v1/dashboard` | High-level system statistics (Docs, Chunks, Entities, Trust) |
| `GET` | `/api/v1/trust` | 4-tier trust score metric breakdown |

---

## Running the Server

Launch local development server:
```bash
python Module-5_Backend_API/app.py
```
or via uvicorn:
```bash
uvicorn Module-5_Backend_API.app:app --reload --port 8000
```
Interactive OpenAPI documentation will be available at `http://localhost:8000/docs`.

---

## Testing & Execution

Run standalone API integration tests:
```bash
python Module-5_Backend_API/test_module5.py
```
