# agent_core/utils/exceptions.py
"""Custom exceptions for llm agent lab project"""


class LlmAgentError(Exception):
    """Base exception for NearCare MCP errors"""
    pass


class AgentToolError(LlmAgentError):
    """Custom exception raised when a LangChain tool fails."""
    pass


class AuthenticationError(LlmAgentError):
    """Custom exception raised when a token generation fails."""
    pass


class IngestionError(LlmAgentError):
    pass


class VectorStoreError(LlmAgentError):
    pass


class ContextBuildError(LlmAgentError):
    """Raised when building the context prompt fails."""
    pass