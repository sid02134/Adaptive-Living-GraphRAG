"""
Module 1: Document Ingestion Package
"""

import importlib

try:
    from .pdf_loader import PDFLoader
    from .text_cleaner import TextCleaner
    from .chunker import TextChunker
    from .document_manager import DocumentManager
except (ImportError, ValueError):
    try:
        mod_pl = importlib.import_module("Module-1_Document_Ingestion.pdf_loader")
        PDFLoader = getattr(mod_pl, "PDFLoader")
        mod_tc = importlib.import_module("Module-1_Document_Ingestion.text_cleaner")
        TextCleaner = getattr(mod_tc, "TextCleaner")
        mod_ck = importlib.import_module("Module-1_Document_Ingestion.chunker")
        TextChunker = getattr(mod_ck, "TextChunker")
        mod_dm = importlib.import_module("Module-1_Document_Ingestion.document_manager")
        DocumentManager = getattr(mod_dm, "DocumentManager")
    except Exception:
        from pdf_loader import PDFLoader
        from text_cleaner import TextCleaner
        from chunker import TextChunker
        from document_manager import DocumentManager

__all__ = [
    "PDFLoader",
    "TextCleaner",
    "TextChunker",
    "DocumentManager"
]
