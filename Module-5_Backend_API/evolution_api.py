"""
Module 5: Backend API
File: evolution_api.py
Purpose: FastAPI APIRouter for Module 6 Dynamic Knowledge Evolution endpoints.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

# Ensure root workspace directory is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import importlib
mod_ee = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.evolution_engine")
AdaptiveKnowledgeEvolutionEngine = getattr(mod_ee, "AdaptiveKnowledgeEvolutionEngine")

mod_cr = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.conflict_engine")
ConflictResolutionEngine = getattr(mod_cr, "ConflictResolutionEngine")

mod_ar = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.adaptive_retriever")
AdaptiveRetrievalEngine = getattr(mod_ar, "AdaptiveRetrievalEngine")

mod_cfg = importlib.import_module("Module-6_Dynamic_Knowledge_Evolution.config")
Module6Config = getattr(mod_cfg, "Module6Config")


# Initialize router with tag
router = APIRouter(prefix="/evolution", tags=["Dynamic Knowledge Evolution"])

# Instantiate Module 6 Engine Singleton
evolution_engine = AdaptiveKnowledgeEvolutionEngine()
adaptive_retriever = AdaptiveRetrievalEngine()


# ----------------------------------------------------
# Pydantic Schemas for Request & Response Body
# ----------------------------------------------------
class KnowledgeUpdatePayload(BaseModel):
    subject: str = Field(..., description="Subject entity name")
    predicate: str = Field(..., description="Relationship/predicate title")
    object: str = Field(..., description="Object entity or property value")
    source: Optional[str] = Field("user_input", description="Source document or origin")
    source_type: Optional[str] = Field("general", description="Source category for reliability rating")
    timestamp: Optional[str] = Field(None, description="ISO timestamp string")
    confidence: Optional[float] = Field(0.8, ge=0.0, le=1.0, description="Initial confidence")
    context_chunk: Optional[str] = Field("", description="Supporting context text chunk")
    conflict_policy_override: Optional[str] = Field(None, description="Optional conflict policy override")


class ConflictFeedbackPayload(BaseModel):
    conflict_id: str = Field(..., description="ID of conflict record")
    winning_claim_id: str = Field(..., description="Claim ID chosen as winning claim or 'PRESERVE_BOTH'")
    rationale: Optional[str] = Field("User manual feedback override", description="Rationale description")


class AdaptiveQueryPayload(BaseModel):
    query: str = Field(..., min_length=2, description="Query string")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Top results count")
    include_historical: Optional[bool] = Field(False, description="Whether to include archived/superseded facts")
    vector_weight: Optional[float] = Field(0.35, ge=0.0, le=1.0, description="Vector score weight")
    graph_weight: Optional[float] = Field(0.25, ge=0.0, le=1.0, description="Graph score weight")
    trust_weight: Optional[float] = Field(0.20, ge=0.0, le=1.0, description="Trust score weight")
    freshness_weight: Optional[float] = Field(0.20, ge=0.0, le=1.0, description="Freshness score weight")


# ----------------------------------------------------
# API Endpoint Routes
# ----------------------------------------------------

@router.post("/update", summary="Submit incoming knowledge fact for dynamic evolution")
async def update_knowledge(payload: KnowledgeUpdatePayload):
    """Evaluate an incoming claim against existing knowledge and apply ADD/UPDATE/REPLACE/ARCHIVE decision."""
    try:
        data = payload.model_dump()
        override = data.pop("conflict_policy_override", None)
        result = evolution_engine.evaluate_and_evolve(data, conflict_policy_override=override)
        return {
            "status": "success",
            "evolution_result": result.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge evolution update failed: {str(e)}")


@router.post("/feedback", summary="Submit manual conflict resolution feedback")
async def resolve_conflict_feedback(payload: ConflictFeedbackPayload):
    """Apply manual override feedback to resolve a flagged conflict."""
    try:
        conflicts = ConflictResolutionEngine.get_all_conflicts()
        target = next((c for c in conflicts if c.get("conflict_id") == payload.conflict_id), None)
        if not target:
            raise HTTPException(status_code=404, detail=f"Conflict ID '{payload.conflict_id}' not found.")

        target["resolution_status"] = f"RESOLVED_MANUAL_{payload.winning_claim_id}"
        target["winning_claim_id"] = payload.winning_claim_id
        target["applied_policy"] = "MANUAL_FEEDBACK"
        target["rationale"] = payload.rationale

        return {
            "status": "success",
            "message": f"Conflict '{payload.conflict_id}' updated successfully.",
            "conflict_record": target
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conflict feedback update failed: {str(e)}")


@router.get("/history", summary="Get knowledge evolution audit history")
async def get_evolution_history(limit: int = Query(50, ge=1, le=500)):
    """Retrieve audit history log of evolution decisions."""
    try:
        history = evolution_engine.get_evolution_history()
        return {
            "status": "success",
            "total_records": len(history),
            "history": history[-limit:]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch evolution history: {str(e)}")


@router.get("/conflicts", summary="Get all detected knowledge conflicts")
async def get_conflicts():
    """Retrieve list of all active and resolved knowledge contradictions."""
    try:
        conflicts = ConflictResolutionEngine.get_all_conflicts()
        return {
            "status": "success",
            "total_conflicts": len(conflicts),
            "conflicts": conflicts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conflicts: {str(e)}")


@router.get("/status", summary="Get Module 6 engine status and configuration")
async def get_evolution_status():
    """Retrieve status metrics and engine parameters for Module 6."""
    try:
        history = evolution_engine.get_evolution_history()
        conflicts = ConflictResolutionEngine.get_all_conflicts()
        decisions_summary = {
            "ADD": sum(1 for h in history if h.get("decision") == "ADD"),
            "UPDATE": sum(1 for h in history if h.get("decision") == "UPDATE"),
            "REPLACE": sum(1 for h in history if h.get("decision") == "REPLACE"),
            "ARCHIVE": sum(1 for h in history if h.get("decision") == "ARCHIVE"),
            "REJECT": sum(1 for h in history if h.get("decision") == "REJECT"),
        }

        return {
            "status": "active",
            "module_name": "Module 6: Dynamic Knowledge Evolution",
            "engines": [
                "1. Adaptive Knowledge Evolution Engine",
                "2. Conflict Resolution Engine",
                "3. Trust & Confidence Engine",
                "4. Temporal Knowledge Aging Engine",
                "5. Adaptive Retrieval Engine"
            ],
            "decisions_summary": decisions_summary,
            "total_conflicts_logged": len(conflicts),
            "configuration": {
                "default_conflict_policy": Module6Config.DEFAULT_CONFLICT_POLICY,
                "lambda_decay": Module6Config.LAMBDA_DECAY,
                "outdated_threshold_days": Module6Config.OUTDATED_THRESHOLD_DAYS,
                "archive_threshold_days": Module6Config.ARCHIVE_THRESHOLD_DAYS,
                "adaptive_retrieval_weights": Module6Config.ADAPTIVE_RETRIEVAL_WEIGHTS
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch evolution status: {str(e)}")


@router.post("/query", summary="Execute 4-factor adaptive retrieval query")
async def adaptive_query(payload: AdaptiveQueryPayload):
    """Execute 4-factor adaptive retrieval (Vector + Graph + Trust + Freshness)."""
    try:
        weights = {
            "vector_weight": payload.vector_weight,
            "graph_weight": payload.graph_weight,
            "trust_weight": payload.trust_weight,
            "freshness_weight": payload.freshness_weight
        }
        results = adaptive_retriever.adaptive_retrieve(
            query=payload.query,
            top_k=payload.top_k,
            include_historical=payload.include_historical,
            custom_weights=weights
        )
        return {
            "status": "success",
            "adaptive_retrieval": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adaptive retrieval query failed: {str(e)}")
