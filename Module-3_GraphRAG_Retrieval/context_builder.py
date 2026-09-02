"""
Module 3: GraphRAG Retrieval
File: context_builder.py
Purpose: Fuse vector text chunks and Neo4j graph subgraphs into formatted context strings.
"""

from typing import List, Dict, Any
from pathlib import Path
try:
    from .exceptions import ContextBuildError
    from .utils import logger
except (ImportError, ValueError):
    try:
        from exceptions import ContextBuildError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module3_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        ContextBuildError = getattr(_mod, "ContextBuildError")
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")



class ContextBuilder:
    """Fuses retrieved text chunks and knowledge graph subgraphs into clean Markdown context.

    Attributes:
        max_context_length (int): Maximum character length of context block.
    """

    def __init__(self, max_context_length: int = 4000) -> None:
        """Initialize ContextBuilder with length limit.

        Args:
            max_context_length (int): Maximum length of context string.
        """
        self.max_context_length = max_context_length

    def build_context(
        self,
        retrieval_output: Dict[str, Any]
    ) -> str:
        """Build formatted Markdown context string from hybrid retrieval output.

        Args:
            retrieval_output (Dict[str, Any]): Output dictionary from HybridRetriever.

        Returns:
            str: Formatted Markdown context string.

        Raises:
            ContextBuildError: If formatting fails.
        """
        try:
            chunks = retrieval_output.get("chunks", [])
            graph_context = retrieval_output.get("graph_context", {})
            query_entities = retrieval_output.get("query_entities", [])

            lines = ["### RETRIEVED DOCUMENT CONTEXT\n"]

            if not chunks:
                lines.append("No relevant document text chunks found.\n")
            else:
                for idx, chunk in enumerate(chunks, start=1):
                    doc_name = chunk.get("metadata", {}).get("source_file", "unknown_source.pdf")
                    score = chunk.get("hybrid_score", 0.0)
                    text = chunk.get("document", "").strip()

                    lines.append(f"#### Source [{idx}]: {doc_name} (Relevance Score: {score:.2f})")
                    lines.append(f"```{text}```\n")

            # Append Graph Subgraph Knowledge
            nodes = graph_context.get("nodes", [])
            edges = graph_context.get("edges", [])

            lines.append("### KNOWLEDGE GRAPH CONNECTIONS\n")
            if query_entities:
                lines.append(f"**Identified Entities/Keywords:** {', '.join(query_entities)}")

            if nodes:
                entity_labels = [f"{n['id']} ({n.get('label', 'Entity')})" for n in nodes[:15]]
                lines.append(f"**Connected Knowledge Graph Nodes:** {', '.join(entity_labels)}")

            if edges:
                triplets = [f"({e['source']}) --[{e['relationship']}]--> ({e['target']})" for e in edges[:10]]
                lines.append("**Semantic Knowledge Triplets:**")
                for trip in triplets:
                    lines.append(f"- {trip}")
            else:
                lines.append("No entity-relation triplets retrieved for this query.")

            full_context = "\n".join(lines)
            if len(full_context) > self.max_context_length:
                full_context = full_context[:self.max_context_length] + "\n...[Context Truncated]"

            logger.info(f"Built context string of length {len(full_context)} characters.")
            return full_context
        except Exception as e:
            logger.error(f"Context build error: {e}")
            raise ContextBuildError(f"Failed to build context string: {e}") from e


if __name__ == "__main__":
    builder = ContextBuilder()
    sample_ret = {
        "chunks": [{"document": "GraphRAG integrates Neo4j.", "metadata": {"source_file": "doc1.pdf"}, "hybrid_score": 0.85}],
        "graph_context": {"nodes": [{"id": "Neo4j", "label": "ORG"}], "edges": [{"source": "GraphRAG", "target": "Neo4j", "relationship": "USES"}]},
        "query_entities": ["GraphRAG", "Neo4j"]
    }
    print("Formatted Context:\n" + "=" * 50)
    print(builder.build_context(sample_ret))
