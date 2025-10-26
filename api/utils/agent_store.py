# api/utils/agent_store.py
agent_store = {}

def get_agent(session_id):
    """Get agent by session ID."""
    return agent_store.get(session_id)

def set_agent(session_id, agent):
    """Store agent with session ID."""
    agent_store[session_id] = agent

def remove_agent(session_id):
    """Remove agent by session ID."""
    agent_store.pop(session_id, None)