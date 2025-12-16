from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class BudgetCategory(str, Enum):
    """Budget category enumeration."""
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")


class ModelItem(BaseModel):
    """Model information."""
    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name of the model")


class ProviderInfo(BaseModel):
    """Provider information."""
    provider: str = Field(..., description="Provider identifier")
    name: str = Field(..., description="Display name of the provider")
    models: List[ModelItem] = Field(..., description="List of available models")


class ModelsResponse(BaseModel):
    """Response model for available models."""
    providers: List[ProviderInfo] = Field(..., description="List of available providers and their models")


class ItineraryRequest(BaseModel):
    """Initial itinerary request model."""
    description: str = Field(
        ..., 
        description="Description of the ideal holiday including destination, duration, budget, and interests",
        min_length=10,
        max_length=1000
    )
    provider: str = Field("cerebras", description="Model provider to use")
    model: str = Field("llama-3.3-70b", description="Model ID to use")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "I want a 7-day tropical vacation in Bali with a moderate budget.",
                "provider": "cerebras",
                "model": "llama-3.3-70b"
            }
        }


class RefinementRequest(BaseModel):
    """Request model for refining an existing itinerary."""
    session_id: str = Field(
        ..., 
        description="Unique session identifier for conversation context"
    )
    feedback: str = Field(
        ..., 
        description="User feedback or answers to follow-up questions",
        min_length=5,
        max_length=1000
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123456",
                "feedback": "I prefer more adventure activities."
            }
        }


class FollowUpQuestion(BaseModel):
    """Model for follow-up questions."""
    question: str = Field(..., description="The follow-up question")
    order: int = Field(..., description="Question sequence number")


class ItineraryResponse(BaseModel):
    """Itinerary response model."""
    session_id: str = Field(..., description="Unique session identifier")
    itinerary: str = Field(..., description="Generated itinerary content")
    follow_up_questions: List[FollowUpQuestion] = Field(
        ..., 
        description="List of follow-up questions for refinement"
    )
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123456",
                "itinerary": "# 7-Day Bali Itinerary...",
                "follow_up_questions": [
                    {
                        "question": "Would you prefer beachfront or jungle accommodations?",
                        "order": 1
                    }
                ],
                "provider": "cerebras",
                "model": "llama-3.3-70b"
            }
        }


class SaveItineraryRequest(BaseModel):
    """Request model to save an itinerary."""
    session_id: str = Field(..., description="Session ID of the itinerary to save")
    filename: Optional[str] = Field(
        None, 
        description="Custom filename (without extension)",
        max_length=100
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123456",
                "filename": "bali_trip"
            }
        }


class SaveItineraryResponse(BaseModel):
    """Response model for saved itinerary."""
    success: bool = Field(..., description="Whether the save was successful")
    filename: str = Field(..., description="Name of the saved file")
    message: str = Field(..., description="Response message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "itinerary_bali_trip.txt",
                "message": "Itinerary saved successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "API Key Missing",
                "detail": "CEREBRAS_API_KEY not found in environment variables"
            }
        }


class ConfigUpdateRequest(BaseModel):
    """Request model for updating configuration."""
    provider: str = Field(..., description="Default provider to set")
    model: str = Field(..., description="Default model to set")

