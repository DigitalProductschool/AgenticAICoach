"""
FastAPI Backend for AI MVP Coach

Simple REST API and web interface for AI-powered MVP coaching.
Designed for demo and production deployment without complex authentication.
"""
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import json
from datetime import datetime
import os
from pathlib import Path
from ..simple_coach import MVPCoachingSession

# Initialize FastAPI app
app = FastAPI(
    title="AI MVP Coach API",
    description="AI-powered MVP coaching and validation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# In-memory storage for demo (replace with database in production)
sessions_db = {}
conversations_db = {}

# Pydantic Models
class CoachingMessage(BaseModel):
    message: str = Field(..., description="User message to the coach")
    session_id: Optional[str] = Field(None, description="Session ID for continuing conversation")

class CoachingResponse(BaseModel):
    session_id: str
    coach_response: str
    phase: str
    timestamp: datetime
    suggestions: List[str] = []

class SessionSummary(BaseModel):
    session_id: str
    started_at: datetime
    last_activity: datetime
    phase: str
    message_count: int
    status: str

# Web Interface Routes
@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def home(request: Request):
    """Main web interface for the AI MVP Coach"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse, tags=["Web Interface"])
async def chat_page(request: Request):
    """Chat interface page"""
    return templates.TemplateResponse("chat.html", {"request": request})

# API Endpoints
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "message": "AI MVP Coach API is running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow()
    }

@app.post("/api/chat", response_model=CoachingResponse, tags=["Coaching"])
async def chat_with_coach(message: CoachingMessage):
    """Send message to AI coach and get response"""
    try:
        session_id = message.session_id or str(uuid.uuid4())
        
        # Get or create coaching session
        if session_id not in sessions_db:
            coach_session = MVPCoachingSession()
            sessions_db[session_id] = {
                "coach": coach_session,
                "created_at": datetime.utcnow(),
                "last_activity": datetime.utcnow(),
                "message_count": 0
            }
            conversations_db[session_id] = []
        else:
            coach_session = sessions_db[session_id]["coach"]
            sessions_db[session_id]["last_activity"] = datetime.utcnow()
        
        # Process coaching interaction
        response = coach_session.coaching_conversation(message.message)
        
        # Update conversation history
        conversations_db[session_id].append({
            "timestamp": datetime.utcnow(),
            "user_message": message.message,
            "coach_response": response,
            "phase": coach_session.current_phase
        })
        
        sessions_db[session_id]["message_count"] += 1
        
        # Generate suggestions based on current phase
        suggestions = _generate_suggestions(coach_session.current_phase)
        
        return CoachingResponse(
            session_id=session_id,
            coach_response=response,
            phase=coach_session.current_phase,
            timestamp=datetime.utcnow(),
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coaching error: {str(e)}")

@app.get("/api/sessions", response_model=List[SessionSummary], tags=["Coaching"])
async def get_all_sessions():
    """Get all coaching sessions (for demo purposes)"""
    all_sessions = []
    for session_id, session_data in sessions_db.items():
        all_sessions.append(SessionSummary(
            session_id=session_id,
            started_at=session_data["created_at"],
            last_activity=session_data["last_activity"],
            phase=session_data["coach"].current_phase,
            message_count=session_data["message_count"],
            status="active"
        ))
    
    return sorted(all_sessions, key=lambda x: x.last_activity, reverse=True)

@app.get("/api/sessions/{session_id}/conversation", tags=["Coaching"])
async def get_session_conversation(session_id: str):
    """Get conversation history for a specific session"""
    if session_id not in sessions_db:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions_db[session_id]
    return {
        "session_id": session_id,
        "conversation": conversations_db.get(session_id, []),
        "session_info": {
            "created_at": session_data["created_at"],
            "last_activity": session_data["last_activity"],
            "message_count": session_data["message_count"],
            "current_phase": session_data["coach"].current_phase
        }
    }

# Form submission endpoint for web interface
@app.post("/submit-message", response_class=HTMLResponse, tags=["Web Interface"])
async def submit_message(request: Request, message: str = Form(...), session_id: str = Form(None)):
    """Handle form submission from web interface"""
    try:
        coaching_msg = CoachingMessage(message=message, session_id=session_id)
        response = await chat_with_coach(coaching_msg)
        
        # Return updated chat interface with response
        return templates.TemplateResponse("chat_response.html", {
            "request": request,
            "response": response,
            "user_message": message
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _generate_suggestions(phase: str) -> List[str]:
    """Generate contextual suggestions based on current coaching phase"""
    suggestions_map = {
        "risk_assessment": [
            "What's the biggest assumption in your business model?",
            "Who would be most disappointed if your product didn't exist?",
            "What evidence do you have that this problem needs solving?"
        ],
        "customer_discovery": [
            "Can you describe your ideal customer in detail?",
            "What job is your customer trying to get done?",
            "How do customers currently solve this problem?"
        ],
        "problem_validation": [
            "How painful is this problem for your customers?",
            "What would happen if this problem wasn't solved?",
            "How often does this problem occur?"
        ],
        "solution_validation": [
            "What's the simplest version of your solution?",
            "What features are absolutely essential?",
            "How will you measure solution effectiveness?"
        ]
    }
    
    return suggestions_map.get(phase, [
        "Tell me more about your MVP idea",
        "What's your biggest challenge right now?",
        "How can I help you validate your assumptions?"
    ])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
