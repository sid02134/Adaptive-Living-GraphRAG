"""
Module 2: Knowledge Representation
File: relationship_builder.py
Purpose: Construct directed relationships between nodes (Document, Chunk, Entity, Topic, Keyword).
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
try:
    from utils import logger
except (ImportError, AttributeError):
    import importlib.util
    _ut_path = Path(__file__).resolve().parent / "utils.py"
    _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    logger = getattr(_mod, "logger")


class RelationshipBuilder:
    """Builds graph relationships matching schema (CONTAINS, MENTIONS, RELATED_TO, BELONGS_TO, HAS_KEYWORD)."""

    def build_chunk_relationships(
        self,
        doc_name: str,
        chunk_id: str,
        chunk_text: str,
        entities: List[Dict[str, Any]],
        topics: List[str],
        keywords: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Build node-edge structures for a given text chunk.

        Args:
            doc_name (str): Source document filename.
            chunk_id (str): Unique chunk ID.
            chunk_text (str): Raw chunk text.
            entities (List[Dict[str, Any]]): Extracted entity dicts.
            topics (List[str]): Detected topic strings.
            keywords (List[str]): Extracted keyword strings.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Structured dictionary of relationships by type.
        """
        relationships = {
            "CONTAINS": [],      # Document -> Chunk
            "MENTIONS": [],      # Chunk -> Entity
            "RELATED_TO": [],    # Entity -> Entity
            "BELONGS_TO": [],    # Chunk / Entity -> Topic
            "HAS_KEYWORD": []    # Chunk -> Keyword
        }

        # 1. Document CONTAINS Chunk
        relationships["CONTAINS"].append({
            "source_type": "Document",
            "source_id": doc_name,
            "target_type": "Chunk",
            "target_id": chunk_id,
            "rel_type": "CONTAINS"
        })

        # 2. Chunk MENTIONS Entity
        for ent in entities:
            relationships["MENTIONS"].append({
                "source_type": "Chunk",
                "source_id": chunk_id,
                "target_type": "Entity",
                "target_id": ent["name"],
                "entity_label": ent["label"],
                "rel_type": "MENTIONS"
            })

        # 3. Entity RELATED_TO Entity (Co-occurrence within same chunk)
        entity_names = [e["name"] for e in entities]
        for i in range(len(entity_names)):
            for j in range(i + 1, len(entity_names)):
                relationships["RELATED_TO"].append({
                    "source_type": "Entity",
                    "source_id": entity_names[i],
                    "target_type": "Entity",
                    "target_id": entity_names[j],
                    "rel_type": "RELATED_TO",
                    "weight": 1.0,
                    "context_chunk": chunk_id
                })

        # 4. Chunk / Entity BELONGS_TO Topic
        for topic in topics:
            relationships["BELONGS_TO"].append({
                "source_type": "Chunk",
                "source_id": chunk_id,
                "target_type": "Topic",
                "target_id": topic,
                "rel_type": "BELONGS_TO"
            })

        # 5. Chunk HAS_KEYWORD Keyword
        for kw in keywords:
            relationships["HAS_KEYWORD"].append({
                "source_type": "Chunk",
                "source_id": chunk_id,
                "target_type": "Keyword",
                "target_id": kw,
                "rel_type": "HAS_KEYWORD"
            })

        return relationships


if __name__ == "__main__":
    builder = RelationshipBuilder()
    rel = builder.build_chunk_relationships(
        doc_name="sample.pdf",
        chunk_id="chunk_01",
        chunk_text="GraphRAG uses Neo4j and ChromaDB.",
        entities=[{"name": "Neo4j", "label": "ORG"}, {"name": "ChromaDB", "label": "ORG"}],
        topics=["Knowledge Graphs"],
        keywords=["graph", "vector"]
    )
    print("Built relationships:", {k: len(v) for k, v in rel.items()})
