# agent_core/agent/executor.py
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from agent_core.config.settings import settings
from agent_core.utils.logger import log


def run_agent(agent, user_input, session_id):
    """
    Run the agent with persistent conversation history.

    Args:
        agent: Pre-initialized LangGraph agent instance
        user_input: The user's query
        session_id: Unique identifier for this conversation session
    """
    try:
        log.info("Running LangGraph agent with user input: %s", user_input)

        # Initialize persistent chat history
        chat_history = SQLChatMessageHistory(
            session_id=session_id,
            connection=settings.local_db_url,
            table_name="history"
        )

        # Get existing messages from database
        messages = chat_history.messages.copy()

        # Add current user message
        messages.append(HumanMessage(content=user_input))

        # Invoke the agent
        result = agent.invoke({"messages": messages})

        # Save all messages back to database
        # Clear first to avoid duplicates, then add all
        chat_history.clear()
        for message in result["messages"]:
            chat_history.add_message(message)

        # Extract the final response
        final_message = result["messages"][-1]
        output = final_message.content

        log.info("Agent response saved to session: %s", session_id)

        return {
            "response": output,
            "session_id": session_id
        }

    except Exception as e:
        log.exception("Agent execution failed: %s", e)
        return {"error": str(e)}


def run_agent_streaming(agent, user_input, session_id):
    """Streaming version with persistent history."""
    try:
        log.info("Running LangGraph agent (streaming) with user input: %s", user_input)

        # Initialize persistent chat history
        chat_history = SQLChatMessageHistory(
            session_id=session_id,
            connection=settings.local_db_url,
            table_name="history"
        )

        # Get existing messages
        messages = chat_history.messages.copy()
        messages.append(HumanMessage(content=user_input))

        # Stream the agent's response
        all_messages = []
        for chunk in agent.stream({"messages": messages}):
            all_messages = chunk.get("messages", all_messages)
            yield chunk

        # After streaming completes, save to database
        if all_messages:
            chat_history.clear()
            for message in all_messages:
                chat_history.add_message(message)

    except Exception as e:
        log.exception("Agent streaming failed: %s", e)
        yield {"error": str(e)}