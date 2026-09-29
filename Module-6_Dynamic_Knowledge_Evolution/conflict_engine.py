"""
Module 6: Dynamic Knowledge Evolution
File: conflict_engine.py
Purpose: Engine 2 - Detect contradictory claims, compare evidence/freshness, and apply resolution policies.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

try:
    from .config import Module6Config
    from .models import KnowledgeClaim, ConflictRecord, ConflictPolicy, ValidityStatus
    from .trust_confidence_engine import TrustConfidenceEngine
    from .utils import logger, append_json_log, load_json_log, calculate_days_elapsed
    from .exceptions import ConflictResolutionError
except (ImportError, ValueError):
    from config import Module6Config
    from models import KnowledgeClaim, ConflictRecord, ConflictPolicy, ValidityStatus
    from trust_confidence_engine import TrustConfidenceEngine
    from utils import logger, append_json_log, load_json_log, calculate_days_elapsed
    from exceptions import ConflictResolutionError


class ConflictResolutionEngine:
    """Engine 2: Contradiction detection and policy-based conflict resolution."""

    def __init__(
        self,
        default_policy: str = Module6Config.DEFAULT_CONFLICT_POLICY,
        trust_engine: Optional[TrustConfidenceEngine] = None
    ) -> None:
        """Initialize ConflictResolutionEngine.

        Args:
            default_policy (str): Policy name ("WEIGHTED_HYBRID", "LATEST_WINS", "HIGHEST_TRUST_WINS", "PRESERVE_BOTH").
            trust_engine (Optional[TrustConfidenceEngine]): Trust engine instance.
        """
        self.default_policy = default_policy
        self.trust_engine = trust_engine or TrustConfidenceEngine()
        logger.info(f"ConflictResolutionEngine initialized with policy '{self.default_policy}'")

    def detect_conflict(
        self,
        incoming_claim: KnowledgeClaim,
        existing_claims: List[KnowledgeClaim]
    ) -> Optional[ConflictRecord]:
        """Detect if an incoming claim contradicts any existing active claim.

        A contradiction occurs when:
            - Both claims share the same Subject (e.g. "Person A" or "Company X")
            - Both claims share the same Predicate (e.g. "is_CEO_of" or "located_in")
            - The Objects/Values differ (e.g. "Company X" vs "Company Y")

        Args:
            incoming_claim (KnowledgeClaim): Incoming claim object.
            existing_claims (List[KnowledgeClaim]): List of existing claims in the system.

        Returns:
            Optional[ConflictRecord]: Conflict record if contradiction detected, else None.
        """
        sub_inc = incoming_claim.subject.strip().lower()
        pred_inc = incoming_claim.predicate.strip().lower()
        obj_inc = incoming_claim.object.strip().lower()

        for existing in existing_claims:
            if existing.validity_status in [ValidityStatus.ARCHIVED, ValidityStatus.SUPERSEDED]:
                continue

            sub_ext = existing.subject.strip().lower()
            pred_ext = existing.predicate.strip().lower()
            obj_ext = existing.object.strip().lower()

            # Check matching subject and predicate with conflicting object
            if sub_inc == sub_ext and pred_inc == pred_ext and obj_inc != obj_ext:
                conflict_id = f"conflict_{uuid.uuid4().hex[:8]}"
                logger.warning(
                    f"Contradiction detected! Subject: '{incoming_claim.subject}', Predicate: '{incoming_claim.predicate}'. "
                    f"Claim A ({existing.id}): '{existing.object}', Claim B ({incoming_claim.id}): '{incoming_claim.object}'"
                )
                
                conflict = ConflictRecord(
                    conflict_id=conflict_id,
                    entity_subject=incoming_claim.subject,
                    predicate=incoming_claim.predicate,
                    claim_a=existing.to_dict(),
                    claim_b=incoming_claim.to_dict(),
                    resolution_status="UNRESOLVED"
                )
                return conflict

        return None

    def resolve_conflict(
        self,
        conflict: ConflictRecord,
        policy: Optional[str] = None
    ) -> Tuple[ConflictRecord, Dict[str, Any]]:
        """Apply configured resolution policy to decide winning claim and update historical statuses.

        Args:
            conflict (ConflictRecord): The detected conflict record.
            policy (Optional[str]): Optional policy override.

        Returns:
            Tuple[ConflictRecord, Dict[str, Any]]: Resolved conflict record and update directive dictionary.
        """
        active_policy = policy or self.default_policy
        claim_a_dict = conflict.claim_a
        claim_b_dict = conflict.claim_b

        claim_a = self._dict_to_claim(claim_a_dict)
        claim_b = self._dict_to_claim(claim_b_dict)

        trust_a_bd = self.trust_engine.evaluate_claim_trust(claim_a)
        trust_b_bd = self.trust_engine.evaluate_claim_trust(claim_b)

        winner = None
        rationale = ""

        if active_policy == ConflictPolicy.LATEST_WINS.value:
            days_a = calculate_days_elapsed(claim_a.timestamp)
            days_b = calculate_days_elapsed(claim_b.timestamp)
            if days_b <= days_a:
                winner = claim_b
                rationale = f"Claim B is newer (timestamp: {claim_b.timestamp}) than Claim A ({claim_a.timestamp})."
            else:
                winner = claim_a
                rationale = f"Claim A is newer (timestamp: {claim_a.timestamp}) than Claim B ({claim_b.timestamp})."

        elif active_policy == ConflictPolicy.HIGHEST_TRUST_WINS.value:
            if trust_b_bd.overall_trust_score >= trust_a_bd.overall_trust_score:
                winner = claim_b
                rationale = f"Claim B has higher/equal trust score ({trust_b_bd.overall_trust_score:.2f}) than Claim A ({trust_a_bd.overall_trust_score:.2f})."
            else:
                winner = claim_a
                rationale = f"Claim A has higher trust score ({trust_a_bd.overall_trust_score:.2f}) than Claim B ({trust_b_bd.overall_trust_score:.2f})."

        elif active_policy == ConflictPolicy.PRESERVE_BOTH.value:
            winner = None
            rationale = "Policy PRESERVE_BOTH specified. Both claims retained with CONFLICTING status for human review."

        else:
            # DEFAULT: WEIGHTED_HYBRID (Combines Trust Score and Recency)
            days_a = calculate_days_elapsed(claim_a.timestamp)
            days_b = calculate_days_elapsed(claim_b.timestamp)
            recency_a = calculate_exponential_decay(days_a)
            recency_b = calculate_exponential_decay(days_b)

            final_a = 0.7 * trust_a_bd.overall_trust_score + 0.3 * recency_a
            final_b = 0.7 * trust_b_bd.overall_trust_score + 0.3 * recency_b

            if final_b >= final_a:
                winner = claim_b
                rationale = f"Claim B won weighted hybrid scoring (score: {final_b:.2f} vs {final_a:.2f})."
            else:
                winner = claim_a
                rationale = f"Claim A won weighted hybrid scoring (score: {final_a:.2f} vs {final_b:.2f})."

        # Construct resolution output
        directives = {
            "policy_applied": active_policy,
            "rationale": rationale,
            "claim_a_trust": trust_a_bd.to_dict(),
            "claim_b_trust": trust_b_bd.to_dict()
        }

        if winner:
            winning_id = winner.id
            losing_id = claim_b.id if winning_id == claim_a.id else claim_a.id

            conflict.resolution_status = f"RESOLVED_{winning_id}"
            conflict.winning_claim_id = winning_id
            conflict.applied_policy = active_policy
            conflict.rationale = rationale

            directives["winning_claim_id"] = winning_id
            directives["losing_claim_id"] = losing_id
            directives["losing_action"] = "MARK_SUPERSEDED"  # Never delete, mark superseded
        else:
            conflict.resolution_status = "PRESERVED_BOTH"
            conflict.winning_claim_id = "NONE"
            conflict.applied_policy = active_policy
            conflict.rationale = rationale
            directives["winning_claim_id"] = "NONE"
            directives["action"] = "MARK_BOTH_CONFLICTING"

        # Log conflict record
        append_json_log(Module6Config.CONFLICT_LOG_FILE, conflict.to_dict())

        return conflict, directives

    def get_all_conflicts() -> List[Dict[str, Any]]:
        """Retrieve stored conflict records from audit log file.

        Returns:
            List[Dict[str, Any]]: List of recorded conflicts.
        """
        return load_json_log(Module6Config.CONFLICT_LOG_FILE)

    def _dict_to_claim(self, data: Dict[str, Any]) -> KnowledgeClaim:
        """Convert a claim dictionary to KnowledgeClaim instance."""
        return KnowledgeClaim(
            id=data.get("id", str(uuid.uuid4())),
            subject=data.get("subject", ""),
            predicate=data.get("predicate", ""),
            object=data.get("object", ""),
            source=data.get("source", "unknown"),
            source_type=data.get("source_type", "general"),
            timestamp=data.get("timestamp", ""),
            confidence=float(data.get("confidence", 0.8)),
            context_chunk=data.get("context_chunk", ""),
            validity_status=data.get("validity_status", ValidityStatus.ACTIVE),
            metadata=data.get("metadata", {})
        )
