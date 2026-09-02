"""
Quick Root Integration Flow Test
PDF -> Module 1 -> Module 2 -> Module 3
"""

import sys
import importlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def run_quick_test():
    print("\n" + "=" * 60)
    print("QUICK GRAPH RAG INTEGRATION TEST")
    print("=" * 60)

    # 1. Package Imports from Root
    mod1 = importlib.import_module("Module-1_Document_Ingestion")
    mod2 = importlib.import_module("Module-2_Knowledge_Representation")
    mod3 = importlib.import_module("Module-3_GraphRAG_Retrieval")

    DocumentManager = mod1.DocumentManager
    GraphBuilder = mod2.GraphBuilder
    GraphRAGRetriever = mod3.GraphRAGRetriever

    print("[SUCCESS] Module 1, 2, 3 imported cleanly from root!")

    # 2. Module 1 Ingestion
    doc_mgr = DocumentManager()
    sample_doc = [{
        "filename": "quick_test_paper.pdf",
        "chunks": [
            "Adaptive Living GraphRAG is a trust-aware dynamic knowledge evolution framework.",
            "It combines vector search in ChromaDB with knowledge graphs in Neo4j and Llama 3 LLM synthesis."
        ]
    }]

    # 3. Module 2 Knowledge Graph & Vector Store
    gb = GraphBuilder()
    summary = gb.build_knowledge_graph(sample_doc)
    print("[SUCCESS] Module 2 GraphBuilder executed. Chunks added:", summary["total_chunks"])

    # 4. Module 3 GraphRAG Hybrid Retrieval
    retriever = GraphRAGRetriever()
    result = retriever.run_retrieval_pipeline("What is Adaptive Living GraphRAG?", top_k=2, alpha=0.6)
    print("[SUCCESS] Module 3 GraphRAGRetriever retrieved chunks:", len(result["retrieved_chunks"]))
    print("[SUCCESS] Context String:", result["context_string"][:100], "...")
    print("[SUCCESS] Full Prompt Generated Length:", len(result["prompt"]["full_prompt"]), "chars.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_quick_test()
