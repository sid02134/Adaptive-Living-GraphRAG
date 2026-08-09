"""
Module 4: LLM + Trust Engine
File: source_ranker.py
Purpose: Rank context sources by relevance, provenance, and trust ratings.
"""

from typing import List, Dict, Any
from pathlib import Path
try:
    from utils import trust_logger
except (ImportError, AttributeError):
    import importlib.util
    _ut_path = Path(__file__).resolve().parent / "utils.py"
    _spec = importlib.util.spec_from_file_location("mod4_utils", _ut_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    trust_logger = getattr(_mod, "trust_logger")


class SourceRanker:
    """Ranks context sources and chunks based on semantic similarity and provenance reliability."""

    def rank_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank retrieved chunks by combined trust rank score.

        Args:
            chunks (List[Dict[str, Any]]): List of retrieved chunk dictionaries.

        Returns:
            List[Dict[str, Any]]: Ranked list of source chunks with assigned rank integer.
        """
        if not chunks:
            return []

        ranked_chunks = []
        for c in chunks:
            score = float(c.get("hybrid_score", c.get("vector_score", 0.5)))
            doc_name = c.get("metadata", {}).get("source_file", "unknown_source.pdf")

            # Boost verified file extensions
            provenance_weight = 1.0
            if doc_name.endswith(".pdf"):
                provenance_weight = 1.1

            rank_score = round(score * provenance_weight, 4)
            c_copy = dict(c)
            c_copy["rank_score"] = rank_score
            ranked_chunks.append(c_copy)

        ranked_chunks.sort(key=lambda x: x["rank_score"], reverse=True)
        for rank_idx, item in enumerate(ranked_chunks, start=1):
            item["rank"] = rank_idx

        trust_logger.info(f"Ranked {len(ranked_chunks)} source chunk(s).")
        return ranked_chunks


if __name__ == "__main__":
    sr = SourceRanker()
    out = sr.rank_sources([
        {"id": "c1", "hybrid_score": 0.7, "metadata": {"source_file": "a.pdf"}},
        {"id": "c2", "hybrid_score": 0.9, "metadata": {"source_file": "b.pdf"}}
    ])
    print("Ranked Sources:\n", out)
