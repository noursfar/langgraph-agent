# agent_core/rag/config.py
from pathlib import Path

# PATHS
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)


CHUNK_SIZE = 800  # Characters per chunk (roughly 200 tokens)
CHUNK_OVERLAP = 200  # Overlap between chunks to preserve context
