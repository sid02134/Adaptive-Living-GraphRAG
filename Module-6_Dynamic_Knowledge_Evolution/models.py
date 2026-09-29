"""
Module 6: Dynamic Knowledge Evolution
File: models.py
Purpose: Structured data models for Knowledge Evolution, Conflicts, Trust Scores, and Retrieval.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class EvolutionDecisionType(str, Enum):
    """Supported decision outcomes for knowledge evolution."""
    ADD = "ADD"
    UPDATE = "UPDATE"
    REPLACE = "REPLACE"
    ARCHIVE = "ARCHIVE"
    REJECT = "REJECT"


class ValidityStatus(str, Enum):
    """Validity statuses for nodes, relationships, and claims."""
    ACTIVE = "ACTIVE"
    OUTDATED = "OUTDATED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    CONFLICTING = "CONFLICTING"


class ConflictPolicy(str, Enum):
    """Conflict resolution policy modes."""
    WEIGHTED_HYBRID = "WEIGHTED_HYBRID"
    LATEST_WINS = "LATEST_WINS"
    HIGHEST_TRUST_WINS = "HIGHEST_TRUST_WINS"
    PRESERVE_BOTH = "PRESERVE_BOTH"


@dataclass
class KnowledgeClaim:
    """Represents an incoming or existing knowledge claim/fact."""
    id: str
    subject: str
    predicate: str
    object: str
    source: str = "unknown"
    source_type: str = "general"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: float = 0.8
    context_chunk: str = ""
    validity_status: ValidityStatus = ValidityStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert claim object to dictionary."""
        return {
            "id": self.id,
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "source": self.source,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "confidence": float(self.confidence),
            "context_chunk": self.context_chunk,
            "validity_status": self.validity_status.value if isinstance(self.validity_status, ValidityStatus) else str(self.validity_status),
            "metadata": self.metadata
        }


@dataclass
class TrustScoreBreakdown:
    """Detailed transparent metrics breakdown for trust scoring."""
    source_reliability: float
    freshness: float
    evidence_support: float
    graph_agreement: float
    retrieval_relevance: float
    overall_trust_score: float
    interpretation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_reliability": round(self.source_reliability, 4),
            "freshness": round(self.freshness, 4),
            "evidence_support": round(self.evidence_support, 4),
            "graph_agreement": round(self.graph_agreement, 4),
            "retrieval_relevance": round(self.retrieval_relevance, 4),
            "overall_trust_score": round(self.overall_trust_score, 4),
            "score_percentage": f"{round(self.overall_trust_score * 100, 1)}%",
            "interpretation": self.interpretation
        }


@dataclass
class ConflictRecord:
    """Record representing a detected conflict between competing claims."""
    conflict_id: str
    entity_subject: str
    predicate: str
    claim_a: Dict[str, Any]
    claim_b: Dict[str, Any]
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolution_status: str = "UNRESOLVED"  # UNRESOLVED, RESOLVED_CLAIM_A, RESOLVED_CLAIM_B, RESOLVED_BOTH
    winning_claim_id: Optional[str] = None
    applied_policy: Optional[str] = None
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "entity_subject": self.entity_subject,
            "predicate": self.predicate,
            "claim_a": self.claim_a,
            "claim_b": self.claim_b,
            "detected_at": self.detected_at,
            "resolution_status": self.resolution_status,
            "winning_claim_id": self.winning_claim_id,
            "applied_policy": self.applied_policy,
            "rationale": self.rationale
        }


@dataclass
class EvolutionResult:
    """Result summary of evaluating an incoming knowledge item."""
    claim_id: str
    decision: EvolutionDecisionType
    reasoning: str
    trust_breakdown: Dict[str, Any]
    conflict_detected: bool = False
    conflict_record: Optional[Dict[str, Any]] = None
    graph_updates: Dict[str, Any] = field(default_factory=dict)
    vector_updates: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "decision": self.decision.value if isinstance(self.decision, EvolutionDecisionType) else str(self.decision),
            "reasoning": self.reasoning,
            "trust_breakdown": self.trust_breakdown,
            "conflict_detected": self.conflict_detected,
            "conflict_record": self.conflict_record,
            "graph_updates": self.graph_updates,
            "vector_updates": self.vector_updates,
            "timestamp": self.timestamp
        }
