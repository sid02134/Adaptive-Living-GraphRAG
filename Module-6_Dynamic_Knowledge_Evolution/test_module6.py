"""
Module 6: Dynamic Knowledge Evolution
File: test_module6.py
Purpose: Complete test suite verifying all 11 Module 6 requirements and failure modes.
"""

import unittest
from datetime import datetime, timezone, timedelta
import sys
from pathlib import Path

# Ensure root workspace directory is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import importlib
mod_cfg = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.config")
Module6Config = getattr(mod_cfg, "Module6Config")

mod_md = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.models")
KnowledgeClaim = getattr(mod_md, "KnowledgeClaim")
EvolutionDecisionType = getattr(mod_md, "EvolutionDecisionType")
ValidityStatus = getattr(mod_md, "ValidityStatus")
ConflictRecord = getattr(mod_md, "ConflictRecord")

mod_ee = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.evolution_engine")
AdaptiveKnowledgeEvolutionEngine = getattr(mod_ee, "AdaptiveKnowledgeEvolutionEngine")

mod_cr = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.conflict_engine")
ConflictResolutionEngine = getattr(mod_cr, "ConflictResolutionEngine")

mod_tc = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.trust_confidence_engine")
TrustConfidenceEngine = getattr(mod_tc, "TrustConfidenceEngine")

mod_ta = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.temporal_aging_engine")
TemporalKnowledgeAgingEngine = getattr(mod_ta, "TemporalKnowledgeAgingEngine")

mod_ar = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.adaptive_retriever")
AdaptiveRetrievalEngine = getattr(mod_ar, "AdaptiveRetrievalEngine")

mod_iu = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.incremental_graph_updater")
IncrementalGraphUpdater = getattr(mod_iu, "IncrementalGraphUpdater")


