# Module 3: GraphRAG Retrieval

## Purpose
Module 3 provides dual vector and knowledge graph retrieval engines, performing weighted score fusion ($S_{hybrid} = \alpha S_{vector} + (1-\alpha) S_{graph}$), context building, and prompt generation for Llama 3 LLM synthesis.

---

## Workflow Architecture

```
User Query
    │
    ├─────────────────────────────┐
    ▼                             ▼
┌──────────────────────┐   ┌──────────────────────┐
│ VectorRetriever      │   │ GraphRetriever       │
│ (ChromaDB Vector)    │   │ (Neo4j Subgraphs)    │
└──────────┬───────────┘   └──────────┬───────────┘
           │                          │
           └──────────────┬───────────┘
                          ▼
             ┌──────────────────────────┐
             │ HybridRetriever          │
             │ (Weighted Score Fusion)  │
             └────────────┬─────────────┘
                          ▼
             ┌──────────────────────────┐
             │ ContextBuilder           │
             │ (Markdown Formatting)    │
             └────────────┬─────────────┘
                          ▼
             ┌──────────────────────────┐
             │ PromptBuilder            │
             │ (Llama 3 Prompt Pair)    │
             └──────────────────────────┘
```

---

## Formula

$$\text{Hybrid Score } S_{hybrid} = \alpha \cdot S_{vector} + (1 - \alpha) \cdot S_{graph}$$

where:
- $\alpha \in [0.0, 1.0]$ is the configurable vector score weight (default = `0.6`).
- $S_{vector}$ is the normalized ChromaDB cosine similarity score.
- $S_{graph}$ is the graph entity-chunk connection score.

---

## Class & Method Index

### 1. `VectorRetriever` (`vector_retriever.py`)
- `retrieve(query: str, top_k: int) -> List[Dict]`: Fetches semantically similar text chunks from ChromaDB.

### 2. `GraphRetriever` (`graph_retriever.py`)
- `retrieve(query: str, top_k: int) -> Dict`: Traverses Neo4j entity graph for subgraphs, nodes, and linked chunks.

### 3. `HybridRetriever` (`hybrid_retriever.py`)
- `retrieve(query: str, top_k: int, alpha: Optional[float]) -> Dict`: Fuses vector and graph scores, re-ranks items, and returns top-k chunks.

### 4. `ContextBuilder` (`context_builder.py`)
- `build_context(retrieval_output: Dict) -> str`: Merges text chunks and graph triplets into structured Markdown context.

### 5. `PromptBuilder` (`prompt_builder.py`)
- `build_prompt(query: str, context: str) -> Dict`: Constructs system and user prompts for Llama 3.

### 6. `GraphRAGRetriever` (`retriever.py`)
- `run_retrieval_pipeline(query: str, top_k: int, alpha: float) -> Dict`: Master orchestrator running vector search, graph search, context fusion, and prompt building.

---

## Testing & Execution

Run standalone module unit and integration tests:
```bash
python Module-3_GraphRAG_Retrieval/test_module3.py
```
