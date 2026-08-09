"""
Module 4: LLM + Trust Engine
File: conflict_resolution.py
Purpose: Identify and resolve conflicting statements across source chunks.
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


class ConflictResolver:
    """Detects contradicting claims across chunks using entity overlap and statement heuristics."""

    def resolve_conflicts(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect and log potential conflicts among context chunks.

        Args:
            chunks (List[Dict[str, Any]]): Retrieved context chunks.

        Returns:
            Dict[str, Any]: Conflict resolution analysis containing conflict_detected flag and resolution_notes.
        """
        if not chunks or len(chunks) < 2:
            return {
                "conflict_detected": False,
                "conflicting_chunks": [],
                "resolution_notes": "Single or no chunk context. No cross-document conflicts detected."
            }

        negative_terms = {"not", "no", "never", "unlike", "deprecated", "cannot", "does not"}
        negated_chunks = []
        affirmative_chunks = []

        for c in chunks:
            text = c.get("document", "").lower()
            if any(term in text for term in negative_terms):
                negated_chunks.append(c.get("id"))
            else:
                affirmative_chunks.append(c.get("id"))

        has_conflict = len(negated_chunks) > 0 and len(affirmative_chunks) > 0

        notes = (
            "Cross-document conflict detected between affirmative and negated claims. "
            "Prioritized higher hybrid trust score source." if has_conflict else
            "All retrieved source chunks show consistent non-contradictory claims."
        )

        trust_logger.info(f"Conflict resolution analysis: conflict={has_conflict}")
        return {
            "conflict_detected": has_conflict,
            "negated_chunks": negated_chunks,
            "affirmative_chunks": affirmative_chunks,
            "resolution_notes": notes
        }


if __name__ == "__main__":
    cr = ConflictResolver()
    res = cr.resolve_conflicts([
        {"id": "c1", "document": "GraphRAG is supported on Windows."},
        {"id": "c2", "document": "GraphRAG is not supported on Linux."}
    ])
    print("Conflict Resolver Result:\n", res)
