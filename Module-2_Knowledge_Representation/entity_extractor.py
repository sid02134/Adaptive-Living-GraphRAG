"""
Module 2: Knowledge Representation
File: entity_extractor.py
Purpose: Extract named entities, topics, and keywords using spaCy NLP.
"""

import re
from typing import List, Dict, Any, Set
from pathlib import Path
try:
    from .config import Module2Config
    from .exceptions import EntityExtractionError
    from .utils import logger, clean_entity_text
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
        from exceptions import EntityExtractionError
    except (ImportError, AttributeError):
        import importlib.util
        _ex_path = Path(__file__).resolve().parent / "exceptions.py"
        _spec = importlib.util.spec_from_file_location("module2_exceptions", _ex_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        EntityExtractionError = getattr(_mod, "EntityExtractionError")
    try:
        from utils import logger, clean_entity_text
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module2_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")
        clean_entity_text = getattr(_mod, "clean_entity_text")



class EntityExtractor:
    """Extracts named entities, topics, and keywords from input text using spaCy.

    Attributes:
        spacy_model (str): Name of the spaCy language model.
        nlp (Any): spaCy Language instance.
    """

    def __init__(self, spacy_model: str = Module2Config.SPACY_MODEL) -> None:
        """Initialize EntityExtractor with specified spaCy model.

        Args:
            spacy_model (str): spaCy pipeline model name (e.g., en_core_web_sm).
        """
        self.spacy_model = spacy_model
        self.nlp = None
        self._load_nlp()

    def _load_nlp(self) -> None:
        """Load spaCy model pipeline with graceful error handling."""
        try:
            import spacy
            logger.info(f"Loading spaCy model: {self.spacy_model}")
            self.nlp = spacy.load(self.spacy_model)
            logger.info("spaCy NLP model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load spaCy model '{self.spacy_model}' ({e}). Using regex entity extraction fallback.")
            self.nlp = None

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from input text chunk.

        Args:
            text (str): Input text string.

        Returns:
            List[Dict[str, Any]]: List of entity dicts containing text, label, start, end.
        """
        if not text or not text.strip():
            return []

        try:
            if self.nlp is not None:
                doc = self.nlp(text)
                entities = []
                seen = set()

                for ent in doc.ents:
                    cleaned_name = clean_entity_text(ent.text)
                    if len(cleaned_name) < 2 or cleaned_name.lower() in ("the", "this", "that", "a", "an"):
                        continue

                    key = (cleaned_name, ent.label_)
                    if key not in seen:
                        seen.add(key)
                        entities.append({
                            "name": cleaned_name,
                            "label": ent.label_,
                            "start_char": ent.start_char,
                            "end_char": ent.end_char
                        })
                return entities
            else:
                return self._fallback_extract_entities(text)
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            raise EntityExtractionError(f"Entity extraction error: {e}") from e

    def extract_keywords(self, text: str, max_keywords: int = 8) -> List[str]:
        """Extract key technical terms and nouns from text.

        Args:
            text (str): Input text.
            max_keywords (int): Maximum number of keywords to return.

        Returns:
            List[str]: List of unique keyword strings.
        """
        if not text:
            return []

        stop_words = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of", "from"}

        if self.nlp is not None:
            doc = self.nlp(text)
            keywords = set()
            for token in doc:
                if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and len(token.text) > 3:
                    keywords.add(clean_entity_text(token.text))
            return list(keywords)[:max_keywords]

        words = re.findall(r"\b[A-Za-z]{4,}\b", text)
        filtered = [clean_entity_text(w) for w in words if w.lower() not in stop_words]
        return list(dict.fromkeys(filtered))[:max_keywords]

    def extract_topics(self, text: str) -> List[str]:
        """Categorize text chunk into domain topics.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of detected topic names.
        """
        text_lower = text.lower()
        topics = []

        domain_keywords = {
            "Knowledge Graphs": ["graph", "neo4j", "node", "edge", "entity", "relationship", "triplet"],
            "Vector Search": ["vector", "embedding", "chromadb", "similarity", "cosine", "dense"],
            "LLM Systems": ["llm", "llama", "ollama", "prompt", "chat", "generation", "retrieval"],
            "Trust Evaluation": ["trust", "confidence", "provenance", "consistency", "reliability", "citation"],
            "Document Processing": ["pdf", "ingestion", "chunk", "text", "cleaner", "loader"]
        }

        for topic, kws in domain_keywords.items():
            if any(kw in text_lower for kw in kws):
                topics.append(topic)

        return topics if topics else ["General Knowledge"]

    def _fallback_extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Perform fallback capitalization-based entity extraction.

        Args:
            text (str): Input text string.

        Returns:
            List[Dict[str, Any]]: Extracted fallback entities.
        """
        # Find capitalized words (proper nouns)
        matches = re.finditer(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b", text)
        entities = []
        seen = set()

        for m in matches:
            ent_str = clean_entity_text(m.group(0))
            if ent_str not in seen and len(ent_str) > 2:
                seen.add(ent_str)
                entities.append({
                    "name": ent_str,
                    "label": "CONCEPT",
                    "start_char": m.start(),
                    "end_char": m.end()
                })
        return entities[:10]


if __name__ == "__main__":
    extractor = EntityExtractor()
    sample = "GraphRAG was developed by DeepMind engineers in London to optimize Neo4j and Llama 3."
    ents = extractor.extract_entities(sample)
    kws = extractor.extract_keywords(sample)
    topics = extractor.extract_topics(sample)
    print("Entities:", ents)
    print("Keywords:", kws)
    print("Topics:", topics)
