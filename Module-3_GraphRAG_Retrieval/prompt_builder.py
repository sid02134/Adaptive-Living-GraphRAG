"""
Module 3: GraphRAG Retrieval
File: prompt_builder.py
Purpose: Construct system and user prompts for Llama 3 answer synthesis.
"""

from typing import Dict, Any
from pathlib import Path
try:
    from .utils import logger
except (ImportError, ValueError):
    try:
        from utils import logger
    except (ImportError, AttributeError):
        import importlib.util
        _ut_path = Path(__file__).resolve().parent / "utils.py"
        _spec = importlib.util.spec_from_file_location("module3_utils", _ut_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        logger = getattr(_mod, "logger")



class PromptBuilder:
    """Builds structured system and user prompts for Llama 3 generation."""

    def __init__(self, system_instruction: str = "") -> None:
        """Initialize PromptBuilder with system instructions.

        Args:
            system_instruction (str): Default system directive.
        """
        self.system_instruction = system_instruction or (
            "You are an expert AI Assistant powering the Adaptive Living GraphRAG framework. "
            "Your task is to answer the user's question using ONLY the provided document context and knowledge graph triplets. "
            "Always maintain factual accuracy, cite your sources inline using [Source: filename], "
            "and state your confidence level clearly."
        )

    def build_prompt(self, query: str, context: str) -> Dict[str, str]:
        """Assemble structured system prompt and user prompt pair.

        Args:
            query (str): User query string.
            context (str): Formatted context block from ContextBuilder.

        Returns:
            Dict[str, str]: Dict containing 'system_prompt', 'user_prompt', and 'full_prompt'.
        """
        user_prompt = f"""CONTEXT INFORMATION:
=========================================
{context}
=========================================

USER QUESTION:
{query}

INSTRUCTIONS:
1. Synthesize a concise, accurate answer based strictly on the provided Context Information and Knowledge Graph Triplets.
2. Include inline citations for key claims in the format [Source: filename].
3. If the context does not contain enough information to answer the question, clearly state: "Insufficient information in retrieved domain documents."
4. Provide a structured response with key takeaways.
"""
        full_prompt = f"<|system|>\n{self.system_instruction}\n<|user|>\n{user_prompt}\n<|assistant|>\n"

        logger.info(f"Built Llama 3 prompt for query '{query}' (Prompt length: {len(full_prompt)} chars).")
        return {
            "system_prompt": self.system_instruction,
            "user_prompt": user_prompt,
            "full_prompt": full_prompt
        }


if __name__ == "__main__":
    pb = PromptBuilder()
    prompt = pb.build_prompt("What is Neo4j?", "Source [1]: doc.pdf\nNeo4j is a graph database.")
    print("Full Prompt Preview:\n", prompt["full_prompt"][:300])
