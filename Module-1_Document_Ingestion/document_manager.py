"""
Module 1 : Document Ingestion
File : document_manager.py
Purpose : Complete document processing pipeline.
"""

try:
    from .pdf_loader import PDFLoader
    from .text_cleaner import TextCleaner
    from .chunker import TextChunker
except (ImportError, ValueError):
    from pdf_loader import PDFLoader
    from text_cleaner import TextCleaner
    from chunker import TextChunker



class DocumentManager:

    def __init__(self):

        self.loader = PDFLoader("data/pdfs")
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()

    def process_documents(self):

        documents = self.loader.load_pdfs()

        processed_documents = []

        for document in documents:

            cleaned_text = self.cleaner.clean(document["text"])

            chunks = self.chunker.split_text(cleaned_text)

            processed_documents.append(
                {
                    "filename": document["filename"],
                    "chunks": chunks
                }
            )

        return processed_documents


if __name__ == "__main__":

    manager = DocumentManager()

    documents = manager.process_documents()

    print("\n" + "=" * 60)
    print("DOCUMENT PROCESSING SUMMARY")
    print("=" * 60)

    for document in documents:

        print(f"\nFile : {document['filename']}")
        print(f"Chunks : {len(document['chunks'])}")