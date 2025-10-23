# agent_core/agent/base_agent.py
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from agent_core.prompts.formatter import compose_prompt
from agent_core.tools.get_pds_contact import get_pds_contact_tool
from agent_core.tools.get_patient_data import get_patient_data_tool
from agent_core.tools.rag_query import retrieve_admin_info_tool
from agent_core.config.settings import settings
from agent_core.utils.logger import log
from agent_core.utils.exceptions import AgentToolError


class AgentState(TypedDict):
    """State schema for the agent graph."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


def create_agent():
    """
    Initialize the LangGraph agent with registered tools.

    Returns:
        Compiled LangGraph agent ready to run.
    """
    try:
        log.info("Initializing LangGraph agent with model: %s", settings.model_name)

        # Initialize OpenAI LLM with tool binding
        llm = ChatOpenAI(
            model=settings.model_name,
            temperature=0,
            api_key=settings.openai_api_key,
        )

        # Register tools
        tools = [get_pds_contact_tool, get_patient_data_tool, retrieve_admin_info_tool]

        # Bind tools to the LLM
        llm_with_tools = llm.bind_tools(tools)

        # Create tool node for executing tools
        tool_node = ToolNode(tools)

        # Define the function that determines whether to continue or end
        def should_continue(state: AgentState):
            """Determine if we should continue to tools or end."""
            messages = state["messages"]
            last_message = messages[-1]

            # If there are no tool calls, we finish
            if not last_message.tool_calls:
                return "end"
            # Otherwise continue with tools
            return "continue"

        # Define the function that calls the model
        def call_model(state: AgentState):
            """Call the LLM with the current state + composed prompt."""
            messages = compose_prompt(state["messages"], 269)
            response = llm_with_tools.invoke(messages)
            # Return the response which will be added to messages
            return {"messages": [response]}

        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)

        # Set the entrypoint as `agent`
        workflow.set_entry_point("agent")

        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )

        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")

        # Compile the graph
        agent = workflow.compile()

        log.info("LangGraph agent initialized successfully with %d tool(s).", len(tools))
        return agent

    except Exception as e:
        log.exception("Failed to initialize LangGraph agent: %s", e)
        raise AgentToolError(f"Agent initialization failed: {str(e)}") from e