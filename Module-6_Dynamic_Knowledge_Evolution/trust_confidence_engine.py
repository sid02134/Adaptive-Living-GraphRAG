"""
Module 6: Dynamic Knowledge Evolution
File: trust_confidence_engine.py
Purpose: Engine 3 - Compute transparent system-level trust & confidence scores.
"""

from typing import Dict, Any, Optional
from pathlib import Path

try:
    from .config import Module6Config
    from .models import KnowledgeClaim, TrustScoreBreakdown
    from .utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from .exceptions import TrustCalculationError
except (ImportError, ValueError):
    from config import Module6Config
    from models import KnowledgeClaim, TrustScoreBreakdown
    from utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from exceptions import TrustCalculationError

# Import Module 4 TrustScore calculator if available for interoperability
try:
    import importlib
    mod_ts = importlib.import_module("Module-4_LLM_Trust_Engine.trust_score")
    TrustScoreCalculator = getattr(mod_ts, "TrustScoreCalculator")
except Exception:
    TrustScoreCalculator = None


class TrustConfidenceEngine:
    """Engine 3: Calculates multi-factor system trust & confidence scores for claims and retrieval context.

    Formulas & Factors:
        1. Source Reliability (S_rel): Rated by domain authority/source type [0.0 - 1.0].
        2. Freshness (S_fresh): Computed via exponential decay exp(-lambda * days_elapsed).
        3. Supporting Evidence (S_evid): Score reflecting length, specificity, and citation backing [0.0 - 1.0].
        4. Graph Agreement (S_agree): Alignment ratio with verified graph entities/triples [0.0 - 1.0].
        5. Retrieval Relevance (S_relv): Semantic/vector search similarity score [0.0 - 1.0].

    Weighted Formula:
        TrustScore = w1*S_rel + w2*S_fresh + w3*S_evid + w4*S_agree + w5*S_relv
    """

    def __init__(self, custom_weights: Optional[Dict[str, float]] = None) -> None:
        """Initialize TrustConfidenceEngine with configurable scoring weights."""
        self.weights = custom_weights or Module6Config.TRUST_WEIGHTS
        self.module4_calculator = TrustScoreCalculator() if TrustScoreCalculator is not None else None
        logger.info(f"TrustConfidenceEngine initialized with weights: {self.weights}")

    def evaluate_claim_trust(
        self,
        claim: KnowledgeClaim,
        graph_agreement_score: float = 0.8,
        retrieval_relevance_score: float = 0.8,
        evidence_score: Optional[float] = None
    ) -> TrustScoreBreakdown:
        """Calculate complete transparent trust breakdown for a given knowledge claim.

        Args:
            claim (KnowledgeClaim): The target claim object.
            graph_agreement_score (float): Score indicating alignment with existing graph (0.0 to 1.0).
            retrieval_relevance_score (float): Score indicating similarity to search query/context (0.0 to 1.0).
            evidence_score (Optional[float]): Optional explicit evidence score.

        Returns:
            TrustScoreBreakdown: Detailed breakdown of inputs, weights, overall score, and interpretation.
        """
        try:
            # 1. Source Reliability (S_rel)
            source_type = str(claim.source_type or "unknown").lower()
            s_rel = Module6Config.SOURCE_RELIABILITY_SCORES.get(
                source_type,
                claim.confidence if claim.confidence is not None else 0.5
            )

            # 2. Freshness (S_fresh)
            days = calculate_days_elapsed(claim.timestamp)
            s_fresh = calculate_exponential_decay(days)

            # 3. Supporting Evidence (S_evid)
            if evidence_score is not None:
                s_evid = max(0.0, min(1.0, float(evidence_score)))
            else:
                chunk_len = len(claim.context_chunk or "")
                s_evid = min(1.0, 0.4 + (chunk_len / 500.0) * 0.6) if chunk_len > 0 else 0.5

            # 4. Graph Agreement (S_agree)
            s_agree = max(0.0, min(1.0, float(graph_agreement_score)))

            # 5. Retrieval Relevance (S_relv)
            s_relv = max(0.0, min(1.0, float(retrieval_relevance_score)))

            # Weighted Combination
            w_rel = self.weights.get("source_reliability", 0.25)
            w_fresh = self.weights.get("freshness", 0.20)
            w_evid = self.weights.get("evidence_support", 0.20)
            w_agree = self.weights.get("graph_agreement", 0.20)
            w_relv = self.weights.get("retrieval_relevance", 0.15)

            overall_score = (
                (w_rel * s_rel) +
                (w_fresh * s_fresh) +
                (w_evid * s_evid) +
                (w_agree * s_agree) +
                (w_relv * s_relv)
            )
            overall_score = max(0.0, min(1.0, float(overall_score)))

            # Generate transparent system-level interpretation
            interpretation = self._format_interpretation(overall_score, s_rel, s_fresh, s_agree)

            breakdown = TrustScoreBreakdown(
                source_reliability=s_rel,
                freshness=s_fresh,
                evidence_support=s_evid,
                graph_agreement=s_agree,
                retrieval_relevance=s_relv,
                overall_trust_score=overall_score,
                interpretation=interpretation
            )

            return breakdown

        except Exception as e:
            logger.error(f"Trust confidence evaluation error: {e}")
            raise TrustCalculationError(f"Failed to calculate trust score: {e}") from e

    def _format_interpretation(
        self,
        overall: float,
        s_rel: float,
        s_fresh: float,
        s_agree: float
    ) -> str:
        """Format human-readable system confidence interpretation."""
        if overall >= 0.85:
            confidence_level = "High System Confidence"
        elif overall >= 0.65:
            confidence_level = "Moderate System Confidence"
        elif overall >= 0.45:
            confidence_level = "Low/Cautious Confidence"
        else:
            confidence_level = "Untrusted / High Uncertainty"

        desc = (
            f"This claim has a score of {overall:.2f} ({confidence_level}). "
            f"Note: This score reflects system-level confidence based on available source reliability ({s_rel:.2f}), "
            f"freshness ({s_fresh:.2f}), and graph agreement ({s_agree:.2f}), not guaranteed real-world truth."
        )
        return desc
