"""
Module 3: GraphRAG Retrieval Package
"""

import importlib

try:
    from .vector_retriever import VectorRetriever
    from .graph_retriever import GraphRetriever
    from .hybrid_retriever import HybridRetriever
    from .context_builder import ContextBuilder
    from .prompt_builder import PromptBuilder
    from .retriever import GraphRAGRetriever
except (ImportError, ValueError):
    try:
        mod_vr = importlib.import_module("Module-3_GraphRAG_Retrieval.vector_retriever")
        VectorRetriever = getattr(mod_vr, "VectorRetriever")
        mod_gr = importlib.import_module("Module-3_GraphRAG_Retrieval.graph_retriever")
        GraphRetriever = getattr(mod_gr, "GraphRetriever")
        mod_hr = importlib.import_module("Module-3_GraphRAG_Retrieval.hybrid_retriever")
        HybridRetriever = getattr(mod_hr, "HybridRetriever")
        mod_cb = importlib.import_module("Module-3_GraphRAG_Retrieval.context_builder")
        ContextBuilder = getattr(mod_cb, "ContextBuilder")
        mod_pb = importlib.import_module("Module-3_GraphRAG_Retrieval.prompt_builder")
        PromptBuilder = getattr(mod_pb, "PromptBuilder")
        mod_ret = importlib.import_module("Module-3_GraphRAG_Retrieval.retriever")
        GraphRAGRetriever = getattr(mod_ret, "GraphRAGRetriever")
    except Exception:
        from vector_retriever import VectorRetriever
        from graph_retriever import GraphRetriever
        from hybrid_retriever import HybridRetriever
        from context_builder import ContextBuilder
        from prompt_builder import PromptBuilder
        from retriever import GraphRAGRetriever

__all__ = [
    "VectorRetriever",
    "GraphRetriever",
    "HybridRetriever",
    "ContextBuilder",
    "PromptBuilder",
    "GraphRAGRetriever"
]
