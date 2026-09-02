"""
Module 4: LLM + Trust Engine Package
"""

import importlib

try:
    from .ollama_client import OllamaClient
    from .trust_score import TrustEvaluator
    from .source_ranker import SourceRanker
    from .conflict_resolution import ConflictResolver
    from .citation_generator import CitationGenerator
    from .response_formatter import ResponseFormatter
    from .answer_generator import AnswerGenerator
except (ImportError, ValueError):
    try:
        mod_oc = importlib.import_module("Module-4_LLM_Trust_Engine.ollama_client")
        OllamaClient = getattr(mod_oc, "OllamaClient")
        mod_te = importlib.import_module("Module-4_LLM_Trust_Engine.trust_score")
        TrustEvaluator = getattr(mod_te, "TrustEvaluator")
        mod_sr = importlib.import_module("Module-4_LLM_Trust_Engine.source_ranker")
        SourceRanker = getattr(mod_sr, "SourceRanker")
        mod_cr = importlib.import_module("Module-4_LLM_Trust_Engine.conflict_resolution")
        ConflictResolver = getattr(mod_cr, "ConflictResolver")
        mod_cg = importlib.import_module("Module-4_LLM_Trust_Engine.citation_generator")
        CitationGenerator = getattr(mod_cg, "CitationGenerator")
        mod_rf = importlib.import_module("Module-4_LLM_Trust_Engine.response_formatter")
        ResponseFormatter = getattr(mod_rf, "ResponseFormatter")
        mod_ag = importlib.import_module("Module-4_LLM_Trust_Engine.answer_generator")
        AnswerGenerator = getattr(mod_ag, "AnswerGenerator")
    except Exception:
        from ollama_client import OllamaClient
        from trust_score import TrustEvaluator
        from source_ranker import SourceRanker
        from conflict_resolution import ConflictResolver
        from citation_generator import CitationGenerator
        from response_formatter import ResponseFormatter
        from answer_generator import AnswerGenerator

__all__ = [
    "OllamaClient",
    "TrustEvaluator",
    "SourceRanker",
    "ConflictResolver",
    "CitationGenerator",
    "ResponseFormatter",
    "AnswerGenerator"
]
