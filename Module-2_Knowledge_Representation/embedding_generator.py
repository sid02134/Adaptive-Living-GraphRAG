"""
Module 2: Knowledge Representation
File: embedding_generator.py
Purpose: Generate dense vector embeddings using SentenceTransformer (all-MiniLM-L6-v2).
"""

from typing import List, Union
import numpy as np

from pathlib import Path
try:
    from .config import Module2Config
    from .exceptions import EmbeddingError
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
        from exceptions import EmbeddingError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module2_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        EmbeddingError = getattr(_mod, "EmbeddingError")
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")



class EmbeddingGenerator:
    """Generates dense vector embeddings for input text strings using SentenceTransformer.

    Attributes:
        model_name (str): SentenceTransformer model identifier.
        model (SentenceTransformer): Loaded model instance.
    """

    def __init__(self, model_name: str = Module2Config.EMBEDDING_MODEL_NAME) -> None:
        """Initialize the EmbeddingGenerator with a specified model name.

        Args:
            model_name (str): SentenceTransformer model name. Defaults to all-MiniLM-L6-v2.
        """
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the SentenceTransformer model with fallback mechanisms."""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Initializing fallback deterministic embedding generator.")
            self.model = None

    def generate_embeddings(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """Generate dense vector embeddings for a text string or list of text strings.

        Args:
            texts (Union[str, List[str]]): Input text or list of texts.

        Returns:
            List[List[float]]: List of vector embeddings (each embedding is a list of floats).

        Raises:
            EmbeddingError: If vector generation fails.
        """
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return []

        try:
            if self.model is not None:
                embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
                return embeddings.tolist()
            else:
                # Deterministic fallback embedding generation (384 dimensions)
                logger.info(f"Generating fallback embeddings for {len(texts)} texts.")
                return [self._fallback_embedding(text) for text in texts]
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise EmbeddingError(f"Embedding generation error: {e}") from e

    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate vector embedding for a single string.

        Args:
            text (str): Input text string.

        Returns:
            List[float]: Vector embedding as a list of floats.
        """
        embeddings = self.generate_embeddings([text])
        return embeddings[0] if embeddings else []

    def _fallback_embedding(self, text: str, dim: int = 384) -> List[float]:
        """Generate deterministic fallback normalized float vector based on text hash.

        Args:
            text (str): Text input.
            dim (int): Vector dimensionality (384 for MiniLM-L6-v2).

        Returns:
            List[float]: Normalized pseudo-vector.
        """
        seed = sum(ord(c) for c in text) % (2**32)
        rng = np.random.RandomState(seed)
        vec = rng.randn(dim)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()


if __name__ == "__main__":
    generator = EmbeddingGenerator()
    sample_texts = [
        "GraphRAG integrates Knowledge Graphs and Vector Search.",
        "Adaptive living environment dynamically updates entity relations."
    ]
    embeddings = generator.generate_embeddings(sample_texts)
    print(f"Generated {len(embeddings)} embeddings. Dimension: {len(embeddings[0])}")
