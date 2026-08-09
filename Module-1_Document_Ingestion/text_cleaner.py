"""
Module 1 : Document Ingestion
File : text_cleaner.py
Purpose : Clean extracted PDF text.
"""

import re


class TextCleaner:

    def clean(self, text):

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Replace multiple spaces with single space
        text = re.sub(r" +", " ", text)

        # Replace multiple blank lines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # Remove leading and trailing spaces
        text = text.strip()

        return text


if __name__ == "__main__":

    sample = """

        GraphRAG        is an advanced

        Retrieval      Augmented
        Generation system.

    """

    cleaner = TextCleaner()

    cleaned = cleaner.clean(sample)

    print("Original Text")
    print("----------------------")
    print(sample)

    print("\nCleaned Text")
    print("----------------------")
    print(cleaned)