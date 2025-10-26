# agent_core/prompts/formatter.py
from langchain_core.messages import SystemMessage
from agent_core.prompts.system_prompt import SYSTEM_PROMPT


def compose_prompt(messages, prebuilt_context):
    system_message = SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{prebuilt_context}")

    return [system_message] + messages
