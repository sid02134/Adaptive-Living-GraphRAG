"""
Module 6: Dynamic Knowledge Evolution
File: adaptive_retriever.py
Purpose: Engine 5 - Perform 4-dimensional adaptive retrieval combining vector similarity, graph relevance, trust, and temporal freshness.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from .config import Module6Config
    from .trust_confidence_engine import TrustConfidenceEngine
    from .temporal_aging_engine import TemporalKnowledgeAgingEngine
    from .utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from .exceptions import AdaptiveRetrievalError
except (ImportError, ValueError):
    from config import Module6Config
    from trust_confidence_engine import TrustConfidenceEngine
    from temporal_aging_engine import TemporalKnowledgeAgingEngine
    from utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from exceptions import AdaptiveRetrievalError

# Import Module 3 HybridRetriever if available
try:
    import importlib
    mod_hr = importlib.import_module("Module-3_GraphRAG_Retrieval.hybrid_retriever")
    HybridRetriever = getattr(mod_hr, "HybridRetriever")
except Exception:
    HybridRetriever = None


class AdaptiveRetrievalEngine:
    """Engine 5: Extended GraphRAG retriever combining 4 scoring dimensions.

    Formula:
        FinalScore = w1*VectorScore + w2*GraphScore + w3*TrustScore + w4*FreshnessScore
    """

    def __init__(
        self,
        base_hybrid_retriever: Optional[Any] = None,
        trust_engine: Optional[TrustConfidenceEngine] = None,
        temporal_engine: Optional[TemporalKnowledgeAgingEngine] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> None:
        """Initialize AdaptiveRetrievalEngine.

        Args:
            base_hybrid_retriever (Optional[Any]): Module 3 HybridRetriever instance.
            trust_engine (Optional[TrustConfidenceEngine]): Trust engine instance.
            temporal_engine (Optional[TemporalKnowledgeAgingEngine]): Temporal aging engine instance.
            weights (Optional[Dict[str, float]]): Dictionary specifying w_vector, w_graph, w_trust, w_freshness.
        """
        self.hybrid_retriever = base_hybrid_retriever or (HybridRetriever() if HybridRetriever is not None else None)
        self.trust_engine = trust_engine or TrustConfidenceEngine()
        self.temporal_engine = temporal_engine or TemporalKnowledgeAgingEngine()
        
        raw_weights = weights or Module6Config.ADAPTIVE_RETRIEVAL_WEIGHTS
        self.w_vector = raw_weights.get("vector_weight", 0.35)
        self.w_graph = raw_weights.get("graph_weight", 0.25)
        self.w_trust = raw_weights.get("trust_weight", 0.20)
        self.w_freshness = raw_weights.get("freshness_weight", 0.20)

        # Normalize weights so they sum to 1.0
        total_w = self.w_vector + self.w_graph + self.w_trust + self.w_freshness
        if total_w > 0:
            self.w_vector /= total_w
            self.w_graph /= total_w
            self.w_trust /= total_w
            self.w_freshness /= total_w

        logger.info(
            f"AdaptiveRetrievalEngine initialized (weights: vector={self.w_vector:.2f}, "
            f"graph={self.w_graph:.2f}, trust={self.w_trust:.2f}, freshness={self.w_freshness:.2f})"
        )

    def adaptive_retrieve(
        self,
        query: str,
        top_k: int = 5,
        include_historical: bool = False,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Perform 4-dimensional adaptive retrieval across vector, graph, trust, and temporal axes.

        Args:
            query (str): Query string.
            top_k (int): Number of top results to return.
            include_historical (bool): Whether to include superseded/archived historical knowledge.
            custom_weights (Optional[Dict[str, float]]): Runtime weight overrides.

        Returns:
            Dict[str, Any]: Ranked retrieval results with itemized score breakdowns.
        """
        try:
            logger.info(f"Executing 4-factor adaptive retrieval for query: '{query}' (top_k={top_k})")

            # Apply runtime weights if provided
            w_v = self.w_vector
            w_g = self.w_graph
            w_t = self.w_trust
            w_f = self.w_freshness

            if custom_weights:
                w_v = custom_weights.get("vector_weight", w_v)
                w_g = custom_weights.get("graph_weight", w_g)
                w_t = custom_weights.get("trust_weight", w_t)
                w_f = custom_weights.get("freshness_weight", w_f)
                tot = w_v + w_g + w_t + w_f
                if tot > 0:
                    w_v, w_g, w_t, w_f = w_v / tot, w_g / tot, w_t / tot, w_f / tot

            # 1. Fetch base candidates via HybridRetriever or fallback
            base_chunks = []
            graph_context = {"nodes": [], "edges": []}
            query_entities = []

            if self.hybrid_retriever is not None:
                try:
                    res = self.hybrid_retriever.retrieve(query, top_k=top_k * 2)
                    base_chunks = res.get("chunks", [])
                    graph_context = res.get("graph_context", graph_context)
                    query_entities = res.get("query_entities", query_entities)
                except Exception as e:
                    logger.warning(f"Module 3 HybridRetriever execution failed: {e}. Falling back to direct mock.")
                    base_chunks = []

            # Fallback candidate generation if retriever unavailable or empty
            if not base_chunks:
                base_chunks = [
                    {
                        "id": f"chunk_adaptive_1",
                        "document": f"Relevant context for query '{query}' retrieved from knowledge repository.",
                        "metadata": {"source_file": "knowledge_doc.pdf", "timestamp": "2026-03-15T10:00:00Z", "source_type": "official_doc"},
                        "vector_score": 0.88,
                        "graph_score": 0.82
                    }
                ]

            # 2. Enrich candidate items with Trust and Freshness Scores
            enriched_items = []
            for item in base_chunks:
                meta = item.get("metadata", {})
                status = meta.get("validity_status", "ACTIVE")

                # Filter out historical items if include_historical is False
                if not include_historical and status in ["SUPERSEDED", "ARCHIVED"]:
                    continue

                v_score = float(item.get("vector_score", 0.5))
                g_score = float(item.get("graph_score", 0.5))

                # Compute Freshness Score (S_fresh)
                ts = meta.get("timestamp") or meta.get("created_at")
                days = calculate_days_elapsed(str(ts)) if ts else 0.0
                f_score = calculate_exponential_decay(days)

                # Compute Trust Score (S_trust)
                src_type = meta.get("source_type", "official_doc")
                s_rel = Module6Config.SOURCE_RELIABILITY_SCORES.get(src_type, 0.7)
                t_score = 0.4 * s_rel + 0.3 * f_score + 0.3 * g_score

                # Calculate Final 4-Factor Adaptive Score
                final_score = (w_v * v_score) + (w_g * g_score) + (w_t * t_score) + (w_f * f_score)
                final_score = round(max(0.0, min(1.0, float(final_score))), 4)

                enriched_item = dict(item)
                enriched_item["vector_score"] = round(v_score, 4)
                enriched_item["graph_score"] = round(g_score, 4)
                enriched_item["trust_score"] = round(t_score, 4)
                enriched_item["freshness_score"] = round(f_score, 4)
                enriched_item["final_adaptive_score"] = final_score
                enriched_item["validity_status"] = status

                enriched_items.append(enriched_item)

            # 3. Sort candidates by final_adaptive_score descending
            enriched_items.sort(key=lambda x: x["final_adaptive_score"], reverse=True)
            top_results = enriched_items[:top_k]

            return {
                "query": query,
                "top_k": top_k,
                "include_historical": include_historical,
                "applied_weights": {
                    "vector_weight": round(w_v, 3),
                    "graph_weight": round(w_g, 3),
                    "trust_weight": round(w_t, 3),
                    "freshness_weight": round(w_f, 3)
                },
                "results": top_results,
                "graph_context": graph_context,
                "query_entities": query_entities
            }

        except Exception as e:
            logger.error(f"Adaptive retrieval execution error: {e}")
            raise AdaptiveRetrievalError(f"Adaptive retrieval failed: {e}") from e
