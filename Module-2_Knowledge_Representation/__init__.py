"""
Module 2: Knowledge Representation Package
"""

import importlib

try:
    from .embedding_generator import EmbeddingGenerator
    from .chroma_manager import ChromaManager
    from .entity_extractor import EntityExtractor
    from .relationship_builder import RelationshipBuilder
    from .neo4j_manager import Neo4jManager
    from .graph_builder import GraphBuilder
except (ImportError, ValueError):
    try:
        mod_eg = importlib.import_module("Module-2_Knowledge_Representation.embedding_generator")
        EmbeddingGenerator = getattr(mod_eg, "EmbeddingGenerator")
        mod_cm = importlib.import_module("Module-2_Knowledge_Representation.chroma_manager")
        ChromaManager = getattr(mod_cm, "ChromaManager")
        mod_ee = importlib.import_module("Module-2_Knowledge_Representation.entity_extractor")
        EntityExtractor = getattr(mod_ee, "EntityExtractor")
        mod_rb = importlib.import_module("Module-2_Knowledge_Representation.relationship_builder")
        RelationshipBuilder = getattr(mod_rb, "RelationshipBuilder")
        mod_nm = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
        Neo4jManager = getattr(mod_nm, "Neo4jManager")
        mod_gb = importlib.import_module("Module-2_Knowledge_Representation.graph_builder")
        GraphBuilder = getattr(mod_gb, "GraphBuilder")
    except Exception:
        from embedding_generator import EmbeddingGenerator
        from chroma_manager import ChromaManager
        from entity_extractor import EntityExtractor
        from relationship_builder import RelationshipBuilder
        from neo4j_manager import Neo4jManager
        from graph_builder import GraphBuilder

__all__ = [
    "EmbeddingGenerator",
    "ChromaManager",
    "EntityExtractor",
    "RelationshipBuilder",
    "Neo4jManager",
    "GraphBuilder"
]
