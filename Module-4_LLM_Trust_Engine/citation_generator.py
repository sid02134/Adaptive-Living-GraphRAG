"""
Module 4: LLM + Trust Engine
File: citation_generator.py
Purpose: Generate verifiable source citations and reference lists for LLM responses.
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


class CitationGenerator:
    """Generates structured inline citations and source references."""

    def generate_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate structured citation records for retrieved chunks.

        Args:
            chunks (List[Dict[str, Any]]): Retrieved context chunks.

        Returns:
            List[Dict[str, Any]]: List of citation dicts containing citation_id, source_file, chunk_id, score, formatted_citation.
        """
        if not chunks:
            return []

        citations = []
        seen_sources = set()

        for idx, chunk in enumerate(chunks, start=1):
            doc_name = chunk.get("metadata", {}).get("source_file", "unknown_document.pdf")
            cid = chunk.get("id", f"chunk_{idx}")
            score = chunk.get("hybrid_score", chunk.get("vector_score", 0.5))

            cit_key = (doc_name, cid)
            if cit_key not in seen_sources:
                seen_sources.add(cit_key)
                citations.append({
                    "citation_id": f"[{idx}]",
                    "source_file": doc_name,
                    "chunk_id": cid,
                    "relevance_score": round(float(score), 4),
                    "formatted_citation": f"[Source {idx}: {doc_name} (Chunk: {cid}, Trust Score: {score:.2f})]"
                })

        trust_logger.info(f"Generated {len(citations)} citation record(s).")
        return citations


if __name__ == "__main__":
    cg = CitationGenerator()
    cits = cg.generate_citations([
        {"id": "chk_01", "hybrid_score": 0.88, "metadata": {"source_file": "GraphRAG_Paper.pdf"}}
    ])
    print("Citations:\n", cits)
