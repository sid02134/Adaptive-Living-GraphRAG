# Module 6: Dynamic Knowledge Evolution

## Overview
Module 6 extends the Adaptive Living GraphRAG framework by enabling the Knowledge Graph and Vector Store to evolve dynamically as new information arrives, rather than remaining static. 

---

## Distinction Between Implementations

### Current Implementation (Modules 1–5)
- **Module 1**: PDF document loading, cleaning, and text chunking.
- **Module 2**: 384-dimensional sentence embeddings (`all-MiniLM-L6-v2`), ChromaDB storage, entity/relationship extraction, and Neo4j graph building.
- **Module 3**: 2-Factor Hybrid Retrieval combining vector similarity and graph subgraphs ($S_{\text{hybrid}} = \alpha S_{\text{vec}} + (1-\alpha) S_{\text{graph}}$).
- **Module 4**: LLM answer generation (Ollama/Llama 3), citation verification, and trust score computation.
- **Module 5**: FastAPI backend REST endpoints and React + Vite frontend dashboard.

### New Implementation (Module 6)
Module 6 adds **Dynamic Knowledge Evolution**, featuring 5 modular functional engines:
1. **Adaptive Knowledge Evolution Engine**
2. **Conflict Resolution Engine**
3. **Trust & Confidence Engine**
4. **Temporal Knowledge Aging Engine**
5. **Adaptive Retrieval Engine**

---

## 1. Adaptive Knowledge Evolution Engine (`evolution_engine.py`)

### Purpose
Evaluates incoming information (claims, triples, document chunks) against existing knowledge in ChromaDB and Neo4j and decides the exact evolution action:
- **`ADD`**: Brand new fact triple.
- **`UPDATE`**: Fact already exists; update metadata or verify evidence.
- **`REPLACE`**: Updated claim superseding a previous active claim.
- **`ARCHIVE`**: Outdated knowledge explicitly marked for archiving.
- **`REJECT`**: Untrusted, malformed, or low-confidence claim.

### Input
- `incoming_data`: Dictionary containing `subject`, `predicate`, `object`, `source`, `source_type`, `timestamp`, `confidence`, `context_chunk`.

### Algorithm
1. Parse and validate triple inputs. Reject if missing required fields.
2. Calculate trust & confidence score via Engine 3. If score < 0.25, reject.
3. Search existing claims for exact matches or partial matches.
4. Trigger Engine 2 (Conflict Resolution Engine) if matching subject + predicate with differing object is detected.
5. Trigger Engine 4 (Temporal Aging Engine) if timestamp indicates old/outdated claim.
6. Handoff actionable mutation directive to `IncrementalGraphUpdater`.

### Output
- `EvolutionResult` containing decision, reasoning text, itemized trust breakdown, conflict record (if any), and incremental update summary.

---

## 2. Conflict Resolution Engine (`conflict_engine.py`)

### Purpose
Detects contradictory claims and resolves competing information using configurable policy rules without silently deleting historical data.

### Input
- `incoming_claim`: Incoming `KnowledgeClaim` object.
- `existing_claims`: List of existing active claims in the system.

### Configurable Resolution Policies
- **`WEIGHTED_HYBRID`** (Default): Combines multi-factor trust score (70%) and recency score (30%).
- **`LATEST_WINS`**: Compares timestamps; newest claim wins.
- **`HIGHEST_TRUST_WINS`**: Compares overall trust score; highest trust wins.
- **`PRESERVE_BOTH`**: Preserves both claims with `CONFLICTING` status for manual human review.

### Database Interaction
- Losing claims are marked as `SUPERSEDED` (never deleted) in Neo4j and ChromaDB.
- Conflict records are appended to `data/evolution_conflicts.json`.

---

## 3. Trust & Confidence Engine (`trust_confidence_engine.py`)

### Purpose
Extends Module 4's trust engine to compute a transparent 5-factor system confidence score $[0.0, 1.0]$.

### Input Factors & Formula
$$\text{TrustScore} = w_1 S_{\text{rel}} + w_2 S_{\text{fresh}} + w_3 S_{\text{evid}} + w_4 S_{\text{agree}} + w_5 S_{\text{relv}}$$

- **Source Reliability ($S_{\text{rel}}$)**: Journal = 0.95, Official Doc = 0.90, Database = 0.85, News = 0.70, User Input = 0.60, Blog = 0.50.
- **Freshness ($S_{\text{fresh}}$)**: Computed via exponential decay $e^{-\lambda \cdot t}$.
- **Supporting Evidence ($S_{\text{evid}}$)**: Context chunk specificity and length score.
- **Graph Agreement ($S_{\text{agree}}$)**: Alignment ratio with verified knowledge graph triples.
- **Retrieval Relevance ($S_{\text{relv}}$)**: Vector search similarity score.

*Note: The calculated score represents system-level confidence based on available evidence, not absolute real-world truth.*

---

## 4. Temporal Knowledge Aging Engine (`temporal_aging_engine.py`)

### Purpose
Manages time-aware metadata and applies configurable decay curves without automatically deleting historical knowledge.

### Mathematical Aging Formula
$$S_{\text{fresh}} = e^{-\lambda \cdot \text{days\_elapsed}}$$

- **Lambda Decay ($\lambda$)**: `0.01` (configurable via `LAMBDA_DECAY`).
- **Outdated Threshold**: `180` days (marks status as `OUTDATED`).
- **Archive Threshold**: `365` days (marks status as `ARCHIVED`).
- **Historical Retrieval**: Supports querying historical facts when `include_historical=True`.

---

## 5. Adaptive Retrieval Engine (`adaptive_retriever.py`)

### Purpose
Extends Module 3 retrieval with a 4-dimensional scoring model.

### Formula
$$\text{FinalScore} = w_1 \cdot \text{VectorScore} + w_2 \cdot \text{GraphScore} + w_3 \cdot \text{TrustScore} + w_4 \cdot \text{FreshnessScore}$$

- Default Weights: $w_1 = 0.35, w_2 = 0.25, w_3 = 0.20, w_4 = 0.20$.
- Preserves Module 3's `HybridRetriever` for backwards compatibility.

---

## 6. Incremental Graph Updater (`incremental_graph_updater.py`)

### Purpose
Executes fine-grained Cypher `MERGE` and `SET` queries in Neo4j and document updates in ChromaDB to avoid full graph reconstruction.

---

## 7. API Endpoints (`Module-5_Backend_API/evolution_api.py`)

- `POST /api/v1/evolution/update`: Evaluate incoming claim for knowledge evolution.
- `POST /api/v1/evolution/feedback`: Submit manual conflict resolution feedback.
- `GET /api/v1/evolution/history`: Retrieve decision audit log.
- `GET /api/v1/evolution/conflicts`: Retrieve flagged knowledge contradictions.
- `GET /api/v1/evolution/status`: Retrieve engine metrics & parameters.
- `POST /api/v1/evolution/query`: Execute 4-Factor Adaptive Retrieval query.

---

## 8. Testing & Verification

Comprehensive test suite in `Module-6_Dynamic_Knowledge_Evolution/test_module6.py` and `test_module6_api_integration.py` covering all 11 required scenarios and failure modes.
