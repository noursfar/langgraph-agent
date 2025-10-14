# agent_core/agent/base_agent.py
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from agent_core.tools.get_pds_contact import get_pds_contact
from agent_core.config.settings import settings
from agent_core.utils.logger import log
from agent_core.utils.exceptions import AgentToolError


def create_agent():
    """
    Initialize the LangChain agent with registered tools.

    Returns:
        agent (BaseSingleActionAgent or BaseMultiActionAgent):
            Configured LangChain agent ready to run.
    """
    try:
        log.info("Initializing agent with model: %s", settings.model_name)

        # Initialize OpenAI LLM with API key and configuration
        llm = ChatOpenAI(
            model=settings.model_name,
            temperature=0,
            api_key=settings.openai_api_key,
        )

        # Register tools
        tools = [get_pds_contact]

        # Initialize LangChain agent with function-calling capabilities
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            handle_parsing_errors=True,
        )

        log.info("Agent initialized successfully with %d tool(s).", len(tools))
        return agent

    except Exception as e:
        log.exception("Failed to initialize agent: %s", e)
        raise AgentToolError(f"Agent initialization failed: {str(e)}") from e
