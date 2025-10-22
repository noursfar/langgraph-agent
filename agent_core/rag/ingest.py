# agent_core/rag/ingest.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from agent_core.rag.vector_store import VectorStore

from agent_core.config.settings import settings
from agent_core.rag.config import CHUNK_SIZE, CHUNK_OVERLAP
from agent_core.utils.exceptions import IngestionError


def ingest_document(file_path, collection_name="medical_documents"):
    try:
        # Initialize vector store
        vector_store = VectorStore(collection_name)

        # Check if file_path already exists in the collection
        existing_sources = vector_store.list_sources()
        if file_path in existing_sources:
            raise IngestionError(f"File {file_path} already ingested in collection {collection_name}")

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
            model=settings.embedding_model,
            api_key=settings.openai_api_key
        )
        texts = [chunk.page_content for chunk in chunks]
        embeddings = embeddings_model.embed_documents(texts)

        # Store in vector DB
        vector_store.add_documents(chunks, embeddings, file_path)
    except Exception as e:
        raise IngestionError(f"Failed to ingest {file_path}: {str(e)}")