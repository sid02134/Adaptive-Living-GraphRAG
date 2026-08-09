"""
Module 3: GraphRAG Retrieval
File: test_module3.py
Purpose: Unit and integration tests for Module 3 components.
"""

import sys
from pathlib import Path

# Add Module 3 directory to path
sys.path.append(str(Path(__file__).resolve().parent))

try:
    from config import Module3Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module3_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module3Config = _mod.Module3Config
from vector_retriever import VectorRetriever
from graph_retriever import GraphRetriever
from hybrid_retriever import HybridRetriever
from context_builder import ContextBuilder
from prompt_builder import PromptBuilder
from retriever import GraphRAGRetriever


def test_vector_retriever():
    """Test standalone vector retriever."""
    vr = VectorRetriever()
    res = vr.retrieve("test query", top_k=2)
    assert isinstance(res, list)
    print("\n[PASSED] VectorRetriever test")


def test_graph_retriever():
    """Test standalone graph retriever."""
    gr = GraphRetriever()
    res = gr.retrieve("Neo4j knowledge graph", top_k=2)
    assert "subgraph" in res
    assert "query_entities" in res
    print("[PASSED] GraphRetriever test")


def test_hybrid_retriever():
    """Test hybrid weighted retrieval formula."""
    hr = HybridRetriever(alpha=0.7)
    res = hr.retrieve("GraphRAG hybrid search", top_k=3)
    assert "chunks" in res
    assert "alpha" in res
    assert res["alpha"] == 0.7
    print("[PASSED] HybridRetriever test")


def test_context_builder():
    """Test context builder formatting."""
    cb = ContextBuilder()
    sample = {
        "chunks": [{"document": "GraphRAG is trust-aware.", "metadata": {"source_file": "doc1.pdf"}, "hybrid_score": 0.9}],
        "graph_context": {"nodes": [{"id": "GraphRAG", "label": "CONCEPT"}], "edges": []},
        "query_entities": ["GraphRAG"]
    }
    context = cb.build_context(sample)
    assert "RETRIEVED DOCUMENT CONTEXT" in context
    assert "doc1.pdf" in context
    print("[PASSED] ContextBuilder test")


def test_prompt_builder():
    """Test Llama 3 prompt assembly."""
    pb = PromptBuilder()
    prompt = pb.build_prompt("What is GraphRAG?", "Context: GraphRAG is a framework.")
    assert "user_prompt" in prompt
    assert "full_prompt" in prompt
    assert "What is GraphRAG?" in prompt["user_prompt"]
    print("[PASSED] PromptBuilder test")


def test_graphrag_retriever_pipeline():
    """Test master retriever pipeline integration."""
    grr = GraphRAGRetriever()
    pipeline_res = grr.run_retrieval_pipeline("Explain GraphRAG retrieval", top_k=3, alpha=0.6)
    assert pipeline_res["query"] == "Explain GraphRAG retrieval"
    assert "context_string" in pipeline_res
    assert "prompt" in pipeline_res
    print("[PASSED] GraphRAGRetriever Pipeline Integration test")


if __name__ == "__main__":
    print("\nRunning Module 3 Unit & Integration Tests...\n" + "=" * 50)
    test_vector_retriever()
    test_graph_retriever()
    test_hybrid_retriever()
    test_context_builder()
    test_prompt_builder()
    test_graphrag_retriever_pipeline()
    print("=" * 50 + "\nAll Module 3 Tests Passed Successfully!\n")
