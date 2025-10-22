# agent_core/prompts/formatter.py
from langchain_core.messages import SystemMessage

from agent_core.prompts.system_prompt import SYSTEM_PROMPT
from agent_core.prompts.context_prompt import build_context_prompt


def compose_prompt(messages, pds_name=None, facility_name=None):
    system_context = build_context_prompt(pds_name, facility_name)
    system_message = SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{system_context}")
    return [system_message] + messages
