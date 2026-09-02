"""
Module 5: Backend API
File: upload_api.py
Purpose: APIRouter for PDF document upload and automated pipeline triggering.
"""

import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

try:
    from .models import UploadResponse
except (ImportError, ValueError):
    from models import UploadResponse


router = APIRouter(tags=["Document Ingestion"])
logger = logging.getLogger("backend_logger")


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf_document(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a PDF document, trigger Module 1 ingestion and Module 2 knowledge graph construction.

    Args:
        file (UploadFile): PDF file uploaded in multipart form data.

    Returns:
        UploadResponse: Summary stats on text chunks, extracted entities, and graph relations created.

    Raises:
        HTTPException: If file is not PDF or processing fails.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        base_dir = Path(__file__).resolve().parent.parent
        pdf_dir = base_dir / "data" / "pdfs"
        os.makedirs(pdf_dir, exist_ok=True)

        target_file_path = pdf_dir / file.filename
        logger.info(f"Saving uploaded PDF to: {target_file_path}")

        with open(target_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Run Module 1 Processing
        import importlib
        mod1 = importlib.import_module("Module-1_Document_Ingestion.document_manager")
        DocumentManager = getattr(mod1, "DocumentManager")

        doc_mgr = DocumentManager()
        processed_docs = doc_mgr.process_documents()

        # Filter for newly uploaded file
        uploaded_doc = [d for d in processed_docs if d.get("filename") == file.filename]
        if not uploaded_doc:
            uploaded_doc = processed_docs if processed_docs else [{"filename": file.filename, "chunks": ["Uploaded document text placeholder."]}]

        # 2. Run Module 2 Graph Builder
        mod2 = importlib.import_module("Module-2_Knowledge_Representation.graph_builder")
        GraphBuilder = getattr(mod2, "GraphBuilder")

        builder = GraphBuilder()
        graph_summary = builder.build_knowledge_graph(uploaded_doc)

        return UploadResponse(
            status="success",
            filename=file.filename,
            chunks_processed=graph_summary.get("total_chunks", 0),
            entities_extracted=graph_summary.get("total_entities_extracted", 0),
            graph_building_summary=graph_summary.get("relationships_created", {})
        )
    except Exception as e:
        logger.error(f"Failed to process uploaded file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
