# agent_core/tools/rag_query.py
from langchain_core.tools import StructuredTool
from langchain_openai import OpenAIEmbeddings
from agent_core.rag.vector_store import VectorStore
from agent_core.config.settings import settings
from agent_core.utils.logger import log
from agent_core.utils.exceptions import AgentToolError


def retrieve_admin_info(question, collection="medical_documents"):
    try:
        log.info("Running RAG query for question: %s", question)

        # Initialize embedding model
        embeddings_model = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key
        )

        # Compute embedding for user question
        query_embedding = embeddings_model.embed_query(question)

        # Initialize vector store and query top results
        vector_store = VectorStore(collection)
        results = vector_store.query(query_embedding, top_k=3)

        if not results["documents"]:
            log.warning("No relevant chunks found for question: %s", question)
            return {"answer": None, "context": "Aucun document pertinent trouvé."}

        # Merge retrieved chunks into context
        merged_context = "\n\n".join(results["documents"])

        log.info("RAG query retrieved %d relevant chunks.", len(results["documents"]))

        return {
            "answer": merged_context,
            "metadata": results["metadatas"]
        }

    except Exception as e:
        log.exception("RAG query failed for question: %s", question)
        raise AgentToolError(f"RAG query failed: {str(e)}") from e


retrieve_admin_info_tool = StructuredTool.from_function(
    func=retrieve_admin_info,
    name="retrieve_admin_info",
    description=(
        "Récupère les informations nécessaires à partir des documents officiels "
        "stockés dans la base vectorielle (RAG). Utilisé lorsque l'utilisateur pose une question administrative."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Question de l'utilisateur sur un sujet administratif ou documentaire."
            }
        },
        "required": ["question"]
    }
)
