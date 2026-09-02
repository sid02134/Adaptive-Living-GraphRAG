"""
Module 1: Document Ingestion
File: test_module1.py
Purpose: Unit and integration tests for Module 1 components.
"""

import os
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import importlib

try:
    mod1_pl = importlib.import_module("Module-1_Document_Ingestion.pdf_loader")
    PDFLoader = getattr(mod1_pl, "PDFLoader")
    mod1_tc = importlib.import_module("Module-1_Document_Ingestion.text_cleaner")
    TextCleaner = getattr(mod1_tc, "TextCleaner")
    mod1_ck = importlib.import_module("Module-1_Document_Ingestion.chunker")
    TextChunker = getattr(mod1_ck, "TextChunker")
    mod1_dm = importlib.import_module("Module-1_Document_Ingestion.document_manager")
    DocumentManager = getattr(mod1_dm, "DocumentManager")
except Exception:
    from pdf_loader import PDFLoader
    from text_cleaner import TextCleaner
    from chunker import TextChunker
    from document_manager import DocumentManager




def test_text_cleaner():
    """Test TextCleaner formatting and whitespace normalization."""
    cleaner = TextCleaner()
    raw = "   GraphRAG\t\t\tis   an    advanced   framework.\n\n\n\nRetrieval   Augmented.   "
    cleaned = cleaner.clean(raw)
    assert "\t" not in cleaned
    assert "  " not in cleaned
    assert "GraphRAG is an advanced framework." in cleaned
    print("\n[PASSED] TextCleaner unit test")


def test_text_chunker():
    """Test TextChunker chunk splitting and overlaps."""
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    sample_text = "Adaptive Living GraphRAG integrates knowledge graph representations with dense vector embeddings to evaluate trust scores across complex documents."
    chunks = chunker.split_text(sample_text)
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    assert all(isinstance(c, str) for c in chunks)
    print("[PASSED] TextChunker unit test")


def test_pdf_loader_empty():
    """Test PDFLoader on empty folder."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        loader = PDFLoader(tmp_dir)
        docs = loader.load_pdfs()
        assert docs == []
    print("[PASSED] PDFLoader empty folder test")


def test_document_manager_pipeline():
    """Test DocumentManager processing pipeline."""
    manager = DocumentManager()
    processed = manager.process_documents()
    assert isinstance(processed, list)
    print("[PASSED] DocumentManager pipeline integration test")


if __name__ == "__main__":
    print("\nRunning Module 1 Unit & Integration Tests...\n" + "=" * 50)
    test_text_cleaner()
    test_text_chunker()
    test_pdf_loader_empty()
    test_document_manager_pipeline()
    print("=" * 50 + "\nAll Module 1 Tests Passed Successfully!\n")
