"""
Adaptive Living GraphRAG Framework
Root Server Runner & Application Entrypoint
"""

import sys
import uvicorn
from pathlib import Path

# Add root workspace directory to python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main():
    print("=" * 60)
    print("Adaptive Living GraphRAG")
    print("Trust-Aware Dynamic Knowledge Evolution Framework")
    print("Starting FastAPI Backend Server on http://127.0.0.1:8000 ...")
    print("=" * 60)

    uvicorn.run("Module-5_Backend_API.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()