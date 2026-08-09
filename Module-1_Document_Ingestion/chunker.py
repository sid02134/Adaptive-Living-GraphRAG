"""
Module 1 : Document Ingestion
File : chunker.py
Purpose : Split cleaned text into chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(self, chunk_size=500, chunk_overlap=100):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_text(self, text):

        return self.splitter.split_text(text)


if __name__ == "__main__":

    sample = """
    GraphRAG is an advanced Retrieval-Augmented Generation framework.

    It combines Knowledge Graphs,
    Vector Databases,
    Large Language Models,
    and Intelligent Retrieval.
    """ * 50

    chunker = TextChunker()

    chunks = chunker.split_text(sample)

    print("=" * 50)
    print("Total Chunks :", len(chunks))
    print("=" * 50)

    for i, chunk in enumerate(chunks):

        print(f"\nChunk {i+1}")
        print("-" * 40)
        print(chunk[:200])