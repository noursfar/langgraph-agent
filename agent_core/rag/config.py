# agent_core/rag/config.py
"""RAG-specific configuration and constants."""
from pathlib import Path

# ============================================================================
# PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# EMBEDDING CONFIGURATION
# ============================================================================
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model
EMBEDDING_DIMENSION = 1536  # Ada-002 produces 1536-dimensional vectors
BATCH_SIZE = 100  # Number of texts to embed in one API call

# ============================================================================
# CHUNKING CONFIGURATION
# ============================================================================
CHUNK_SIZE = 800  # Characters per chunk (roughly 200 tokens)
CHUNK_OVERLAP = 200  # Overlap between chunks to preserve context
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Hierarchical splitting

# ============================================================================
# RETRIEVAL CONFIGURATION
# ============================================================================
DEFAULT_TOP_K = 5  # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score (0-1)
MAX_CONTEXT_LENGTH = 3000  # Max characters to return to LLM

# ============================================================================
# CHROMADB CONFIGURATION
# ============================================================================
COLLECTION_NAME = "medical_documents"  # Default collection name

# Metadata fields to store with each chunk
METADATA_FIELDS = [
    "source",  # Original document filename
    "chunk_index",  # Position in document
    "total_chunks",  # Total chunks from this document
    "document_type",  # pdf, docx, txt
    "created_at",  # Timestamp
    "file_size",  # Original file size in bytes
]

# ============================================================================
# SUPPORTED FILE TYPES
# ============================================================================
SUPPORTED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}

# ============================================================================
# RAG PROMPTS
# ============================================================================
CONTEXT_PROMPT_TEMPLATE = """Utilise les informations suivantes pour répondre à la question.
Si tu ne trouves pas la réponse dans le contexte, dis-le clairement.

Contexte:
{context}

Question: {question}

Réponse:"""