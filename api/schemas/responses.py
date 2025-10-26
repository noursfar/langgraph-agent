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


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload."""
    success: bool = Field(..., description="Whether the operation succeeded")
    filename: Optional[str] = Field(None, description="Name of uploaded file")
    hr_id: Optional[str] = Field(None, description="Healthcare facility ID")
    chunks_count: Optional[int] = Field(None, description="Number of chunks created")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "pratiquesoins.pdf",
                "hr_id": "clinic_001",
                "chunks_count": 45,
                "error": None
            }
        }


class DocumentDeleteResponse(BaseModel):
    """Response schema for document deletion."""
    success: bool = Field(..., description="Whether the operation succeeded")
    filename: Optional[str] = Field(None, description="Name of deleted file")
    hr_id: Optional[str] = Field(None, description="Healthcare facility ID")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "pratiquesoins.pdf",
                "hr_id": "clinic_001",
                "error": None
            }
        }


class DocumentListResponse(BaseModel):
    """Response schema for listing documents."""
    success: bool = Field(..., description="Whether the operation succeeded")
    hr_id: Optional[str] = Field(None, description="Healthcare facility ID")
    documents: Optional[List[str]] = Field(None, description="List of document filenames")
    total_chunks: Optional[int] = Field(None, description="Total number of chunks in collection")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "hr_id": "clinic_001",
                "documents": ["pratiquesoins.pdf", "protocoles.pdf"],
                "total_chunks": 120,
                "error": None
            }
        }