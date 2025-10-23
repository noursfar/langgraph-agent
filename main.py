# main.py
import uuid
from agent_core.agent.executor import run_agent

if __name__ == "__main__":
    print("🧠 LLM Agent Lab - LangGraph Agent Starting...\n")

    # Generate a unique session ID for this conversation
    # Each time you run the script, it creates a new conversation
    session_id = str(uuid.uuid4())
    print(f"📝 Session ID: {session_id}")
    print("   (Use this ID to resume this conversation later)\n")

    while True:
        user_query = input("\nEnter your query (or 'quit' to exit): ")

        if user_query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            print(f"💾 Your conversation is saved under session: {session_id}")
            break

        result = run_agent(user_query, session_id)

        if "error" in result:
            print("\n❌ Error:", result["error"])
        else:
            print("\n🤖 Agent Output:")
            print(result["response"])
