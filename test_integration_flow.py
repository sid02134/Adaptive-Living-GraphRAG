"""
Adaptive Living GraphRAG Framework
Root-Level End-to-End Integration Flow Test
Flow: PDF -> Module 1 -> Module 2 -> Module 3
"""

import sys
import importlib
from pathlib import Path

# Insert root directory into sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def run_integration_pipeline():
    print("\n" + "=" * 60)
    print("GRAPH RAG END-TO-END INTEGRATION PIPELINE VERIFICATION")
    print("=" * 60)

    # 1. Import Modules directly from root package names
    print("\n[STEP 1] Verifying Root-Level Module Package Imports...")
    mod1 = importlib.import_module("Module-1_Document_Ingestion")
    mod2 = importlib.import_module("Module-2_Knowledge_Representation")
    mod3 = importlib.import_module("Module-3_GraphRAG_Retrieval")

    DocumentManager = mod1.DocumentManager
    GraphBuilder = mod2.GraphBuilder
    GraphRAGRetriever = mod3.GraphRAGRetriever

    print(" -> Module 1, Module 2, Module 3 packages imported cleanly from root!")

    # 2. Run Module 1 Ingestion
    print("\n[STEP 2] Running Module 1 Document Ingestion Pipeline...")
    doc_mgr = DocumentManager()
    processed_docs = doc_mgr.process_documents()
    print(f" -> Processed {len(processed_docs)} document(s) into text chunks.")
    for d in processed_docs:
        print(f"    - File: {d['filename']} ({len(d['chunks'])} chunk(s))")

    # If no PDFs were found, create sample mock document for pipeline test
    if not processed_docs:
        processed_docs = [{
            "filename": "sample_integration_doc.pdf",
            "chunks": [
                "Adaptive Living GraphRAG is a trust-aware dynamic knowledge evolution framework.",
                "It combines dense vector search in ChromaDB with knowledge graphs in Neo4j and Llama 3 LLM synthesis."
            ]
        }]

    # 3. Run Module 2 Knowledge Representation
    print("\n[STEP 3] Running Module 2 Vector Store & Knowledge Graph Construction...")
    graph_builder = GraphBuilder()
    graph_summary = graph_builder.build_knowledge_graph(processed_docs)
    print(f" -> Knowledge Graph Summary: {graph_summary['status']}")
    print(f"    - Total Chunks in ChromaDB: {graph_summary['total_chunks']}")
    print(f"    - Total Entities Extracted: {graph_summary['total_entities_extracted']}")
    print(f"    - Relationships Created: {graph_summary['relationships_created']}")

    # 4. Run Module 3 GraphRAG Hybrid Retrieval
    print("\n[STEP 4] Running Module 3 Master GraphRAG Retrieval Pipeline...")
    retriever = GraphRAGRetriever()
    query = "How does Adaptive Living GraphRAG combine vector search and knowledge graphs?"
    result = retriever.run_retrieval_pipeline(query=query, top_k=3, alpha=0.6)

    print(f" -> Query: '{result['query']}'")
    print(f" -> Retrieved {len(result['retrieved_chunks'])} chunk(s) via Hybrid Score Fusion (alpha=0.6).")
    print(f" -> Graph Subgraph Nodes: {len(result['graph_context']['nodes'])}, Edges: {len(result['graph_context']['edges'])}")
    print(f" -> Context String Length: {len(result['context_string'])} characters.")
    print(f" -> Llama 3 Prompt Generated Length: {len(result['prompt']['full_prompt'])} characters.")

    print("\n" + "=" * 60)
    print("END-TO-END INTEGRATION FLOW TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    run_integration_pipeline()
