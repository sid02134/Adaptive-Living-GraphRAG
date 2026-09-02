"""
Module 2: Knowledge Representation
File: test_module2.py
Purpose: Unit and integration tests for Module 2 components.
"""

import sys
try:
    import pytest
except ImportError:
    pytest = None
from pathlib import Path

import importlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    mod2_cfg = importlib.import_module("Module-2_Knowledge_Representation.config")
    Module2Config = getattr(mod2_cfg, "Module2Config")
    mod2_eg = importlib.import_module("Module-2_Knowledge_Representation.embedding_generator")
    EmbeddingGenerator = getattr(mod2_eg, "EmbeddingGenerator")
    mod2_cm = importlib.import_module("Module-2_Knowledge_Representation.chroma_manager")
    ChromaManager = getattr(mod2_cm, "ChromaManager")
    mod2_ee = importlib.import_module("Module-2_Knowledge_Representation.entity_extractor")
    EntityExtractor = getattr(mod2_ee, "EntityExtractor")
    mod2_rb = importlib.import_module("Module-2_Knowledge_Representation.relationship_builder")
    RelationshipBuilder = getattr(mod2_rb, "RelationshipBuilder")
    mod2_nm = importlib.import_module("Module-2_Knowledge_Representation.neo4j_manager")
    Neo4jManager = getattr(mod2_nm, "Neo4jManager")
    mod2_gb = importlib.import_module("Module-2_Knowledge_Representation.graph_builder")
    GraphBuilder = getattr(mod2_gb, "GraphBuilder")
except Exception:
    from config import Module2Config
    from embedding_generator import EmbeddingGenerator
    from chroma_manager import ChromaManager
    from entity_extractor import EntityExtractor
    from relationship_builder import RelationshipBuilder
    from neo4j_manager import Neo4jManager
    from graph_builder import GraphBuilder




def test_embedding_generator():
    """Test vector embedding generation."""
    generator = EmbeddingGenerator()
    texts = ["Test sentence for GraphRAG vector embedding."]
    embeddings = generator.generate_embeddings(texts)
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384
    print("\n[PASSED] EmbeddingGenerator test")


def test_chroma_manager():
    """Test ChromaDB chunk storage and vector similarity search."""
    manager = ChromaManager(collection_name="test_collection")
    chunks = ["GraphRAG combines vector search with graph indexing."]
    embeddings = [[0.1] * 384]
    metadatas = [{"source": "test.pdf"}]

    ids = manager.add_chunks(chunks, embeddings, metadatas)
    assert len(ids) == 1

    results = manager.query_similarity(embeddings[0], n_results=1)
    assert len(results) >= 1
    print("[PASSED] ChromaManager test")


def test_entity_extractor():
    """Test spaCy entity, keyword, and topic extraction."""
    extractor = EntityExtractor()
    sample = "Neo4j and ChromaDB are used by AI researchers in San Francisco."
    entities = extractor.extract_entities(sample)
    keywords = extractor.extract_keywords(sample)
    topics = extractor.extract_topics(sample)

    assert isinstance(entities, list)
    assert isinstance(keywords, list)
    assert isinstance(topics, list)
    print("[PASSED] EntityExtractor test")


def test_relationship_builder():
    """Test relationship creation."""
    builder = RelationshipBuilder()
    rels = builder.build_chunk_relationships(
        doc_name="test.pdf",
        chunk_id="chk_0",
        chunk_text="GraphRAG uses Llama 3.",
        entities=[{"name": "Llama 3", "label": "MODEL"}],
        topics=["LLM Systems"],
        keywords=["graphrag"]
    )
    assert "CONTAINS" in rels
    assert "MENTIONS" in rels
    assert "BELONGS_TO" in rels
    print("[PASSED] RelationshipBuilder test")


def test_graph_builder_integration():
    """Test full pipeline integration from processed documents to vector and graph stores."""
    sample_docs = [
        {
            "filename": "integration_test.pdf",
            "chunks": [
                "GraphRAG is a trust-aware retrieval framework.",
                "It uses Sentence Transformers to embed document text."
            ]
        }
    ]
    builder = GraphBuilder()
    summary = builder.build_knowledge_graph(sample_docs)
    assert summary["status"] == "success"
    assert summary["total_chunks"] == 2
    print("[PASSED] GraphBuilder Integration test")


if __name__ == "__main__":
    print("\nRunning Module 2 Unit & Integration Tests...\n" + "=" * 50)
    test_embedding_generator()
    test_chroma_manager()
    test_entity_extractor()
    test_relationship_builder()
    test_graph_builder_integration()
    print("=" * 50 + "\nAll Module 2 Tests Passed Successfully!\n")
