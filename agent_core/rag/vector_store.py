# agent_core/rag/vector_store.py
import chromadb
from chromadb.config import Settings
from agent_core.rag.config import CHROMA_PERSIST_DIR
from agent_core.utils.logger import log
from agent_core.utils.exceptions import AgentToolError


class VectorStore:
    """ChromaDB vector store for document embeddings."""

    def __init__(self, collection_name):
        """Initialize ChromaDB client and collection."""
        try:
            self.client = chromadb.PersistentClient(
                path=str(CHROMA_PERSIST_DIR),
                settings=Settings(anonymized_telemetry=False, allow_reset=True)
            )

            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Medical documents"}
            )

            self.collection_name = collection_name
            log.info("VectorStore initialized: collection '%s'", collection_name)

        except Exception as e:
            log.exception("Failed to initialize VectorStore")
            raise AgentToolError(f"VectorStore init failed: {str(e)}") from e


    def add_documents(self, chunks, embeddings, file_path):
        if not chunks or not embeddings:
            raise ValueError("chunks and embeddings cannot be empty")

        if len(chunks) != len(embeddings):
            raise ValueError(f"Mismatch: {len(chunks)} chunks but {len(embeddings)} embeddings")

        try:
            from pathlib import Path
            source_filename = Path(file_path).name
        except Exception as e:
            raise AgentToolError(f"Failed to extract file name from {file_path}: {str(e)}") from e

        # Prepare data for ChromaDB
        texts = [chunk.page_content for chunk in chunks]
        metadatas = []
        ids = []

        for idx, chunk in enumerate(chunks):
            metadata = {}
            if hasattr(chunk, 'metadata') and chunk.metadata:
                metadata.update(chunk.metadata)

            metadata.update({
                "source": source_filename,
                "chunk_index": idx,
                "total_chunks": len(chunks),
            })
            metadatas.append(metadata)

            # Generate unique ID: filename + chunk index
            chunk_id = f"{source_filename}_{idx}"
            ids.append(chunk_id)

        try:
            # Add to ChromaDB collection
            self.collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
        except Exception as e:
            raise  AgentToolError(f"Failed to add documents: {str(e)}") from e

        log.info("Added %d chunks from '%s' to vector store", len(chunks), source_filename)


    def query(self, query_embedding, top_k = 5, where = None):
        """
        Query the vector store for similar documents.

        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to return
            where: Optional metadata filter (e.g., {"source": "protocol.pdf"})

        Returns:
            Dict with keys: 'documents', 'metadatas', 'distances', 'ids'
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where
            )

            # ChromaDB returns nested lists, flatten them
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else [],
                'ids': results['ids'][0] if results['ids'] else []
            }

        except Exception as e:
            log.exception("Query failed")
            raise AgentToolError(f"Query failed: {str(e)}") from e


    def delete_by_source(self, source):
        try:
            self.collection.delete(where={"source": source})
            log.info("Deleted all chunks from source: %s", source)
        except Exception as e:
            log.exception("Delete by source failed")
            raise AgentToolError(f"Delete failed: {str(e)}") from e


    def count(self):
        """Get total number of chunks in the collection."""
        return self.collection.count()


    def list_sources(self):
        """Get list of unique source files in the collection."""
        try:
            # Get all documents
            results = self.collection.get()
            if not results or not results.get('metadatas'):
                return []

            # Extract unique source
            sources = set()
            for metadata in results['metadatas']:
                if 'source' in metadata:
                    sources.add(metadata['source'])

            return sorted(list(sources))
        except Exception as e:
            log.exception("Failed to list sources: %s", e)
            return []


    def reset(self):
        """Delete all documents from the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Medical documents"}
            )
            log.warning("Collection '%s' reset - all documents deleted", self.collection_name)
        except Exception as e:
            log.exception("Reset failed")
            raise AgentToolError(f"Reset failed: {str(e)}") from e
