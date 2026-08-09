# Module 4: LLM + Trust Engine

## Purpose
Module 4 executes Llama 3 generation via Ollama, evaluates factual trust metrics using a 4-tier weighted formula, ranks context sources, resolves cross-document conflicts, generates inline citations, and formats responses for the API/Frontend.

---

## Architecture & Workflow

```
Retrieved Context (Module 3)
           │
           ▼
┌──────────────────────────────┐
│  OllamaClient                │
│  (Llama 3 Connection)        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  TrustEvaluator              │
│  (4-Tier Formula)            │
└──────────┬───────────────────┘
           │
           ├──────────────────────────────┬──────────────────────────────┐
           ▼                              ▼                              ▼
┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│  SourceRanker        │       │  ConflictResolver    │       │  CitationGenerator   │
└──────────┬───────────┘       └──────────┬───────────┘       └──────────┬───────────┘
           │                              │                              │
           └──────────────────────────────┼──────────────────────────────┘
                                          ▼
                               ┌──────────────────────┐
                               │ ResponseFormatter    │
                               │ (Markdown & JSON)    │
                               └──────────────────────┘
```

---

## Trust Score Formula

$$\text{Trust Score } T = 0.40 \cdot S_{semantic\_similarity} + 0.30 \cdot S_{source\_reliability} + 0.20 \cdot S_{graph\_consistency} + 0.10 \cdot S_{citation\_coverage}$$

Where:
- **Semantic Similarity ($S_{semantic\_similarity}$)**: Cosine hybrid vector score of matched text chunks.
- **Source Reliability ($S_{source\_reliability}$)**: Verified source file provenance.
- **Graph Consistency ($S_{graph\_consistency}$)**: Knowledge graph node/edge connectivity density.
- **Citation Coverage ($S_{citation\_coverage}$)**: Proportion of claims grounded in citations.

---

## Class & Method Index

### 1. `OllamaClient` (`ollama_client.py`)
- `generate(prompt: str, system_prompt: Optional[str]) -> str`: Calls Ollama REST API (`/api/generate`) for Llama 3 with fallback response generation.

### 2. `TrustEvaluator` (`trust_score.py`)
- `evaluate_trust(...) -> Dict`: Computes 4-tier trust score ($T \in [0.0, 1.0]$), percentage, confidence rating, and metric breakdown.

### 3. `SourceRanker` (`source_ranker.py`)
- `rank_sources(chunks: List[Dict]) -> List[Dict]`: Ranks context sources by relevance and file provenance.

### 4. `ConflictResolver` (`conflict_resolution.py`)
- `resolve_conflicts(chunks: List[Dict]) -> Dict`: Identifies contradicting claims using negation heuristics.

### 5. `CitationGenerator` (`citation_generator.py`)
- `generate_citations(chunks: List[Dict]) -> List[Dict]`: Builds verifiable source citations.

### 6. `ResponseFormatter` (`response_formatter.py`)
- `format_frontend_response(...) -> Dict`: Standardizes outputs into Markdown, JSON, and Frontend response objects.

### 7. `AnswerGenerator` (`answer_generator.py`)
- `generate_answer(query: str, retrieval_result: Optional[Dict]) -> Dict`: Master orchestrator running the full LLM + Trust pipeline.

---

## Testing & Execution

Run standalone module unit and integration tests:
```bash
python Module-4_LLM_Trust_Engine/test_module4.py
```
