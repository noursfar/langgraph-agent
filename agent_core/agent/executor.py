# agent_core/agent/executor.py
from langchain_core.messages import HumanMessage
from agent_core.agent.base_agent import create_agent
from agent_core.utils.logger import log
from db.model import Conversation

HR_ID = "1"      # Static for now
PDS_ID = "269"   # Static for now

def save_conversation(messages):
    """Save or update the conversation in the database."""
    try:
        # Try to fetch existing conversation for this HR/PDS
        conversation = Conversation.query.filter_by(hr_id=HR_ID, pds_id=PDS_ID).first()
        breakpoint()

        if conversation:
            # Update existing conversation
            conversation.full_history = messages
        else:
            # Create new conversation
            conversation = Conversation(hr_id=HR_ID, pds_id=PDS_ID, full_history=messages)

        # Persist to DB
        conversation.save()
        log.info("Conversation saved successfully (id=%s)", conversation.id)

    except Exception as e:
        log.exception("Failed to save conversation: %s", e)


def run_agent(user_input, conversation_history):
    try:
        agent = create_agent()
        log.info("Running LangGraph agent with user input: %s", user_input)

        messages = list(conversation_history) if conversation_history else []
        messages.append(HumanMessage(content=user_input))

        result = agent.invoke({"messages": messages})
        final_message = result["messages"][-1]
        output = final_message.content

        # Persist the updated conversation
        breakpoint()
        save_conversation(result["messages"])

        log.info("Agent response: ...")

        return {
            "response": output,
            "messages": result["messages"]  # Full conversation for memory
        }

    except Exception as e:
        log.exception("Agent execution failed: %s", e)
        return {"error": str(e)}
