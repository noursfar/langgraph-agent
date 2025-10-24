# api/schemas/requests.py
from pydantic import BaseModel, Field


class InitializeRequest(BaseModel):
    """Request schema for initializing a new conversation session."""
    userId: str = Field(..., description="Unique identifier for the user")
    token: str = Field(..., description="Authentication token")

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "user_123",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class ChatRequest(BaseModel):
    """Request schema for sending a message to the agent."""
    message: str = Field(..., description="User's message/query")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Quels sont les protocoles d'admission?"
            }
        }