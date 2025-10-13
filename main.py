# llm_agent_lab/main.py
from agent_core.agent.executor import run_agent

if __name__ == "__main__":
    print("🧠 LLM Agent Lab - Starting Agent...\n")

    user_query = input("Enter your query: ")
    result = run_agent(user_query)

    print("\n--- Agent Output ---")
    print(result["response"] if "response" in result else result["error"])
