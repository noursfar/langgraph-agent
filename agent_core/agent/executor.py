# agent_core/agent/executor.py
from agent_core.agent.base_agent import create_agent
from agent_core.utils.logger import log


def run_agent(user_input: str):
    """Run the agent safely and return a structured result."""
    try:
        agent = create_agent()
        log.info("Running agent with user input: %s", user_input)
        result = agent.invoke({"input": user_input})
        log.info("Agent response: %s", result)
        return {"response": result['output']}
    except Exception as e:
        log.exception("Agent execution failed: %s", e)
        return {"error": str(e)}
