"""
Module 4: LLM + Trust Engine
File: trust_score.py
Purpose: Implement 4-tier Trust Score evaluation formula and metric breakdowns.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
try:
    from config import Module4Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module4_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module4Config = _mod.Module4Config
try:
    from exceptions import TrustScoreError
except (ImportError, AttributeError):
    import importlib.util
    _ex_path = Path(__file__).resolve().parent / "exceptions.py"
    _spec = importlib.util.spec_from_file_location("mod4_exceptions", _ex_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    TrustScoreError = getattr(_mod, "TrustScoreError")
try:
    from utils import trust_logger, clamp
except (ImportError, AttributeError):
    import importlib.util
    _ut_path = Path(__file__).resolve().parent / "utils.py"
    _spec = importlib.util.spec_from_file_location("mod4_utils", _ut_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    trust_logger = getattr(_mod, "trust_logger")
    clamp = getattr(_mod, "clamp")


class TrustEvaluator:
    """Evaluates trust metrics according to the exact 4-tier weighted formula:

    Trust = 40% Semantic Similarity + 30% Source Reliability + 20% Graph Consistency + 10% Citation Coverage
    """

    def __init__(self) -> None:
        """Initialize TrustEvaluator with configured formula weights."""
        self.w_sem = Module4Config.WEIGHT_SEMANTIC_SIMILARITY
        self.w_src = Module4Config.WEIGHT_SOURCE_RELIABILITY
        self.w_graph = Module4Config.WEIGHT_GRAPH_CONSISTENCY
        self.w_cit = Module4Config.WEIGHT_CITATION_COVERAGE

    def evaluate_trust(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        graph_context: Dict[str, Any],
        generated_answer: str,
        citations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compute 4-tier Trust Score and metric breakdown.

        Args:
            retrieved_chunks (List[Dict[str, Any]]): Retrieved text chunks with hybrid scores.
            graph_context (Dict[str, Any]): Graph subgraphs and triplets.
            generated_answer (str): Text answer output from LLM.
            citations (List[Dict[str, Any]]): Formatted source citations.

        Returns:
            Dict[str, Any]: Dict containing overall 'trust_score', 'confidence_level', and 'metric_breakdown'.

        Raises:
            TrustScoreError: If evaluation fails.
        """
        try:
            # 1. Semantic Similarity Score (40%)
            if retrieved_chunks:
                sem_scores = [float(c.get("hybrid_score", c.get("vector_score", 0.5))) for c in retrieved_chunks]
                s_semantic = sum(sem_scores) / len(sem_scores)
            else:
                s_semantic = 0.0
            s_semantic = clamp(s_semantic)

            # 2. Source Reliability Score (30%)
            if retrieved_chunks:
                # Reliability based on presence of verified document sources
                reliable_sources = sum(1 for c in retrieved_chunks if c.get("metadata", {}).get("source_file"))
                s_reliability = reliable_sources / len(retrieved_chunks)
            else:
                s_reliability = 0.5
            s_reliability = clamp(s_reliability)

            # 3. Graph Consistency Score (20%)
            nodes = graph_context.get("nodes", [])
            edges = graph_context.get("edges", [])
            if nodes or edges:
                s_graph = min(1.0, 0.4 + (0.1 * len(nodes)) + (0.05 * len(edges)))
            else:
                s_graph = 0.5
            s_graph = clamp(s_graph)

            # 4. Citation Coverage Score (10%)
            if citations and generated_answer:
                cit_count = len(citations)
                s_citation = min(1.0, 0.3 + (0.25 * cit_count))
            else:
                s_citation = 0.0
            s_citation = clamp(s_citation)

            # Compute Weighted Final Trust Score
            total_trust = (
                (self.w_sem * s_semantic) +
                (self.w_src * s_reliability) +
                (self.w_graph * s_graph) +
                (self.w_cit * s_citation)
            )
            total_trust = round(clamp(total_trust), 4)

            # Determine Confidence Level Text
            if total_trust >= 0.85:
                confidence = "High Confidence"
            elif total_trust >= 0.65:
                confidence = "Medium Confidence"
            else:
                confidence = "Low Confidence / Needs Verification"

            breakdown = {
                "semantic_similarity": round(s_semantic * 100, 2),
                "source_reliability": round(s_reliability * 100, 2),
                "graph_consistency": round(s_graph * 100, 2),
                "citation_coverage": round(s_citation * 100, 2)
            }

            trust_logger.info(f"Evaluated Trust Score: {total_trust} ({confidence}) Breakdown: {breakdown}")
            return {
                "trust_score": total_trust,
                "trust_percentage": round(total_trust * 100, 2),
                "confidence_level": confidence,
                "metric_breakdown": breakdown
            }
        except Exception as e:
            trust_logger.error(f"Trust evaluation error: {e}")
            raise TrustScoreError(f"Failed to evaluate trust score: {e}") from e


if __name__ == "__main__":
    evaluator = TrustEvaluator()
    res = evaluator.evaluate_trust(
        retrieved_chunks=[{"hybrid_score": 0.85, "metadata": {"source_file": "doc1.pdf"}}],
        graph_context={"nodes": [{"id": "A"}], "edges": [{"source": "A", "target": "B"}]},
        generated_answer="Sample answer with citation [Source: doc1.pdf]",
        citations=[{"source": "doc1.pdf"}]
    )
    print("Trust Evaluator Result:\n", res)
