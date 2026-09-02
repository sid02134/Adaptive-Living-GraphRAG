"""
Module 2: Knowledge Representation
File: chroma_manager.py
Purpose: Manage ChromaDB collection persistent storage and vector search queries.
"""

import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from .config import Module2Config
    from .exceptions import ChromaDBError
    from .utils import logger
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
    try:
        from exceptions import ChromaDBError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module2_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        ChromaDBError = getattr(_mod, "ChromaDBError")
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")



class ChromaManager:
    """Manages persistent document storage and similarity search in ChromaDB.

    Attributes:
        db_path (str): Persistent directory path for ChromaDB.
        collection_name (str): ChromaDB collection name.
        client (Any): ChromaDB client instance.
        collection (Any): Active ChromaDB collection handle.
    """

    def __init__(
        self,
        db_path: str = Module2Config.CHROMADB_PATH,
        collection_name: str = Module2Config.COLLECTION_NAME
    ) -> None:
        """Initialize ChromaManager with database path and collection name.

        Args:
            db_path (str): Directory path to persist ChromaDB storage.
            collection_name (str): Name of collection to store vector chunks.
        """
        self.db_path = db_path
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._init_db()

    def _init_db(self) -> None:
        """Initialize ChromaDB client and get or create target collection."""
        try:
            os.makedirs(self.db_path, exist_ok=True)
            import chromadb

            logger.info(f"Initializing ChromaDB persistent client at: {self.db_path}")
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"ChromaDB collection '{self.collection_name}' ready. Count: {self.collection.count()}")
        except Exception as e:
            logger.warning(f"Could not initialize native ChromaDB client ({e}). Initializing in-memory fallback vector store.")
            self._init_fallback_store()

    def _init_fallback_store(self) -> None:
        """Initialize lightweight fallback vector storage dictionary for offline operations."""
        self.fallback_data = []  # List of dicts with id, document, embedding, metadata

    def add_chunks(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add text chunks, embeddings, and metadatas to ChromaDB collection.

        Args:
            chunks (List[str]): List of text chunk strings.
            embeddings (List[List[float]]): Corresponding dense vector embeddings.
            metadatas (List[Dict[str, Any]]): Metadata dictionaries for each chunk.
            ids (Optional[List[str]]): Optional list of unique chunk IDs.

        Returns:
            List[str]: List of generated/provided chunk IDs.

        Raises:
            ChromaDBError: If insertion fails.
        """
        if not chunks:
            return []

        if ids is None:
            ids = [f"chunk_{uuid.uuid4().hex[:8]}" for _ in range(len(chunks))]

        try:
            if self.collection is not None:
                self.collection.add(
                    documents=chunks,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully added {len(chunks)} chunks to ChromaDB collection '{self.collection_name}'.")
            else:
                for chunk, emb, meta, cid in zip(chunks, embeddings, metadatas, ids):
                    self.fallback_data.append({
                        "id": cid,
                        "document": chunk,
                        "embedding": emb,
                        "metadata": meta
                    })
                logger.info(f"Added {len(chunks)} chunks to fallback vector store.")
            return ids
        except Exception as e:
            logger.error(f"Failed to add chunks to ChromaDB: {e}")
            raise ChromaDBError(f"ChromaDB insertion error: {e}") from e

    def query_similarity(
        self,
        query_embedding: List[float],
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Query ChromaDB for vector similarity matching.

        Args:
            query_embedding (List[float]): Query vector embedding.
            n_results (int): Number of top results to retrieve.

        Returns:
            List[Dict[str, Any]]: List of matching records containing id, document, distance, similarity, metadata.
        """
        try:
            if self.collection is not None:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    include=["documents", "metadatas", "distances"]
                )

                formatted = []
                if results and "ids" in results and results["ids"]:
                    ids = results["ids"][0]
                    docs = results["documents"][0]
                    metas = results["metadatas"][0]
                    dists = results["distances"][0]

                    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
                        # Cosine distance to similarity: similarity = 1 - distance
                        similarity = max(0.0, min(1.0, 1.0 - float(dist)))
                        formatted.append({
                            "id": cid,
                            "document": doc,
                            "metadata": meta,
                            "distance": float(dist),
                            "similarity_score": similarity
                        })
                return formatted
            else:
                return self._fallback_query(query_embedding, n_results)
        except Exception as e:
            logger.error(f"ChromaDB query failed: {e}")
            raise ChromaDBError(f"ChromaDB query error: {e}") from e

    def _fallback_query(self, query_embedding: List[float], n_results: int) -> List[Dict[str, Any]]:
        """Perform fallback cosine similarity calculation across fallback store.

        Args:
            query_embedding (List[float]): Query vector.
            n_results (int): Number of top matches.

        Returns:
            List[Dict[str, Any]]: Top matches list.
        """
        import numpy as np
        if not hasattr(self, "fallback_data") or not self.fallback_data:
            return []

        q_vec = np.array(query_embedding)
        q_norm = np.linalg.norm(q_vec)

        scored = []
        for item in self.fallback_data:
            c_vec = np.array(item["embedding"])
            c_norm = np.linalg.norm(c_vec)
            if q_norm > 0 and c_norm > 0:
                sim = float(np.dot(q_vec, c_vec) / (q_norm * c_norm))
            else:
                sim = 0.0
            dist = 1.0 - sim
            scored.append({
                "id": item["id"],
                "document": item["document"],
                "metadata": item["metadata"],
                "distance": dist,
                "similarity_score": sim
            })

        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:n_results]

    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics.

        Returns:
            Dict[str, Any]: Count and collection details.
        """
        if self.collection is not None:
            return {
                "collection_name": self.collection_name,
                "total_chunks": self.collection.count(),
                "db_path": self.db_path
            }
        return {
            "collection_name": self.collection_name,
            "total_chunks": len(getattr(self, "fallback_data", [])),
            "db_path": "in_memory_fallback"
        }


if __name__ == "__main__":
    manager = ChromaManager()
    stats = manager.get_stats()
    print("ChromaManager initialized:", stats)
