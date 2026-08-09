"""
Module 3: GraphRAG Retrieval
File: retriever.py
Purpose: Main GraphRAGRetriever pipeline orchestrating vector search, graph search, context fusion, and prompt building.
"""

from typing import Dict, Any, Optional
from pathlib import Path
try:
    from config import Module3Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module3_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module3Config = _mod.Module3Config
from hybrid_retriever import HybridRetriever
from context_builder import ContextBuilder
from prompt_builder import PromptBuilder
try:
    from utils import logger
except (ImportError, AttributeError):
    import importlib.util
    _ut_path = Path(__file__).resolve().parent / "utils.py"
    _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    logger = getattr(_mod, "logger")


class GraphRAGRetriever:
    """Master pipeline orchestrating vector, graph, hybrid retrieval, context building, and prompt generation.

    Attributes:
        hybrid_retriever (HybridRetriever): Hybrid search engine.
        context_builder (ContextBuilder): Context fusion engine.
        prompt_builder (PromptBuilder): Llama 3 prompt construction engine.
    """

    def __init__(
        self,
        hybrid_retriever: Optional[HybridRetriever] = None,
        context_builder: Optional[ContextBuilder] = None,
        prompt_builder: Optional[PromptBuilder] = None
    ) -> None:
        """Initialize GraphRAGRetriever pipeline."""
        self.hybrid_retriever = hybrid_retriever or HybridRetriever()
        self.context_builder = context_builder or ContextBuilder()
        self.prompt_builder = prompt_builder or PromptBuilder()
        logger.info("GraphRAGRetriever pipeline ready.")

    def run_retrieval_pipeline(
        self,
        query: str,
        top_k: int = Module3Config.TOP_K,
        alpha: float = Module3Config.HYBRID_ALPHA
    ) -> Dict[str, Any]:
        """Run complete retrieval pipeline for input query.

        Args:
            query (str): User query text.
            top_k (int): Number of top chunks to retrieve.
            alpha (float): Hybrid weighting coefficient (vector score weight).

        Returns:
            Dict[str, Any]: Complete retrieval result containing query, chunks, graph_context, context, prompt.
        """
        logger.info(f"Running GraphRAG retrieval pipeline for query: '{query}'")

        # 1. Execute Hybrid Search
        hybrid_output = self.hybrid_retriever.retrieve(query, top_k=top_k, alpha=alpha)

        # 2. Build Context String
        context_string = self.context_builder.build_context(hybrid_output)

        # 3. Assemble Prompt
        prompt_output = self.prompt_builder.build_prompt(query, context_string)

        result = {
            "query": query,
            "top_k": top_k,
            "alpha": alpha,
            "retrieved_chunks": hybrid_output.get("chunks", []),
            "graph_context": hybrid_output.get("graph_context", {}),
            "query_entities": hybrid_output.get("query_entities", []),
            "context_string": context_string,
            "prompt": prompt_output
        }

        logger.info("GraphRAG retrieval pipeline finished successfully.")
        return result


if __name__ == "__main__":
    retriever = GraphRAGRetriever()
    res = retriever.run_retrieval_pipeline("How does GraphRAG use ChromaDB and Neo4j?")
    print("\nRetrieval Pipeline Result Summary:\n")
    print("Chunks Retrieved:", len(res["retrieved_chunks"]))
    print("Entities Found:", res["query_entities"])
    print("Context Length:", len(res["context_string"]))
