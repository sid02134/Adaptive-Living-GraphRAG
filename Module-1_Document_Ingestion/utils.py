"""
Module 1
Utility Functions
"""

from datetime import datetime


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_success(message):
    print(f"[SUCCESS] {message}")


def print_info(message):
    print(f"[INFO] {message}")


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


if __name__ == "__main__":

    print_header("GraphRAG")

    print_success("Module 1 Completed")

    print_info(current_time())