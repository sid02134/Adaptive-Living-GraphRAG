"""
Module 1 : Document Ingestion
File : pdf_loader.py
Purpose : Read PDF files and extract text.
"""

from pathlib import Path
from pypdf import PdfReader


class PDFLoader:

    def __init__(self, pdf_folder):
        self.pdf_folder = Path(pdf_folder)

    def load_pdfs(self):
        documents = []

        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        if not pdf_files:
            print("No PDF files found.")
            return documents

        print(f"Found {len(pdf_files)} PDF(s).\n")

        for pdf in pdf_files:

            print(f"Reading : {pdf.name}")

            reader = PdfReader(pdf)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            documents.append(
                {
                    "filename": pdf.name,
                    "text": text
                }
            )

            print(f"Finished : {pdf.name}")
            print("-" * 50)

        return documents


if __name__ == "__main__":

    loader = PDFLoader("data/pdfs")

    docs = loader.load_pdfs()

    print("\nSummary")
    print("=" * 40)

    for doc in docs:

        print(doc["filename"])
        print(f"Characters : {len(doc['text'])}")