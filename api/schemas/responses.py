# api/schemas/responses.py
from pydantic import BaseModel, Field
from typing import Optional


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