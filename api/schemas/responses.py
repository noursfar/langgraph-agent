# api/schemas/responses.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class InitializeResponse(BaseModel):
    """Response schema for session initialization."""
    success: bool = Field(..., description="Whether the operation succeeded")
    session_id: Optional[str] = Field(None, description="Generated session ID")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "error": None
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat messages."""
    success: bool = Field(..., description="Whether the operation succeeded")
    response: Optional[str] = Field(None, description="Agent's response message")
    session_id: Optional[str] = Field(None, description="Session ID")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "Selon le livret d'accueil patient, les protocoles d'admission incluent...",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "error": None
            }
        }


class HistoryResponse(BaseModel):
    """Response schema for conversation history."""
    success: bool = Field(..., description="Whether the operation succeeded")
    session_id: Optional[str] = Field(None, description="Session ID")
    messages: Optional[List[Dict[str, Any]]] = Field(None, description="List of conversation messages")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {"type": "human", "content": "Bonjour"},
                    {"type": "ai", "content": "Bonjour! Comment puis-je vous aider?"}
                ],
                "error": None
            }
        }
