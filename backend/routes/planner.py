from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import uuid4
import re
from typing import Dict

from models import (
    ItineraryRequest, 
    RefinementRequest, 
    ItineraryResponse,
    FollowUpQuestion,
    SaveItineraryRequest,
    SaveItineraryResponse,
    ErrorResponse,
    ModelsResponse,
    ConfigUpdateRequest
)
from services.llm_service import LLMService
import os

router = APIRouter(prefix="/api/v1/planner", tags=["Holiday Planner"])

# In-memory session storage (consider using Redis in production)
sessions: Dict[str, dict] = {}

llm_service = LLMService()


def extract_follow_up_questions(itinerary_text: str) -> list[FollowUpQuestion]:
    """Extract follow-up questions from the itinerary text."""
    questions = []
    
    # Look for FOLLOW-UP QUESTIONS section
    if "FOLLOW-UP QUESTIONS" in itinerary_text:
        section = itinerary_text.split("FOLLOW-UP QUESTIONS")[-1]
        
        # Extract questions (numbered or bulleted)
        question_pattern = r'[•\-\*]?\s*(\d+\.)?\s*(.+?)(?=\n[•\-\*\d]|\Z)'
        matches = re.findall(question_pattern, section, re.MULTILINE | re.DOTALL)
        
        for idx, match in enumerate(matches, 1):
            question_text = match[1].strip()
            if question_text and len(question_text) > 5:
                questions.append(FollowUpQuestion(
                    question=question_text,
                    order=idx
                ))
    
    return questions if questions else []


@router.get(
    "/models",
    response_model=ModelsResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_models():
    """Get list of available model providers and models."""
    try:
        providers = llm_service.get_available_providers()
        return ModelsResponse(providers=providers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")


@router.post(
    "/generate",
    response_model=ItineraryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def generate_itinerary(request: ItineraryRequest):
    """
    Generate an initial holiday itinerary based on user description.
    """
    try:
        # Create a new session
        session_id = str(uuid4())
        
        # Generate itinerary
        itinerary = llm_service.generate_itinerary(
            request.description, 
            request.provider, 
            request.model
        )
        
        # Extract follow-up questions
        follow_up_questions = extract_follow_up_questions(itinerary)
        
        # Store session
        sessions[session_id] = {
            "initial_description": request.description,
            "current_itinerary": itinerary,
            "provider": request.provider,
            "model": request.model,
            "history": [
                {"role": "user", "content": request.description},
                {"role": "assistant", "content": itinerary}
            ]
        }
        
        return ItineraryResponse(
            session_id=session_id,
            itinerary=itinerary,
            follow_up_questions=follow_up_questions,
            provider=request.provider,
            model=request.model
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {str(e)}")


@router.post(
    "/refine",
    response_model=ItineraryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request or session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def refine_itinerary(request: RefinementRequest):
    """
    Refine an existing itinerary based on user feedback.
    """
    try:
        # Verify session exists
        if request.session_id not in sessions:
            raise HTTPException(status_code=400, detail=f"Session '{request.session_id}' not found")
        
        session = sessions[request.session_id]
        provider = session.get("provider", "cerebras")
        model = session.get("model", "llama-3.3-70b")
        
        # Build refinement prompt
        refinement_prompt = f"Based on my previous request and your itinerary, here's my feedback/answer: {request.feedback}\n\nPlease refine the itinerary accordingly and include updated FOLLOW-UP QUESTIONS at the end."
        
        # Generate refined itinerary with context
        refined_itinerary = llm_service.refine_itinerary(
            refinement_prompt,
            session["history"],
            provider,
            model
        )
        
        # Update session
        session["current_itinerary"] = refined_itinerary
        session["history"].append({"role": "user", "content": refinement_prompt})
        session["history"].append({"role": "assistant", "content": refined_itinerary})
        
        # Extract follow-up questions
        follow_up_questions = extract_follow_up_questions(refined_itinerary)
        
        return ItineraryResponse(
            session_id=request.session_id,
            itinerary=refined_itinerary,
            follow_up_questions=follow_up_questions,
            provider=provider,
            model=model
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refining itinerary: {str(e)}")


@router.post(
    "/save",
    response_model=SaveItineraryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request or session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def save_itinerary(request: SaveItineraryRequest, background_tasks: BackgroundTasks):
    """
    Save the current itinerary to a file.
    """
    try:
        # Verify session exists
        if request.session_id not in sessions:
            raise HTTPException(status_code=400, detail=f"Session '{request.session_id}' not found")
        
        session = sessions[request.session_id]
        itinerary_content = session["current_itinerary"]
        
        # Generate filename
        if request.filename:
            filename = f"itinerary_{request.filename}.txt"
        else:
            filename = f"itinerary_{request.session_id[:8]}.txt"
        
        # Save in background
        background_tasks.add_task(
            llm_service.save_to_file,
            filename,
            itinerary_content
        )
        
        return SaveItineraryResponse(
            success=True,
            filename=filename,
            message=f"Itinerary is being saved to {filename}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving itinerary: {str(e)}")


@router.get("/sessions/{session_id}", response_model=ItineraryResponse)
async def get_session(session_id: str):
    """
    Retrieve the current state of a session.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=400, detail=f"Session '{session_id}' not found")
    
    session = sessions[session_id]
    itinerary = session["current_itinerary"]
    follow_up_questions = extract_follow_up_questions(itinerary)
    
    return ItineraryResponse(
        session_id=session_id,
        itinerary=itinerary,
        follow_up_questions=follow_up_questions,
        provider=session.get("provider", "cerebras"),
        model=session.get("model", "llama-3.3-70b")
    )


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and its data."""
    if session_id not in sessions:
        raise HTTPException(status_code=400, detail=f"Session '{session_id}' not found")
    
    del sessions[session_id]
    return {"message": f"Session '{session_id}' deleted successfully"}


@router.post("/config/model")
async def update_model_config(request: ConfigUpdateRequest):
    """Update the default model configuration in .env file."""
    try:
        # Go up 3 levels from routes/planner.py to reach root (NewPlanner)
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        
        # Read current .env content
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Update or add variables
        new_lines = []
        provider_updated = False
        model_updated = False
        
        for line in lines:
            if line.startswith('DEFAULT_PROVIDER='):
                new_lines.append(f'DEFAULT_PROVIDER={request.provider}\n')
                provider_updated = True
            elif line.startswith('DEFAULT_MODEL='):
                new_lines.append(f'DEFAULT_MODEL={request.model}\n')
                model_updated = True
            else:
                new_lines.append(line)
        
        if not provider_updated:
            new_lines.append(f'DEFAULT_PROVIDER={request.provider}\n')
        if not model_updated:
            new_lines.append(f'DEFAULT_MODEL={request.model}\n')
            
        # Write back to .env
        with open(env_path, 'w') as f:
            f.writelines(new_lines)
            
        return {"status": "success", "message": "Configuration updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating configuration: {str(e)}")

