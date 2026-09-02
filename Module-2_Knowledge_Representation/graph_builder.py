"""
Module 2: Knowledge Representation
File: graph_builder.py
Purpose: Complete pipeline integrating Module 1 documents with ChromaDB vector store and Neo4j graph.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure parent directory is in Python path to import Module 1 if needed
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from .config import Module2Config
    from .embedding_generator import EmbeddingGenerator
    from .chroma_manager import ChromaManager
    from .entity_extractor import EntityExtractor
    from .relationship_builder import RelationshipBuilder
    from .neo4j_manager import Neo4jManager
    from .utils import logger, setup_logger
except (ImportError, ValueError):
    try:
        from config import Module2Config
    except (ImportError, AttributeError):
        import importlib.util
        _cfg_path = Path(__file__).resolve().parent / "config.py"
        _spec = importlib.util.spec_from_file_location("module2_config", _cfg_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        Module2Config = _mod.Module2Config
    from embedding_generator import EmbeddingGenerator
    from chroma_manager import ChromaManager
    from entity_extractor import EntityExtractor
    from relationship_builder import RelationshipBuilder
    from neo4j_manager import Neo4jManager
    try:
        from utils import logger, setup_logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")
        setup_logger = getattr(_mod, "setup_logger")



class GraphBuilder:
    """Master pipeline orchestrating vector store creation and knowledge graph construction.

    Attributes:
        embedding_generator (EmbeddingGenerator): Generator for 384-d sentence embeddings.
        chroma_manager (ChromaManager): Vector store database manager.
        entity_extractor (EntityExtractor): NLP entity and keyword extractor.
        relationship_builder (RelationshipBuilder): Entity relationship builder.
        neo4j_manager (Neo4jManager): Neo4j graph database manager.
    """

    def __init__(self) -> None:
        """Initialize all pipeline component managers."""
        logger.info("Initializing GraphBuilder pipeline...")
        self.embedding_generator = EmbeddingGenerator()
        self.chroma_manager = ChromaManager()
        self.entity_extractor = EntityExtractor()
        self.relationship_builder = RelationshipBuilder()
        self.neo4j_manager = Neo4jManager()

    def build_knowledge_graph(self, processed_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process document chunks into vector embeddings and Neo4j knowledge graph.

        Args:
            processed_documents (List[Dict[str, Any]]): List of doc dicts containing filename and chunks.
                Format: [{"filename": "doc.pdf", "chunks": ["text1", "text2"]}]

        Returns:
            Dict[str, Any]: Execution summary containing stats on chunks, entities, and relationships created.
        """
        if not processed_documents:
            logger.warning("No documents provided to GraphBuilder.")
            return {"status": "empty", "total_documents": 0, "total_chunks": 0}

        total_chunks = 0
        total_entities = 0
        all_relationships = {
            "CONTAINS": [],
            "MENTIONS": [],
            "RELATED_TO": [],
            "BELONGS_TO": [],
            "HAS_KEYWORD": []
        }

        logger.info(f"Beginning knowledge graph building for {len(processed_documents)} document(s).")

        for doc in processed_documents:
            doc_name = doc.get("filename", "unknown_document.pdf")
            chunks = doc.get("chunks", [])

            if not chunks:
                continue

            logger.info(f"Processing '{doc_name}' ({len(chunks)} chunks)...")

            # 1. Generate Embeddings
            embeddings = self.embedding_generator.generate_embeddings(chunks)

            # 2. Build Metadatas & IDs
            metadatas = [
                {
                    "source_file": doc_name,
                    "chunk_index": i,
                    "character_count": len(chunk_text)
                }
                for i, chunk_text in enumerate(chunks)
            ]
            chunk_ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]

            # 3. Store Vectors in ChromaDB
            self.chroma_manager.add_chunks(
                chunks=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=chunk_ids
            )

            # 4. Extract Entities, Topics, Keywords, & Build Graph Relationships
            for chunk_id, chunk_text in zip(chunk_ids, chunks):
                entities = self.entity_extractor.extract_entities(chunk_text)
                keywords = self.entity_extractor.extract_keywords(chunk_text)
                topics = self.entity_extractor.extract_topics(chunk_text)

                total_entities += len(entities)

                chunk_rels = self.relationship_builder.build_chunk_relationships(
                    doc_name=doc_name,
                    chunk_id=chunk_id,
                    chunk_text=chunk_text,
                    entities=entities,
                    topics=topics,
                    keywords=keywords
                )

                for rel_key, rel_list in chunk_rels.items():
                    all_relationships[rel_key].extend(rel_list)

            total_chunks += len(chunks)

        # 5. Insert Relationships into Neo4j
        logger.info("Batch inserting extracted nodes and relationships into Neo4j...")
        self.neo4j_manager.batch_insert_graph_data(all_relationships)

        summary = {
            "status": "success",
            "total_documents": len(processed_documents),
            "total_chunks": total_chunks,
            "total_entities_extracted": total_entities,
            "relationships_created": {k: len(v) for k, v in all_relationships.items()}
        }

        logger.info(f"GraphBuilder pipeline completed successfully: {summary}")
        return summary

    def build_from_module1(self) -> Dict[str, Any]:
        """Convenience method to import Module 1 DocumentManager and build the graph.

        Returns:
            Dict[str, Any]: Processing execution summary.
        """
        try:
            import importlib
            mod = importlib.import_module("Module-1_Document_Ingestion.document_manager")
            DocumentManager = getattr(mod, "DocumentManager")
            doc_mgr = DocumentManager()
            processed_docs = doc_mgr.process_documents()
            return self.build_knowledge_graph(processed_docs)
        except Exception as e:
            logger.error(f"Failed to load or process documents from Module 1: {e}")
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    sample_docs = [
        {
            "filename": "GraphRAG_Overview.pdf",
            "chunks": [
                "GraphRAG is an advanced Retrieval-Augmented Generation framework.",
                "It combines Knowledge Graphs in Neo4j with Vector Search in ChromaDB and Llama 3."
            ]
        }
    ]
    builder = GraphBuilder()
    res = builder.build_knowledge_graph(sample_docs)
    print("\nGraph Construction Result Summary:\n", res)
