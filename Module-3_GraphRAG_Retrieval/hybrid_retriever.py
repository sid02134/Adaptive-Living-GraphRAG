"""
Module 3: GraphRAG Retrieval
File: hybrid_retriever.py
Purpose: Perform weighted hybrid score fusion combining vector search and graph search.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
try:
    from .config import Module3Config
    from .vector_retriever import VectorRetriever
    from .graph_retriever import GraphRetriever
    from .utils import logger, normalize_scores
except (ImportError, ValueError):
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
    try:
        from utils import logger, normalize_scores
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")
        normalize_scores = getattr(_mod, "normalize_scores")



class HybridRetriever:
    """Combines vector similarity scores and graph relevance scores into a weighted hybrid score.

    Formula:
        S_hybrid = alpha * S_vector + (1 - alpha) * S_graph

    Attributes:
        vector_retriever (VectorRetriever): Vector search retriever.
        graph_retriever (GraphRetriever): Knowledge graph search retriever.
        alpha (float): Weighting coefficient in [0.0, 1.0].
    """

    def __init__(
        self,
        vector_retriever: Optional[VectorRetriever] = None,
        graph_retriever: Optional[GraphRetriever] = None,
        alpha: float = Module3Config.HYBRID_ALPHA
    ) -> None:
        """Initialize HybridRetriever.

        Args:
            vector_retriever (Optional[VectorRetriever]): Vector search instance.
            graph_retriever (Optional[GraphRetriever]): Graph search instance.
            alpha (float): Weight alpha for vector similarity score. Defaults to 0.6.
        """
        self.vector_retriever = vector_retriever or VectorRetriever()
        self.graph_retriever = graph_retriever or GraphRetriever()
        self.alpha = max(0.0, min(1.0, alpha))

    def retrieve(
        self,
        query: str,
        top_k: int = Module3Config.TOP_K,
        alpha: Optional[float] = None
    ) -> Dict[str, Any]:
        """Perform hybrid retrieval combining vector similarity and graph subgraphs.

        Args:
            query (str): User query string.
            top_k (int): Number of top results to return.
            alpha (Optional[float]): Optional runtime override for hybrid alpha weight.

        Returns:
            Dict[str, Any]: Structured hybrid retrieval output containing ranked items and graph subgraphs.
        """
        effective_alpha = self.alpha if alpha is None else max(0.0, min(1.0, alpha))
        logger.info(f"Executing hybrid retrieval for query: '{query}' (top_k={top_k}, alpha={effective_alpha})")

        # 1. Execute Parallel Retrievals
        vector_results = self.vector_retriever.retrieve(query, top_k=top_k * 2)
        graph_results = self.graph_retriever.retrieve(query, top_k=top_k * 2)

        # 2. Combine & Score Chunks
        chunk_map = {}  # chunk_id -> dict item

        for item in vector_results:
            cid = item["id"]
            v_score = float(item.get("similarity_score", 0.5))
            chunk_map[cid] = {
                "id": cid,
                "document": item.get("document", ""),
                "metadata": item.get("metadata", {}),
                "vector_score": v_score,
                "graph_score": 0.0,
                "hybrid_score": 0.0
            }

        graph_chunk_scores = graph_results.get("chunk_scores", {})
        for cid, g_score in graph_chunk_scores.items():
            if cid in chunk_map:
                chunk_map[cid]["graph_score"] = float(g_score)
            else:
                chunk_map[cid] = {
                    "id": cid,
                    "document": f"Graph Context Chunk [{cid}]",
                    "metadata": {"source_file": "graph_knowledge"},
                    "vector_score": 0.0,
                    "graph_score": float(g_score),
                    "hybrid_score": 0.0
                }

        # 3. Calculate Hybrid Score for each chunk
        combined_chunks = list(chunk_map.values())
        for item in combined_chunks:
            v_s = item["vector_score"]
            g_s = item["graph_score"]
            # Hybrid Formula
            h_s = (effective_alpha * v_s) + ((1.0 - effective_alpha) * g_s)
            item["hybrid_score"] = round(float(h_s), 4)

        # 4. Re-rank results by hybrid_score
        combined_chunks.sort(key=lambda x: x["hybrid_score"], reverse=True)
        top_chunks = combined_chunks[:top_k]

        logger.info(f"Hybrid retrieval completed. Selected top {len(top_chunks)} chunk(s).")
        return {
            "query": query,
            "top_k": top_k,
            "alpha": effective_alpha,
            "chunks": top_chunks,
            "graph_context": graph_results.get("subgraph", {"nodes": [], "edges": []}),
            "query_entities": graph_results.get("query_entities", [])
        }


if __name__ == "__main__":
    retriever = HybridRetriever()
    out = retriever.retrieve("Explain how GraphRAG fuses vector search and knowledge graphs.")
    print("Hybrid Retriever Top Items:", len(out["chunks"]))
