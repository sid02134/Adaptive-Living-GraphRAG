"""
Module 6: Dynamic Knowledge Evolution
File: incremental_graph_updater.py
Purpose: Perform fine-grained incremental updates on Neo4j Knowledge Graph and ChromaDB Vector Store
         without full graph reconstruction.
"""

from typing import List, Dict, Any, Optional
import uuid

try:
    from .config import Module6Config
    from .models import KnowledgeClaim, ValidityStatus, EvolutionDecisionType
    from .utils import logger
    from .exceptions import IncrementalUpdateError
except (ImportError, ValueError):
    from config import Module6Config
    from models import KnowledgeClaim, ValidityStatus, EvolutionDecisionType
    from utils import logger
    from exceptions import IncrementalUpdateError

# Import Module 2 Managers if available
try:
    import importlib
    mod_nm = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
    Neo4jManager = getattr(mod_nm, "Neo4jManager")

    mod_cm = importlib.import_module("Module-2_Knowledge_Representation.chroma_manager")
    ChromaManager = getattr(mod_cm, "ChromaManager")

    mod_eg = importlib.import_module("Module-2_Knowledge_Representation.embedding_generator")
    EmbeddingGenerator = getattr(mod_eg, "EmbeddingGenerator")
except Exception:
    Neo4jManager = None
    ChromaManager = None
    EmbeddingGenerator = None


