# llm_agent_lab/main.py
from agent_core.agent.executor import run_agent

if __name__ == "__main__":
    print("🧠 LLM Agent Lab - LangGraph Agent Starting...\n")

    # Optional: Track conversation history for multi-turn conversations
    conversation_history = None  # Changed from [] to None

    while True:
        user_query = input("\nEnter your query (or 'quit' to exit): ")

        if user_query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        result = run_agent(user_query, conversation_history)

        if "error" in result:
            print("\n Error:", result["error"])
        else:
            print("\n Agent Output:")
            print(result["response"])

            # Update conversation history for context in next query
            conversation_history = result.get("messages", None)
