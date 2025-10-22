# agent_core/prompts/context_prompt.py

def build_context_prompt(pds_name = None, facility_name = None):
    context = []
    if pds_name:
        context.append(f"The current user is {pds_name}, a healthcare professional.")
    if facility_name:
        context.append(f"Facility: {facility_name}")
    return "\n".join(context)