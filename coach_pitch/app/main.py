from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from utils.coaching_flow import PitchCoachFlow
from utils.crew_setup import PitchCoachCrew
from utils.feedback_tracker import FeedbackTracker
from typing import Optional, List, Dict, Any
import time
import os

# At the end of your file, add this if not already present:
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

app = FastAPI(title="AI Pitch Coach")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve the index.html file
@app.get("/ui")
async def get_ui():
    return FileResponse("app/static/index.html")

#dding a root redirect so that when someone visits the root URL (/), they're redirected to /ui:
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")


# Store active coaching sessions
active_sessions = {}

class SessionRequest(BaseModel):
    user_id: str = "default"

class MessageRequest(BaseModel):
    session_id: str
    message: str
    user_id: str = "default"

class ActionRequest(BaseModel):
    session_id: str
    action: str  # "qa" or "feedback"
    user_id: str = "default"

class SessionResponse(BaseModel):
    session_id: str
    welcome_message: str

class MessageResponse(BaseModel):
    response: str
    complete_pitch: Optional[str] = None
    is_pitch_complete: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Pitch Coach API"}

@app.post("/start_session", response_model=SessionResponse)
async def start_coaching_session(request: SessionRequest):
    """Start a new coaching session"""
    try:
        # Create a new coaching flow
        coach = PitchCoachFlow()
        
        # Generate a session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store the session
        active_sessions[session_id] = {
            "coach": coach,
            "user_id": request.user_id,
            "created_at": time.time()
        }
        
        # Get the welcome message
        welcome_message = coach.start_conversation()
        
        return {
            "session_id": session_id,
            "welcome_message": welcome_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")

@app.post("/send_message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Send a message to the coach and get a response"""
    try:
        # Check if session exists
        if request.session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get the coach
        session = active_sessions[request.session_id]
        coach = session["coach"]
        
        # Process the message
        response = coach.process_response(request.message)
        
        # Check if the pitch is complete
        is_complete = coach.current_stage == "summary"
        complete_pitch = None
        
        if is_complete:
            complete_pitch = coach._generate_complete_pitch()
            
            # Save the complete pitch
            tracker = FeedbackTracker(request.user_id)
            tracker.add_pitch_feedback(
                complete_pitch, 
                "Generated through guided coaching session", 
                None
            )
        
        return {
            "response": response,
            "complete_pitch": complete_pitch,
            "is_pitch_complete": is_complete
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.post("/session_action")
async def perform_session_action(request: ActionRequest):
    """Perform a session action like generating Q&A or feedback"""
    try:
        # Check if session exists
        if request.session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get the coach
        session = active_sessions[request.session_id]
        coach = session["coach"]
        
        if request.action == "qa":
            # Generate investor questions
            result = coach.get_investor_questions()
            return {"result": result, "action": "qa"}
            
        elif request.action == "feedback":
            # Generate pitch clarity feedback
            result = coach.get_pitch_clarity_feedback()
            return {"result": result, "action": "feedback"}
            
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform action: {str(e)}")

@app.get("/session_history/{session_id}")
async def get_session_history(session_id: str):
    """Get the history of a coaching session"""
    try:
        # Check if session exists
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get the coach
        session = active_sessions[session_id]
        coach = session["coach"]
        
        return {"history": coach.get_history()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

# Keep the existing endpoints for backward compatibility
@app.post("/analyze_pitch")
async def analyze_pitch(request: dict):
    try:
        crew = PitchCoachCrew()
        result = crew.analyze_initial_pitch(request.get("pitch_content", ""))
        result_str = str(result)
        
        # Track feedback
        tracker = FeedbackTracker(request.get("user_id", "default"))
        pitch_id = tracker.add_pitch_feedback(
            request.get("pitch_content", ""), 
            result_str,
            request.get("pitch_id")
        )
        
        return {
            "analysis": result_str, 
            "status": "success", 
            "pitch_id": pitch_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/simulate_qa")
async def simulate_investor_qa(request: dict):
    try:
        crew = PitchCoachCrew()
        result = crew.simulate_investor_qa(
            request.get("pitch_content", ""),
            request.get("industry", "technology"),
            request.get("funding_stage", "seed")
        )
        
        result_str = str(result)
        
        return {"qa_simulation": result_str, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A simulation failed: {str(e)}")

@app.post("/pitch_history")
async def get_pitch_history(request: dict):
    try:
        tracker = FeedbackTracker(request.get("user_id", "default"))
        history = tracker.get_pitch_history(request.get("pitch_id", ""))
        
        if not history:
            raise HTTPException(status_code=404, detail="Pitch history not found")
        
        metrics = tracker.get_improvement_metrics(request.get("pitch_id", ""))
        
        return {
            "history": history,
            "metrics": metrics,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@app.get("/all_pitches/{user_id}")
async def get_all_pitches(user_id: str = "default"):
    try:
        tracker = FeedbackTracker(user_id)
        pitches = tracker.get_all_pitches()
        
        return {
            "pitches": pitches,
            "count": len(pitches),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve pitches: {str(e)}")