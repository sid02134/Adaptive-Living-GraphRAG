"""
Module 3: GraphRAG Retrieval
File: graph_retriever.py
Purpose: Retrieve related entity subgraphs and connected chunks from Neo4j.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from .config import Module3Config
    from .exceptions import GraphSearchError
    from .utils import logger
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
    try:
        from exceptions import GraphSearchError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module3_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        GraphSearchError = getattr(_mod, "GraphSearchError")
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")


class GraphRetriever:
    """Retrieves entity subgraphs and connected chunks from Neo4j based on query entity matching.

    Attributes:
        entity_extractor (Any): EntityExtractor instance.
        neo4j_manager (Any): Neo4jManager instance.
    """

    def __init__(
        self,
        entity_extractor: Optional[Any] = None,
        neo4j_manager: Optional[Any] = None
    ) -> None:
        """Initialize GraphRetriever.

        Args:
            entity_extractor (Optional[Any]): Entity extractor instance.
            neo4j_manager (Optional[Any]): Neo4j database manager instance.
        """
        if entity_extractor is None:
            try:
                import importlib
                mod2 = importlib.import_module("Module-2_Knowledge_Representation.entity_extractor")
                EntityExtractor = getattr(mod2, "EntityExtractor")
                self.entity_extractor = EntityExtractor()
            except Exception as e:
                logger.warning(f"Using default EntityExtractor import: {e}")
                self.entity_extractor = None
        else:
            self.entity_extractor = entity_extractor

        if neo4j_manager is None:
            try:
                import importlib
                mod2 = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
                Neo4jManager = getattr(mod2, "Neo4jManager")
                self.neo4j_manager = Neo4jManager()
            except Exception as e:
                logger.warning(f"Using default Neo4jManager import: {e}")
                self.neo4j_manager = None
        else:
            self.neo4j_manager = neo4j_manager


    def retrieve(self, query: str, top_k: int = Module3Config.TOP_K) -> Dict[str, Any]:
        """Retrieve related subgraphs, entity connections, and graph relevance scores for query.

        Args:
            query (str): User query string.
            top_k (int): Result limit.

        Returns:
            Dict[str, Any]: Structured graph output containing entities, subgraphs, and graph_score map.

        Raises:
            GraphSearchError: If graph retrieval fails.
        """
        if not query or not query.strip():
            return {"entities": [], "subgraph": {"nodes": [], "edges": []}, "chunk_scores": {}}

        try:
            logger.info(f"Executing graph search for query: '{query}'")

            # 1. Extract query entities & keywords
            if self.entity_extractor is not None:
                entities = self.entity_extractor.extract_entities(query)
                keywords = self.entity_extractor.extract_keywords(query)
                entity_names = [e["name"] for e in entities] + keywords
            else:
                entity_names = [w for w in query.split() if len(w) > 3]

            if not entity_names:
                entity_names = [query]

            # 2. Query Neo4j subgraph
            if self.neo4j_manager is not None:
                subgraph = self.neo4j_manager.query_subgraph(entity_names=entity_names, max_depth=2)
            else:
                subgraph = {"nodes": [], "edges": []}

            # 3. Calculate graph relevance scores for connected chunks
            chunk_scores = {}
            for edge in subgraph.get("edges", []):
                src = edge.get("source", "")
                tgt = edge.get("target", "")

                for item in [src, tgt]:
                    if "chunk" in item.lower():
                        chunk_scores[item] = chunk_scores.get(item, 0.0) + 0.35

            logger.info(f"Graph search returned {len(subgraph.get('nodes', []))} node(s) and {len(subgraph.get('edges', []))} edge(s).")
            return {
                "query_entities": entity_names,
                "subgraph": subgraph,
                "chunk_scores": chunk_scores
            }
        except Exception as e:
            logger.error(f"Graph retrieval failed: {e}")
            raise GraphSearchError(f"Graph retrieval error: {e}") from e


if __name__ == "__main__":
    retriever = GraphRetriever()
    out = retriever.retrieve("Tell me about Neo4j and ChromaDB.")
    print("Graph Retriever Output Subgraph Nodes:", len(out["subgraph"]["nodes"]))