class IncrementalGraphUpdater:
    """Manages targeted incremental additions, updates, replacements, and status archiving in Neo4j & ChromaDB."""

    def __init__(
        self,
        neo4j_manager: Optional[Any] = None,
        chroma_manager: Optional[Any] = None,
        embedding_generator: Optional[Any] = None
    ) -> None:
        """Initialize IncrementalGraphUpdater."""
        self.neo4j_manager = neo4j_manager or (Neo4jManager() if Neo4jManager is not None else None)
        self.chroma_manager = chroma_manager or (ChromaManager() if ChromaManager is not None else None)
        self.embedding_generator = embedding_generator or (EmbeddingGenerator() if EmbeddingGenerator is not None else None)
        logger.info("IncrementalGraphUpdater initialized.")

    def apply_claim_update(
        self,
        claim: KnowledgeClaim,
        decision: EvolutionDecisionType,
        losing_claim_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Apply targeted incremental graph & vector store mutation based on evolution decision.

        Args:
            claim (KnowledgeClaim): The target claim.
            decision (EvolutionDecisionType): The evaluated decision (ADD, UPDATE, REPLACE, ARCHIVE, REJECT).
            losing_claim_id (Optional[str]): Optional ID of superseded/losing claim if replacing/resolving conflict.

        Returns:
            Dict[str, Any]: Execution result summary of graph and vector mutations.
        """
        if decision == EvolutionDecisionType.REJECT:
            logger.info(f"Claim {claim.id} REJECTED. No database mutations performed.")
            return {"status": "rejected", "neo4j_updated": False, "chroma_updated": False}

        neo4j_status = "skipped"
        chroma_status = "skipped"

        try:
            # 1. Update Neo4j Graph incrementally
            if self.neo4j_manager is not None and getattr(self.neo4j_manager, "driver", None) is not None:
                neo4j_res = self._update_neo4j(claim, decision, losing_claim_id)
                neo4j_status = neo4j_res.get("status", "success")
            else:
                neo4j_status = "simulated_success"
                logger.info(f"[Simulation] Neo4j incremental update '{decision.value}' applied for claim '{claim.id}'.")

            # 2. Update ChromaDB Vector Store incrementally
            if self.chroma_manager is not None and getattr(self.chroma_manager, "collection", None) is not None:
                chroma_res = self._update_chroma(claim, decision)
                chroma_status = chroma_res.get("status", "success")
            else:
                chroma_status = "simulated_success"
                logger.info(f"[Simulation] ChromaDB incremental vector update '{decision.value}' applied for claim '{claim.id}'.")

            return {
                "claim_id": claim.id,
                "decision": decision.value,
                "neo4j_status": neo4j_status,
                "chroma_status": chroma_status,
                "incremental": True
            }

        except Exception as e:
            logger.error(f"Incremental update failed for claim {claim.id}: {e}")
            raise IncrementalUpdateError(f"Incremental update execution error: {e}") from e

    def _update_neo4j(
        self,
        claim: KnowledgeClaim,
        decision: EvolutionDecisionType,
        losing_claim_id: Optional[str]
    ) -> Dict[str, Any]:
        """Execute Cypher MERGE/SET statements for incremental node/relationship mutation."""
        try:
            with self.neo4j_manager.driver.session() as session:
                sub = claim.subject.strip()
                obj = claim.object.strip()
                rel_type = claim.predicate.strip().upper().replace(" ", "_")

                # Ensure entity nodes exist
                session.run(
                    "MERGE (a:Entity {name: $sub}) ON CREATE SET a.created_at = $ts SET a.updated_at = $ts",
                    sub=sub, ts=claim.timestamp
                )
                session.run(
                    "MERGE (b:Entity {name: $obj}) ON CREATE SET b.created_at = $ts SET b.updated_at = $ts",
                    obj=obj, ts=claim.timestamp
                )

                if decision in [EvolutionDecisionType.ADD, EvolutionDecisionType.UPDATE]:
                    query = (
                        f"MATCH (a:Entity {{name: $sub}}), (b:Entity {{name: $obj}}) "
                        f"MERGE (a)-[r:{rel_type}]->(b) "
                        f"SET r.claim_id = $cid, r.source = $source, r.confidence = $conf, "
                        f"    r.updated_at = $ts, r.validity_status = $status"
                    )
                    session.run(
                        query,
                        sub=sub, obj=obj, cid=claim.id, source=claim.source,
                        conf=claim.confidence, ts=claim.timestamp, status=claim.validity_status.value
                    )

                elif decision == EvolutionDecisionType.REPLACE:
                    # Mark superseded relationship if losing_claim_id provided
                    if losing_claim_id:
                        session.run(
                            "MATCH ()-[r]->() WHERE r.claim_id = $losing_id SET r.validity_status = 'SUPERSEDED'",
                            losing_id=losing_claim_id
                        )
                    # Add new active relationship
                    query = (
                        f"MATCH (a:Entity {{name: $sub}}), (b:Entity {{name: $obj}}) "
                        f"MERGE (a)-[r:{rel_type}]->(b) "
                        f"SET r.claim_id = $cid, r.source = $source, r.confidence = $conf, "
                        f"    r.updated_at = $ts, r.validity_status = 'ACTIVE'"
                    )
                    session.run(
                        query, sub=sub, obj=obj, cid=claim.id, source=claim.source,
                        conf=claim.confidence, ts=claim.timestamp
                    )

                elif decision == EvolutionDecisionType.ARCHIVE:
                    query = (
                        f"MATCH (a:Entity {{name: $sub}})-[r:{rel_type}]->(b:Entity {{name: $obj}}) "
                        f"SET r.validity_status = 'ARCHIVED', r.updated_at = $ts"
                    )
                    session.run(query, sub=sub, obj=obj, ts=claim.timestamp)

            return {"status": "success"}
        except Exception as e:
            logger.warning(f"Neo4j Cypher incremental query failed: {e}")
            return {"status": "error", "message": str(e)}

    def _update_chroma(self, claim: KnowledgeClaim, decision: EvolutionDecisionType) -> Dict[str, Any]:
        """Add or update claim chunk in ChromaDB collection."""
        try:
            chunk_text = claim.context_chunk or f"{claim.subject} {claim.predicate} {claim.object}."
            chunk_id = f"claim_chunk_{claim.id}"
            metadata = {
                "source_file": claim.source,
                "source_type": claim.source_type,
                "timestamp": claim.timestamp,
                "validity_status": claim.validity_status.value if isinstance(claim.validity_status, ValidityStatus) else str(claim.validity_status),
                "decision": decision.value
            }

            if self.embedding_generator is not None:
                embeddings = self.embedding_generator.generate_embeddings([chunk_text])
            else:
                embeddings = None

            self.chroma_manager.add_chunks(
                chunks=[chunk_text],
                embeddings=embeddings,
                metadatas=[metadata],
                ids=[chunk_id]
            )
            return {"status": "success"}
        except Exception as e:
            logger.warning(f"ChromaDB incremental chunk addition failed: {e}")
            return {"status": "error", "message": str(e)}
