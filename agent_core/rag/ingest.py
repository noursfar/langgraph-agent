# agent_core/rag/ingest.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from agent_core.rag.vector_store import VectorStore

from agent_core.config.settings import settings
from agent_core.rag.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL
from agent_core.utils.exceptions import IngestionError


def ingest_document(file_path):
    try:
        # Load document
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Chunk documents using tiktoken
        splitter = TokenTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            encoding_name="cl100k_base"  # tiktoken encoding for text-embedding-ada-002
        )
        chunks = splitter.split_documents(docs)

        # Generate embeddings using OpenAI
        embeddings_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=settings.openai_api_key
        )
        texts = [chunk.page_content for chunk in chunks]
        embeddings = embeddings_model.embed_documents(texts)

        # Store in vector DB
        vector_store = VectorStore()
        vector_store.add_documents(chunks, embeddings, file_path)
    except Exception as e:
        raise IngestionError(f"Failed to ingest {file_path}: {str(e)}")