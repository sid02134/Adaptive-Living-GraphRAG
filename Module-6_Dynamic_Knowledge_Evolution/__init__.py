"""
Module 6: Dynamic Knowledge Evolution Package
"""

import importlib

try:
    from .evolution_engine import AdaptiveKnowledgeEvolutionEngine
    from .conflict_engine import ConflictResolutionEngine
    from .trust_confidence_engine import TrustConfidenceEngine
    from .temporal_aging_engine import TemporalKnowledgeAgingEngine
    from .adaptive_retriever import AdaptiveRetrievalEngine
    from .incremental_graph_updater import IncrementalGraphUpdater
    from .config import Module6Config
    from .models import KnowledgeClaim, EvolutionDecisionType, ConflictRecord, ValidityStatus
except (ImportError, ValueError):
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
    
    mod_cfg = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.config")
    Module6Config = getattr(mod_cfg, "Module6Config")
    
    mod_md = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.models")
    KnowledgeClaim = getattr(mod_md, "KnowledgeClaim")
    EvolutionDecisionType = getattr(mod_md, "EvolutionDecisionType")
    ConflictRecord = getattr(mod_md, "ConflictRecord")
    ValidityStatus = getattr(mod_md, "ValidityStatus")

__all__ = [
    "AdaptiveKnowledgeEvolutionEngine",
    "ConflictResolutionEngine",
    "TrustConfidenceEngine",
    "TemporalKnowledgeAgingEngine",
    "AdaptiveRetrievalEngine",
    "IncrementalGraphUpdater",
    "Module6Config",
    "KnowledgeClaim",
    "EvolutionDecisionType",
    "ConflictRecord",
    "ValidityStatus"
]
