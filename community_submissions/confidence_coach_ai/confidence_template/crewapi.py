from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crew import ConfidenceCrew
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import logging

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the crew
crew = ConfidenceCrew()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Data models
class TextAnalysisRequest(BaseModel):
    text: str

class AudioTranscriptionRequest(BaseModel):
    audio_path: str

class RefinementRequest(BaseModel):
    original_text: str
    refined_text: str


def get_analysis_by_id(analysis_id: str, filepath: str = "analysis_history.json") -> Optional[Dict]:
    """Loads a specific analysis by its ID."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            for analysis in data:
                if analysis["analysis_id"] == analysis_id:
                    return analysis
        return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding JSON. Returning None.")
        return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_absolute_path(relative_path):
    """Convert relative paths to absolute paths"""
    return os.path.join(BASE_DIR, relative_path)

# File paths for storage
ANALYSIS_HISTORY_FILE = get_absolute_path("data/analysis_history.json")
RATING_HISTORY_FILE = get_absolute_path("data/rating_history.json")
REFINEMENT_HISTORY_FILE = get_absolute_path("data/refinement_history.json")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Helper functions for file operations
def _load_json_file(file_path: str, default: Any = []) -> Any:
    """Load JSON data from file or return default if file doesn't exist"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def _save_json_file(file_path: str, data: Any):
    """Save data to JSON file"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def _get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint for API monitoring"""
    return {"status": "healthy", "timestamp": _get_timestamp()}



@app.post("/analyze")
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text for confidence-related insights"""
    try:
        # Perform analysis
        analysis = await crew.analyze_text(request.text)
        
        # Generate unique ID for this analysis
        analysis_id = str(uuid.uuid4())
        
        # Save to analysis history
        history = _load_json_file(ANALYSIS_HISTORY_FILE)
        history_entry = {
            "id": analysis_id,
            "timestamp": _get_timestamp(),
            "original_text": request.text,
            "analysis": analysis
        }
        history.append(history_entry)
        _save_json_file(ANALYSIS_HISTORY_FILE, history)
        
        # Save rating separately to rating history
        rating_history = _load_json_file(RATING_HISTORY_FILE)
        rating_entry = {
            "id": analysis_id,
            "timestamp": _get_timestamp(),
            "text": request.text,
            "rating": analysis["rating"],
        }
        rating_history.append(rating_entry)
        _save_json_file(RATING_HISTORY_FILE, rating_history)
        
        return {
            "id": analysis_id,
            **analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe")
async def transcribe_audio(request: AudioTranscriptionRequest):
    """Transcribe audio file to text"""
    try:
        transcript = crew.transcribe_audio(request.audio_path)
        return {
            "transcript": transcript,
            "audio_path": request.audio_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine")
async def refine_text(request: RefinementRequest):
    """Save refined text versions"""
    try:
        # Load existing refinements
        refinements = _load_json_file(REFINEMENT_HISTORY_FILE)
        
        # Create new refinement entry
        refinement_id = str(uuid.uuid4())
        refinement_entry = {
            "id": refinement_id,
            "timestamp": _get_timestamp(),
            "original_text": request.original_text,
            "refined_text": request.refined_text
        }
        
        # Add to history and save
        refinements.append(refinement_entry)
        _save_json_file(REFINEMENT_HISTORY_FILE, refinements)
        
        return {
            "id": refinement_id,
            "status": "success",
            "refined_text": request.refined_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rating-history/{user_id}")
async def get_rating_history(user_id: str):
    """Get rating history for a user with proper data structure"""
    try:
        analysis_history = _load_json_file(ANALYSIS_HISTORY_FILE, default=[])
        
        # Filter and format the history entries
        user_history = []
        for entry in analysis_history:
            if entry.get("analysis"):  # Ensure analysis exists
                user_history.append({
                    "id": entry["id"],
                    "timestamp": entry.get("timestamp", ""),
                    "text": entry.get("original_text", ""),
                    "rating": entry["analysis"].get("rating", "N/A"),
                    "user_id": user_id  # Add user_id to each entry
                })
        
        return {
            "user_id": user_id,
            "history": user_history,
            "count": len(user_history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-ratings")
async def analyze_multiple_ratings_endpoint(
    previous_analysis_id: str = Form(...),
    previous_analysis_id_2: str = Form(...), 
    previous_analysis_id_3: str = Form(...)
):
    """Analyze three specific ratings for trends"""
    try:
        # Get the three analyses from history
        analysis1 = get_analysis_by_id(previous_analysis_id)
        analysis2 = get_analysis_by_id(previous_analysis_id_2)
        analysis3 = get_analysis_by_id(previous_analysis_id_3)

        if not all([analysis1, analysis2, analysis3]):
            raise HTTPException(
                status_code=404,
                detail="One or more analyses not found"
            )

        # Extract just the rating data
        rating1 = {
            "text": analysis1["original_text"],
            "rating": analysis1["analysis"]["rating"],
            "timestamp": analysis1["timestamp"]
        }
        rating2 = {
            "text": analysis2["original_text"],
            "rating": analysis2["analysis"]["rating"],
            "timestamp": analysis2["timestamp"]
        }
        rating3 = {
            "text": analysis3["original_text"],
            "rating": analysis3["analysis"]["rating"],
            "timestamp": analysis3["timestamp"]
        }

        # Perform analysis using the crew
        analysis_result = await crew.analyze_multiple_ratings(
            rating1,
            rating2,
            rating3
        )

        return {
            "analysis": analysis_result,
            "ratings_used": [
                previous_analysis_id,
                previous_analysis_id_2,
                previous_analysis_id_3
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Rating analysis failed: {str(e)}"
        )

@app.get("/analysis-history")
async def get_analysis_history():
    """Get complete analysis history"""
    try:
        return _load_json_file(ANALYSIS_HISTORY_FILE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/emotional-advice")
async def get_emotional_advice(request: TextAnalysisRequest):
    """Get emotional advice based on user's feelings"""
    try:
        advice = await crew.give_advice(request.text)
        
        return {
            "advice": advice,
            "original_text": request.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if not set
    uvicorn.run(
        app,
        host="0.0.0.0",  # Critical for Streamlit Cloud
        port=port,
    )

