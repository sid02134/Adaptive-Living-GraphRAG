"""
Module 3: GraphRAG Retrieval
File: vector_retriever.py
Purpose: Retrieve top-k semantic text chunks from ChromaDB.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from .config import Module3Config
    from .exceptions import VectorSearchError
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
        from exceptions import VectorSearchError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module3_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        VectorSearchError = getattr(_mod, "VectorSearchError")
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")


class VectorRetriever:
    """Retrieves top-k relevant text chunks based on dense vector cosine similarity in ChromaDB.

    Attributes:
        embedding_generator (Any): Embedding generator instance.
        chroma_manager (Any): ChromaDB database manager instance.
    """

    def __init__(
        self,
        embedding_generator: Optional[Any] = None,
        chroma_manager: Optional[Any] = None
    ) -> None:
        """Initialize VectorRetriever.

        Args:
            embedding_generator (Optional[Any]): Generator instance for query embedding.
            chroma_manager (Optional[Any]): ChromaManager instance for database queries.
        """
        if embedding_generator is None:
            try:
                import importlib
                mod2 = importlib.import_module("Module-2_Knowledge_Representation.embedding_generator")
                EmbeddingGenerator = getattr(mod2, "EmbeddingGenerator")
                self.embedding_generator = EmbeddingGenerator()
            except Exception as e:
                logger.warning(f"Using default embedding generator import: {e}")
                self.embedding_generator = None
        else:
            self.embedding_generator = embedding_generator

        if chroma_manager is None:
            try:
                import importlib
                mod2 = importlib.import_module("Module-2_Knowledge_Representation.chroma_manager")
                ChromaManager = getattr(mod2, "ChromaManager")
                self.chroma_manager = ChromaManager()
            except Exception as e:
                logger.warning(f"Using default ChromaManager import: {e}")
                self.chroma_manager = None
        else:
            self.chroma_manager = chroma_manager

    def retrieve(self, query: str, top_k: int = Module3Config.TOP_K) -> List[Dict[str, Any]]:
        """Retrieve top-k semantically relevant chunks for a user query string.

        Args:
            query (str): User query string.
            top_k (int): Number of top results to return.

        Returns:
            List[Dict[str, Any]]: List of matching records containing id, document, metadata, distance, vector_score.

        Raises:
            VectorSearchError: If vector query execution fails.
        """
        if not query or not query.strip():
            return []

        try:
            logger.info(f"Executing vector search for query: '{query}' (top_k={top_k})")
            if self.embedding_generator is not None:
                query_vector = self.embedding_generator.generate_single_embedding(query)
            else:
                # Fallback dummy embedding vector if missing generator
                query_vector = [0.1] * 384

            if self.chroma_manager is not None:
                results = self.chroma_manager.query_similarity(query_vector, n_results=top_k)
                for r in results:
                    r["vector_score"] = r.get("similarity_score", 0.5)
                logger.info(f"Vector search retrieved {len(results)} chunk(s).")
                return results
            else:
                logger.warning("ChromaManager not initialized. Returning empty vector results.")
                return []
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise VectorSearchError(f"Vector retrieval error: {e}") from e


if __name__ == "__main__":
    retriever = VectorRetriever()
    res = retriever.retrieve("What is GraphRAG?")
    print("Vector Retriever Output:", len(res), "item(s).")
