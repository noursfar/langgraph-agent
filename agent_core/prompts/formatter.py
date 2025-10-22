# agent_core/prompts/formatter.py
import logging
from langchain_core.messages import SystemMessage

from agent_core.prompts.system_prompt import SYSTEM_PROMPT
from agent_core.prompts.context_prompt import build_context_prompt
from agent_core.utils.exceptions import AgentToolError  # new custom exception

logger = logging.getLogger(__name__)

def compose_prompt(messages, pds_id):
    try:
        system_context = build_context_prompt(pds_id)
    except AgentToolError as e:
        # Log detailed error information
        logger.error(f"Failed to build system context prompt: {e}")
        # Gracefully degrade by providing fallback context
        system_context = ""

    # Construct the combined system message
    system_message = SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{system_context}")
    logger.debug("System message successfully composed.")

    return [system_message] + messages
