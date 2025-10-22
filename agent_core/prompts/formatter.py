# agent_core/prompts/formatter.py
from langchain_core.messages import SystemMessage

from agent_core.prompts.system_prompt import SYSTEM_PROMPT
from agent_core.prompts.context_prompt import build_context_prompt
from agent_core.utils.exceptions import ContextBuildError
from agent_core.utils.logger import log

def compose_prompt(messages, pds_id):
    try:
        system_context = build_context_prompt(pds_id)
    except ContextBuildError as e:
        log.error(f"Failed to build system context prompt: {e}")
        system_context = ""

    # Construct the combined system message
    system_message = SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{system_context}")
    log.debug("System message successfully composed.")

    return [system_message] + messages