class TestModule6DynamicKnowledgeEvolution(unittest.TestCase):
    """Unit and Integration Test Suite for Module 6 engines."""

    def setUp(self):
        """Set up fresh engine instances before each test."""
        self.trust_engine = TrustConfidenceEngine()
        self.temporal_engine = TemporalKnowledgeAgingEngine()
        self.conflict_engine = ConflictResolutionEngine(trust_engine=self.trust_engine)
        self.updater = IncrementalGraphUpdater()
        self.evolution_engine = AdaptiveKnowledgeEvolutionEngine(
            trust_engine=self.trust_engine,
            temporal_engine=self.temporal_engine,
            conflict_engine=self.conflict_engine,
            updater=self.updater
        )
        self.adaptive_retriever = AdaptiveRetrievalEngine(
            trust_engine=self.trust_engine,
            temporal_engine=self.temporal_engine
        )

    # ----------------------------------------------------
    # Test Scenario 1: New Information -> ADD
    # ----------------------------------------------------
    def test_1_new_information_add(self):
        incoming = {
            "subject": "DeepMind",
            "predicate": "developed",
            "object": "AlphaFold 3",
            "source": "nature_journal.pdf",
            "source_type": "peer_reviewed_journal",
            "confidence": 0.95,
            "context_chunk": "DeepMind developed AlphaFold 3 to predict biomolecular structures."
        }
        res = self.evolution_engine.evaluate_and_evolve(incoming)
        self.assertEqual(res.decision, EvolutionDecisionType.ADD)
        self.assertIn("New knowledge fact detected", res.reasoning)
        self.assertGreaterEqual(res.trust_breakdown["overall_trust_score"], 0.7)

    # ----------------------------------------------------
    # Test Scenario 2: Existing Information -> UPDATE
    # ----------------------------------------------------
    def test_2_existing_information_update(self):
        fact = {
            "subject": "Neo4j",
            "predicate": "is_a",
            "object": "Graph Database",
            "source": "official_doc.pdf",
            "source_type": "official_doc"
        }
        # First call adds the fact
        res1 = self.evolution_engine.evaluate_and_evolve(fact)
        self.assertEqual(res1.decision, EvolutionDecisionType.ADD)

        # Second call with exact same fact triggers UPDATE
        res2 = self.evolution_engine.evaluate_and_evolve(fact)
        self.assertEqual(res2.decision, EvolutionDecisionType.UPDATE)
        self.assertIn("Fact already exists", res2.reasoning)

    # ----------------------------------------------------
    # Test Scenario 3: Changed Information -> REPLACE
    # ----------------------------------------------------
    def test_3_changed_information_replace(self):
        old_fact = {
            "id": "claim_ceo_001",
            "subject": "Acme Corp",
            "predicate": "has_CEO",
            "object": "John Doe",
            "source": "annual_report_recent.pdf",
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
        }
        self.evolution_engine.evaluate_and_evolve(old_fact)

        new_fact = {
            "id": "claim_ceo_002",
            "subject": "Acme Corp",
            "predicate": "has_CEO",
            "object": "Jane Smith",
            "source": "press_release_2026.pdf",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        res = self.evolution_engine.evaluate_and_evolve(new_fact, conflict_policy_override="LATEST_WINS")
        self.assertTrue(res.conflict_detected)
        self.assertEqual(res.decision, EvolutionDecisionType.REPLACE)
        self.assertIn("Replaced previous claim", res.reasoning)

    # ----------------------------------------------------
    # Test Scenario 4: Outdated Information -> ARCHIVE
    # ----------------------------------------------------
    def test_4_outdated_information_archive(self):
        very_old_ts = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
        ancient_fact = {
            "subject": "Legacy System",
            "predicate": "uses_protocol",
            "object": "HTTP/1.0",
            "source": "legacy_spec.pdf",
            "timestamp": very_old_ts
        }
        res = self.evolution_engine.evaluate_and_evolve(ancient_fact)
        self.assertEqual(res.decision, EvolutionDecisionType.ARCHIVE)
        self.assertIn("marked for archiving", res.reasoning)

    # ----------------------------------------------------
    # Test Scenario 5: Conflicting Information -> CONFLICT DETECTED
    # ----------------------------------------------------
    def test_5_conflicting_information_detected(self):
        claim_a = KnowledgeClaim(
            id="c_01", subject="Python", predicate="version_released", object="3.11", timestamp="2022-10-01T00:00:00Z"
        )
        claim_b = KnowledgeClaim(
            id="c_02", subject="Python", predicate="version_released", object="3.12", timestamp="2023-10-01T00:00:00Z"
        )

        conflict = self.conflict_engine.detect_conflict(claim_b, [claim_a])
        self.assertIsNotNone(conflict)
        self.assertEqual(conflict.entity_subject, "Python")
        self.assertEqual(conflict.predicate, "version_released")

        # Resolve via policy
        resolved, directives = self.conflict_engine.resolve_conflict(conflict, policy="LATEST_WINS")
        self.assertEqual(directives["winning_claim_id"], "c_02")

    # ----------------------------------------------------
    # Test Scenario 6: Trust Score Calculation
    # ----------------------------------------------------
    def test_6_trust_score_calculation(self):
        claim = KnowledgeClaim(
            id="c_trust",
            subject="ChromaDB",
            predicate="stores",
            object="Vector Embeddings",
            source="journal_doc.pdf",
            source_type="peer_reviewed_journal",
            context_chunk="ChromaDB stores high dimensional vector embeddings with HNSW indexing."
        )
        breakdown = self.trust_engine.evaluate_claim_trust(claim, graph_agreement_score=0.9, retrieval_relevance_score=0.95)
        self.assertGreaterEqual(breakdown.overall_trust_score, 0.8)
        self.assertIn("High System Confidence", breakdown.interpretation)

    # ----------------------------------------------------
    # Test Scenario 7: Temporal Aging Decay
    # ----------------------------------------------------
    def test_7_temporal_aging_decay(self):
        recent_claim = KnowledgeClaim(id="r1", subject="A", predicate="B", object="C", timestamp=datetime.now(timezone.utc).isoformat())
        old_claim = KnowledgeClaim(id="o1", subject="A", predicate="B", object="C", timestamp=(datetime.now(timezone.utc) - timedelta(days=100)).isoformat())

        eval_recent = self.temporal_engine.evaluate_temporal_status(recent_claim)
        eval_old = self.temporal_engine.evaluate_temporal_status(old_claim)

        self.assertGreater(eval_recent["freshness_score"], eval_old["freshness_score"])

    # ----------------------------------------------------
    # Test Scenario 8: Incremental Neo4j & Vector Update
    # ----------------------------------------------------
    def test_8_incremental_update(self):
        claim = KnowledgeClaim(id="inc_01", subject="GraphRAG", predicate="uses", object="Neo4j")
        result = self.updater.apply_claim_update(claim, EvolutionDecisionType.ADD)
        self.assertTrue(result["incremental"])
        self.assertEqual(result["decision"], "ADD")

    # ----------------------------------------------------
    # Test Scenario 9: 4-Factor Adaptive Retrieval
    # ----------------------------------------------------
    def test_9_adaptive_retrieval(self):
        res = self.adaptive_retriever.adaptive_retrieve("What is GraphRAG?", top_k=3)
        self.assertIn("results", res)
        self.assertIn("applied_weights", res)
        self.assertGreater(len(res["results"]), 0)

    # ----------------------------------------------------
    # Test Scenario 10: Failure Handling (Malformed Data & Missing Metadata)
    # ----------------------------------------------------
    def test_10_failure_handling_malformed_data(self):
        malformed_input = {"subject": "", "predicate": "", "object": ""}
        res = self.evolution_engine.evaluate_and_evolve(malformed_input)
        self.assertEqual(res.decision, EvolutionDecisionType.REJECT)
        self.assertIn("missing required triple fields", res.reasoning)

    def test_11_failure_handling_missing_metadata(self):
        sparse_input = {"subject": "Test", "predicate": "has", "object": "Data"}
        res = self.evolution_engine.evaluate_and_evolve(sparse_input)
        self.assertIn(res.decision, [EvolutionDecisionType.ADD, EvolutionDecisionType.UPDATE])


if __name__ == "__main__":
    unittest.main()
