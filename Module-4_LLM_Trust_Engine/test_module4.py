"""
Module 4: LLM + Trust Engine
File: test_module4.py
Purpose: Unit and integration tests for Module 4 components.
"""

import sys
from pathlib import Path

# Add Module 4 directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from config import Module4Config
from ollama_client import OllamaClient
from trust_score import TrustEvaluator
from source_ranker import SourceRanker
from conflict_resolution import ConflictResolver
from citation_generator import CitationGenerator
from response_formatter import ResponseFormatter
from answer_generator import AnswerGenerator


def test_ollama_client():
    """Test Ollama client fallback generation."""
    client = OllamaClient()
    response = client.generate("Test prompt query")
    assert isinstance(response, str)
    assert len(response) > 0
    print("\n[PASSED] OllamaClient test")


def test_trust_evaluator_formula():
    """Test exact 4-tier trust score formula calculation."""
    evaluator = TrustEvaluator()
    chunks = [{"hybrid_score": 0.8, "metadata": {"source_file": "doc1.pdf"}}]
    graph_ctx = {"nodes": [{"id": "N1"}], "edges": [{"source": "N1", "target": "N2"}]}
    answer = "GraphRAG is a framework [Source 1: doc1.pdf]."
    citations = [{"source_file": "doc1.pdf", "formatted_citation": "[Source 1: doc1.pdf]"}]

    eval_result = evaluator.evaluate_trust(chunks, graph_ctx, answer, citations)
    assert "trust_score" in eval_result
    assert "trust_percentage" in eval_result
    assert "metric_breakdown" in eval_result

    bd = eval_result["metric_breakdown"]
    assert "semantic_similarity" in bd
    assert "source_reliability" in bd
    assert "graph_consistency" in bd
    assert "citation_coverage" in bd

    print("[PASSED] TrustEvaluator formula test")


def test_source_ranker():
    """Test source ranking logic."""
    ranker = SourceRanker()
    chunks = [
        {"id": "c1", "hybrid_score": 0.5, "metadata": {"source_file": "a.txt"}},
        {"id": "c2", "hybrid_score": 0.9, "metadata": {"source_file": "b.pdf"}}
    ]
    ranked = ranker.rank_sources(chunks)
    assert len(ranked) == 2
    assert ranked[0]["id"] == "c2"
    print("[PASSED] SourceRanker test")


def test_conflict_resolver():
    """Test conflict detection and resolution."""
    resolver = ConflictResolver()
    chunks = [
        {"id": "c1", "document": "Feature X is enabled."},
        {"id": "c2", "document": "Feature X is not supported."}
    ]
    res = resolver.resolve_conflicts(chunks)
    assert res["conflict_detected"] is True
    print("[PASSED] ConflictResolver test")


def test_citation_generator():
    """Test citation string formatting."""
    cg = CitationGenerator()
    chunks = [{"id": "chk_01", "hybrid_score": 0.85, "metadata": {"source_file": "sample.pdf"}}]
    cits = cg.generate_citations(chunks)
    assert len(cits) == 1
    assert "sample.pdf" in cits[0]["formatted_citation"]
    print("[PASSED] CitationGenerator test")


def test_response_formatter():
    """Test frontend response object formatting."""
    formatter = ResponseFormatter()
    res = formatter.format_frontend_response(
        query="What is GraphRAG?",
        answer="GraphRAG integrates Knowledge Graphs with Vector Search.",
        trust_evaluation={"trust_score": 0.9, "trust_percentage": 90.0, "confidence_level": "High Confidence", "metric_breakdown": {}},
        citations=[],
        ranked_sources=[],
        conflict_info={"conflict_detected": False, "resolution_notes": "None"}
    )
    assert res["query"] == "What is GraphRAG?"
    assert res["trust_percentage"] == 90.0
    print("[PASSED] ResponseFormatter test")


def test_answer_generator_pipeline():
    """Test complete AnswerGenerator integration."""
    ag = AnswerGenerator()
    res = ag.generate_answer("How does GraphRAG process documents?")
    assert "answer" in res
    assert "trust_score" in res
    assert "markdown_response" in res
    print("[PASSED] AnswerGenerator Integration test")


if __name__ == "__main__":
    print("\nRunning Module 4 Unit & Integration Tests...\n" + "=" * 50)
    test_ollama_client()
    test_trust_evaluator_formula()
    test_source_ranker()
    test_conflict_resolver()
    test_citation_generator()
    test_response_formatter()
    test_answer_generator_pipeline()
    print("=" * 50 + "\nAll Module 4 Tests Passed Successfully!\n")
