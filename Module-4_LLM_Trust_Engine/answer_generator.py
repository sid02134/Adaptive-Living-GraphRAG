"""
Module 4: LLM + Trust Engine
File: answer_generator.py
Purpose: Master orchestrator uniting LLM generation, Trust calculation, conflict resolution, and citation formatting.
"""

import time
import sys
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(str(Path(__file__).resolve().parent.parent / "Module-3_GraphRAG_Retrieval"))

try:
    from config import Module4Config
except (ImportError, AttributeError):
    import importlib.util
    _cfg_path = Path(__file__).resolve().parent / "config.py"
    _spec = importlib.util.spec_from_file_location("module4_config", _cfg_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    Module4Config = _mod.Module4Config
from ollama_client import OllamaClient
from trust_score import TrustEvaluator
from source_ranker import SourceRanker
from conflict_resolution import ConflictResolver
from citation_generator import CitationGenerator
from response_formatter import ResponseFormatter
try:
    from utils import llm_logger
except (ImportError, AttributeError):
    import importlib.util
    _ut_path = Path(__file__).resolve().parent / "utils.py"
    _spec = importlib.util.spec_from_file_location("mod4_utils", _ut_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    llm_logger = getattr(_mod, "llm_logger")


class AnswerGenerator:
    """Master class executing the end-to-end GraphRAG LLM + Trust Engine pipeline.

    Attributes:
        ollama_client (OllamaClient): Ollama client instance.
        trust_evaluator (TrustEvaluator): 4-tier trust score evaluator.
        source_ranker (SourceRanker): Source ranker instance.
        conflict_resolver (ConflictResolver): Cross-document conflict resolver.
        citation_generator (CitationGenerator): Citation generator instance.
        response_formatter (ResponseFormatter): Frontend response formatter instance.
        retriever_pipeline (Optional[Any]): GraphRAGRetriever instance from Module 3.
    """

    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        retriever_pipeline: Optional[Any] = None
    ) -> None:
        """Initialize AnswerGenerator pipeline components."""
        self.ollama_client = ollama_client or OllamaClient()
        self.trust_evaluator = TrustEvaluator()
        self.source_ranker = SourceRanker()
        self.conflict_resolver = ConflictResolver()
        self.citation_generator = CitationGenerator()
        self.response_formatter = ResponseFormatter()

        if retriever_pipeline is None:
            try:
                mod3_path = Path(__file__).resolve().parent.parent / "Module-3_GraphRAG_Retrieval"
                if str(mod3_path) not in sys.path:
                    sys.path.insert(0, str(mod3_path))
                import importlib
                ret_mod = importlib.import_module("retriever")
                GraphRAGRetriever = getattr(ret_mod, "GraphRAGRetriever")
                self.retriever_pipeline = GraphRAGRetriever()
            except Exception as e:
                llm_logger.warning(f"Could not initialize GraphRAGRetriever from Module 3: {e}")
                self.retriever_pipeline = None
        else:
            self.retriever_pipeline = retriever_pipeline

    def generate_answer(
        self,
        query: str,
        retrieval_result: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        alpha: float = 0.6
    ) -> Dict[str, Any]:
        """Execute end-to-end question answering pipeline with trust evaluation.

        Args:
            query (str): User question text.
            retrieval_result (Optional[Dict[str, Any]]): Optional pre-computed retrieval dict from Module 3.
            top_k (int): Top-k retrieval cutoff.
            alpha (float): Hybrid vector/graph weight.

        Returns:
            Dict[str, Any]: Complete formatted answer dictionary.
        """
        start_time = time.time()
        llm_logger.info(f"Generating answer for query: '{query}'")

        # 1. Obtain Retrieval Results (Run Module 3 if not provided)
        if retrieval_result is None:
            if self.retriever_pipeline is not None:
                retrieval_result = self.retriever_pipeline.run_retrieval_pipeline(query, top_k=top_k, alpha=alpha)
            else:
                retrieval_result = {
                    "query": query,
                    "retrieved_chunks": [],
                    "graph_context": {"nodes": [], "edges": []},
                    "context_string": "No context available.",
                    "prompt": {"full_prompt": query, "system_prompt": ""}
                }

        chunks = retrieval_result.get("retrieved_chunks", [])
        graph_context = retrieval_result.get("graph_context", {})
        prompt_data = retrieval_result.get("prompt", {})

        full_prompt = prompt_data.get("full_prompt", query)
        system_prompt = prompt_data.get("system_prompt", "")

        # 2. Rank Sources & Resolve Conflicts
        ranked_sources = self.source_ranker.rank_sources(chunks)
        conflict_info = self.conflict_resolver.resolve_conflicts(ranked_sources)
        citations = self.citation_generator.generate_citations(ranked_sources)

        # 3. Invoke LLM Answer Generation
        raw_answer = self.ollama_client.generate(full_prompt, system_prompt=system_prompt)

        # 4. Evaluate Trust Score (40% SemSim, 30% SourceRel, 20% GraphCons, 10% CitCov)
        trust_evaluation = self.trust_evaluator.evaluate_trust(
            retrieved_chunks=ranked_sources,
            graph_context=graph_context,
            generated_answer=raw_answer,
            citations=citations
        )

        processing_time_ms = (time.time() - start_time) * 1000.0

        # 5. Format Output Object
        final_output = self.response_formatter.format_frontend_response(
            query=query,
            answer=raw_answer,
            trust_evaluation=trust_evaluation,
            citations=citations,
            ranked_sources=ranked_sources,
            conflict_info=conflict_info,
            processing_time_ms=processing_time_ms
        )

        llm_logger.info(f"Answer generation completed in {processing_time_ms:.2f} ms with Trust Score {trust_evaluation['trust_percentage']}%.")
        return final_output


if __name__ == "__main__":
    generator = AnswerGenerator()
    result = generator.generate_answer("How does Adaptive Living GraphRAG evaluate trust score?")
    print("\nAnswerGenerator Final Output Preview:\n" + "=" * 50)
    print("Answer:", result["answer"][:200])
    print("Trust Score:", result["trust_percentage"], "%")
