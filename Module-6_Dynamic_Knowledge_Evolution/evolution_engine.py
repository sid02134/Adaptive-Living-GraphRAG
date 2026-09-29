"""
Module 6: Dynamic Knowledge Evolution
File: evolution_engine.py
Purpose: Engine 1 - Main Adaptive Knowledge Evolution Engine orchestrating incoming fact evaluation,
         decision-making (ADD, UPDATE, REPLACE, ARCHIVE, REJECT), conflict resolution, trust evaluation,
         and incremental update triggering.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

try:
    from .config import Module6Config
    from .models import (
        KnowledgeClaim, EvolutionDecisionType, ValidityStatus, EvolutionResult, ConflictRecord
    )
    from .trust_confidence_engine import TrustConfidenceEngine
    from .temporal_aging_engine import TemporalKnowledgeAgingEngine
    from .conflict_engine import ConflictResolutionEngine
    from .incremental_graph_updater import IncrementalGraphUpdater
    from .utils import logger, append_json_log, load_json_log
    from .exceptions import EvolutionEngineError
except (ImportError, ValueError):
    from config import Module6Config
    from models import (
        KnowledgeClaim, EvolutionDecisionType, ValidityStatus, EvolutionResult, ConflictRecord
    )
    from trust_confidence_engine import TrustConfidenceEngine
    from temporal_aging_engine import TemporalKnowledgeAgingEngine
    from conflict_engine import ConflictResolutionEngine
    from incremental_graph_updater import IncrementalGraphUpdater
    from utils import logger, append_json_log, load_json_log
    from exceptions import EvolutionEngineError


class AdaptiveKnowledgeEvolutionEngine:
    """Engine 1: Main orchestrator for dynamic knowledge graph evolution."""

    def __init__(
        self,
        trust_engine: Optional[TrustConfidenceEngine] = None,
        temporal_engine: Optional[TemporalKnowledgeAgingEngine] = None,
        conflict_engine: Optional[ConflictResolutionEngine] = None,
        updater: Optional[IncrementalGraphUpdater] = None
    ) -> None:
        """Initialize AdaptiveKnowledgeEvolutionEngine with component engines."""
        self.trust_engine = trust_engine or TrustConfidenceEngine()
        self.temporal_engine = temporal_engine or TemporalKnowledgeAgingEngine()
        self.conflict_engine = conflict_engine or ConflictResolutionEngine(trust_engine=self.trust_engine)
        self.updater = updater or IncrementalGraphUpdater()
        
        # In-memory store of active claims for fallback execution
        self._knowledge_store: List[KnowledgeClaim] = []
        self._load_persisted_store()
        logger.info("AdaptiveKnowledgeEvolutionEngine initialized.")

    def evaluate_and_evolve(
        self,
        incoming_data: Dict[str, Any],
        conflict_policy_override: Optional[str] = None
    ) -> EvolutionResult:
        """Evaluate an incoming claim/fact and apply the appropriate evolution decision.

        Args:
            incoming_data (Dict[str, Any]): Dictionary describing incoming knowledge.
                Expected fields: subject, predicate, object, source, source_type, timestamp, confidence, context_chunk.
            conflict_policy_override (Optional[str]): Optional policy override for conflict resolution.

        Returns:
            EvolutionResult: Complete result detailing decision (ADD, UPDATE, REPLACE, ARCHIVE, REJECT),
                             trust breakdown, conflict reports, and incremental update status.
        """
        try:
            # 1. Parse and validate incoming claim
            claim = self._parse_claim(incoming_data)

            # Rejection check for invalid/empty inputs
            if not claim.subject or not claim.predicate or not claim.object:
                reason = "Rejected due to missing required triple fields (subject, predicate, object)."
                logger.warning(f"Claim REJECTED: {reason}")
                return EvolutionResult(
                    claim_id=claim.id,
                    decision=EvolutionDecisionType.REJECT,
                    reasoning=reason,
                    trust_breakdown={"overall_trust_score": 0.0, "interpretation": "Rejected due to missing fields"}
                )

            # 2. Evaluate Trust & Confidence Score
            trust_breakdown = self.trust_engine.evaluate_claim_trust(claim)
            if trust_breakdown.overall_trust_score < 0.25:
                reason = f"Rejected due to extremely low trust score ({trust_breakdown.overall_trust_score:.2f} < 0.25)."
                logger.warning(f"Claim {claim.id} REJECTED: {reason}")
                return EvolutionResult(
                    claim_id=claim.id,
                    decision=EvolutionDecisionType.REJECT,
                    reasoning=reason,
                    trust_breakdown=trust_breakdown.to_dict()
                )

            # 3. Check for exact duplicate or update to existing facts
            existing_match, is_exact = self._find_matching_fact(claim)

            # 4. Check for Contradictions / Conflicts
            conflict = self.conflict_engine.detect_conflict(claim, self._knowledge_store)
            conflict_record_dict = None
            losing_claim_id = None

            decision = EvolutionDecisionType.ADD
            reasoning = "New knowledge fact detected. Added to graph and vector store."

            if conflict:
                resolved_conflict, directives = self.conflict_engine.resolve_conflict(
                    conflict, policy=conflict_policy_override
                )
                conflict_record_dict = resolved_conflict.to_dict()
                winning_id = directives.get("winning_claim_id")

                if winning_id == claim.id:
                    decision = EvolutionDecisionType.REPLACE
                    losing_claim_id = directives.get("losing_claim_id")
                    reasoning = (
                        f"Conflict detected with existing claim. Incoming claim '{claim.id}' won resolution "
                        f"via {directives.get('policy_applied')} policy. Replaced previous claim '{losing_claim_id}'."
                    )
                    self._mark_claim_superseded(losing_claim_id)
                elif winning_id == "NONE":
                    decision = EvolutionDecisionType.ADD
                    reasoning = "Conflict detected. Both claims preserved with CONFLICTING status."
                    claim.validity_status = ValidityStatus.CONFLICTING
                else:
                    decision = EvolutionDecisionType.REJECT
                    reasoning = (
                        f"Conflict detected with existing claim. Existing claim '{winning_id}' won resolution. "
                        f"Incoming claim '{claim.id}' rejected."
                    )
                    return EvolutionResult(
                        claim_id=claim.id,
                        decision=EvolutionDecisionType.REJECT,
                        reasoning=reasoning,
                        trust_breakdown=trust_breakdown.to_dict(),
                        conflict_detected=True,
                        conflict_record=conflict_record_dict
                    )

            elif existing_match:
                if is_exact:
                    decision = EvolutionDecisionType.UPDATE
                    reasoning = f"Fact already exists. Updated metadata and verified claim '{existing_match.id}'."
                    claim.id = existing_match.id
                else:
                    decision = EvolutionDecisionType.UPDATE
                    reasoning = f"Updated existing fact '{existing_match.id}' with fresh evidence/attributes."

            # 5. Check Temporal Aging for Outdated status
            temporal_eval = self.temporal_engine.evaluate_temporal_status(claim)
            if temporal_eval.get("action_recommended") == "ARCHIVE":
                decision = EvolutionDecisionType.ARCHIVE
                claim.validity_status = ValidityStatus.ARCHIVED
                reasoning = "Information is historically outdated and marked for archiving."

            # 6. Apply Incremental Mutation to Graph & Vector DBs
            update_summary = self.updater.apply_claim_update(
                claim=claim,
                decision=decision,
                losing_claim_id=losing_claim_id
            )

            # 7. Store claim in internal knowledge log
            if decision in [EvolutionDecisionType.ADD, EvolutionDecisionType.UPDATE, EvolutionDecisionType.REPLACE]:
                self._upsert_knowledge_store(claim)

            # Construct result
            result = EvolutionResult(
                claim_id=claim.id,
                decision=decision,
                reasoning=reasoning,
                trust_breakdown=trust_breakdown.to_dict(),
                conflict_detected=conflict is not None,
                conflict_record=conflict_record_dict,
                graph_updates=update_summary
            )

            # Persist audit record
            append_json_log(Module6Config.AUDIT_FILE, result.to_dict())

            return result

        except Exception as e:
            logger.error(f"Error executing evaluate_and_evolve: {e}")
            raise EvolutionEngineError(f"Knowledge evolution evaluation failed: {e}") from e

    def get_evolution_history(self) -> List[Dict[str, Any]]:
        """Retrieve historical log of evolution decisions.

        Returns:
            List[Dict[str, Any]]: Audit history records.
        """
        return load_json_log(Module6Config.AUDIT_FILE)

    def _parse_claim(self, data: Dict[str, Any]) -> KnowledgeClaim:
        """Parse dictionary data into a KnowledgeClaim instance."""
        cid = str(data.get("id") or f"claim_{uuid.uuid4().hex[:8]}")
        return KnowledgeClaim(
            id=cid,
            subject=str(data.get("subject", "")).strip(),
            predicate=str(data.get("predicate", "")).strip(),
            object=str(data.get("object", "")).strip(),
            source=str(data.get("source", "user_input")),
            source_type=str(data.get("source_type", "general")),
            timestamp=str(data.get("timestamp") or data.get("created_at") or ""),
            confidence=float(data.get("confidence", 0.8)),
            context_chunk=str(data.get("context_chunk", "")),
            validity_status=ValidityStatus.ACTIVE,
            metadata=data.get("metadata", {})
        )

    def _find_matching_fact(self, claim: KnowledgeClaim) -> Tuple[Optional[KnowledgeClaim], bool]:
        """Find matching existing claim and check if exact match or update."""
        sub = claim.subject.lower()
        pred = claim.predicate.lower()
        obj = claim.object.lower()

        for ext in self._knowledge_store:
            if ext.validity_status in [ValidityStatus.ARCHIVED, ValidityStatus.SUPERSEDED]:
                continue
            if ext.subject.lower() == sub and ext.predicate.lower() == pred:
                if ext.object.lower() == obj:
                    return ext, True  # Exact match
                return ext, False # Matching subject/predicate, minor difference
        return None, False

    def _upsert_knowledge_store(self, claim: KnowledgeClaim) -> None:
        """Update or insert claim in in-memory store."""
        for i, existing in enumerate(self._knowledge_store):
            if existing.id == claim.id:
                self._knowledge_store[i] = claim
                return
        self._knowledge_store.append(claim)

    def _mark_claim_superseded(self, losing_id: Optional[str]) -> None:
        """Mark a losing claim as SUPERSEDED."""
        if not losing_id:
            return
        for c in self._knowledge_store:
            if c.id == losing_id:
                c.validity_status = ValidityStatus.SUPERSEDED
                break

    def _load_persisted_store(self) -> None:
        """Load persistent history into in-memory store on startup."""
        records = load_json_log(Module6Config.AUDIT_FILE)
        for r in records:
            if r.get("decision") in ["ADD", "UPDATE", "REPLACE"]:
                cid = r.get("claim_id")
                # Create stub KnowledgeClaim
                c = KnowledgeClaim(
                    id=cid,
                    subject=r.get("subject", "Fact"),
                    predicate=r.get("predicate", "relates_to"),
                    object=r.get("object", "Entity"),
                    timestamp=r.get("timestamp", "")
                )
                self._knowledge_store.append(c)
