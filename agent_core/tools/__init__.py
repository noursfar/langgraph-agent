# agent_core/tools/__init__.py

import json
from agent_core.utils.exceptions import AgentToolError


def parse_and_validate_name_input(input_data):
    try:
        data = json.loads(input_data)
    except json.JSONDecodeError as e:
        raise AgentToolError(f"Invalid JSON format: {e}")

    firstname = data.get("firstname")
    lastname = data.get("lastname")

    if not firstname or not lastname:
        raise AgentToolError("Missing 'firstname' or 'lastname' in input_data")

    return firstname, lastname
