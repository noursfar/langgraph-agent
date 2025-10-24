# api/schemas/requests.py
from pydantic import BaseModel, Field


class InitializeRequest(BaseModel):
    """Request schema for initializing a new conversation session."""
    userId: str = Field(..., description="Unique identifier for the user")
    token: str = Field(..., description="Authentication token")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }