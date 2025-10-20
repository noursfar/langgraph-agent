# agent_core/agent/executor.py
from langchain_core.messages import HumanMessage
from agent_core.agent.base_agent import create_agent
from agent_core.utils.logger import log


def run_agent(user_input, conversation_history):
    try:
        agent = create_agent()
        log.info("Running LangGraph agent with user input: %s", user_input)

        # Build messages list - ensure it's never empty
        if conversation_history:
            messages = list(conversation_history)
        else:
            messages = []

        # Always add the current user message
        messages.append(HumanMessage(content=user_input))

        # Invoke the agent
        result = agent.invoke({"messages": messages})

        # Extract the final response
        final_message = result["messages"][-1]
        output = final_message.content

        log.info("Agent response: ...")

        return {
            "response": output,
            "messages": result["messages"]  # Full conversation for memory
        }

    except Exception as e:
        log.exception("Agent execution failed: %s", e)
        return {"error": str(e)}


def run_agent_streaming(user_input, conversation_history):
    """Streaming shows the AI's response token-by-token as it generates (like ChatGPT's typing effect)."""
    try:
        agent = create_agent()
        log.info("Running LangGraph agent (streaming) with user input: %s", user_input)

        # Build messages list
        messages = conversation_history if conversation_history else []
        messages.append(HumanMessage(content=user_input))

        # Stream the agent's response
        for chunk in agent.stream({"messages": messages}):
            yield chunk

    except Exception as e:
        log.exception("Agent streaming failed: %s", e)
        yield {"error": str(e)}