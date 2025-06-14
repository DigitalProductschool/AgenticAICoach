"""
FastAPI Backend for AI MVP Coach

Simple REST API and web interface for AI-powered MVP coaching.
Designed for demo and production deployment without complex authentication.
"""
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import uuid
from datetime import datetime
from pathlib import Path
from ..simple_coach import MVPCoachingSession
from .database import get_db, init_database
from .chat_service import ChatService


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    yield
    # Shutdown (if needed)


# Initialize FastAPI app
app = FastAPI(
    title="AI MVP Coach API",
    description="AI-powered MVP coaching and validation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# In-memory storage for coaching sessions (coach objects only)
# Database handles persistence, but we need to keep MVPCoachingSession objects in memory
active_coaches = {}


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
async def chat_with_coach(message: CoachingMessage, db: Session = Depends(get_db)):
    """Send message to AI coach and get response"""
    try:
        session_id = message.session_id or str(uuid.uuid4())
        start_time = datetime.utcnow()

        # Get or create coaching session in database
        db_session = ChatService.get_session(db, session_id)
        if not db_session:
            db_session = ChatService.create_session(db, session_id)

        # Get or create coaching session object in memory
        if session_id not in active_coaches:
            coach_session = MVPCoachingSession()
            active_coaches[session_id] = coach_session
        else:
            coach_session = active_coaches[session_id]

        # Process coaching interaction
        response = coach_session.process_user_input(message.message)

        # Calculate response time
        response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        # Generate suggestions based on current phase
        suggestions = _generate_suggestions(coach_session.current_phase)

        # Save message to database
        ChatService.add_message(
            db=db,
            session_id=session_id,
            user_message=message.message,
            coach_response=response,
            phase=coach_session.current_phase,
            suggestions=suggestions,
            response_time_ms=response_time_ms
        )

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
async def get_all_sessions(db: Session = Depends(get_db)):
    """Get all coaching sessions"""
    db_sessions = ChatService.get_all_sessions(db)
    all_sessions = []

    for session in db_sessions:
        all_sessions.append(SessionSummary(
            session_id=session.id,
            started_at=session.created_at,
            last_activity=session.last_activity,
            phase=session.current_phase,
            message_count=session.message_count,
            status=session.status
        ))

    return all_sessions


@app.get("/api/sessions/{session_id}/conversation", tags=["Coaching"])
async def get_session_conversation(session_id: str, db: Session = Depends(get_db)):
    """Get conversation history for a specific session"""
    conversation_data = ChatService.get_conversation_history(db, session_id)

    if not conversation_data:
        raise HTTPException(status_code=404, detail="Session not found")

    return conversation_data


# Form submission endpoint for web interface
@app.post("/submit-message", response_class=HTMLResponse, tags=["Web Interface"])
async def submit_message(request: Request, message: str = Form(...), session_id: str = Form(None), db: Session = Depends(get_db)):
    """Handle form submission from web interface"""
    try:
        coaching_msg = CoachingMessage(message=message, session_id=session_id)
        response = await chat_with_coach(coaching_msg, db)

        # Return updated chat interface with response
        return templates.TemplateResponse("chat_response.html", {
            "request": request,
            "response": response,
            "user_message": message
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", tags=["Analytics"])
async def get_statistics(db: Session = Depends(get_db)):
    """Get overall chat statistics"""
    return ChatService.get_session_stats(db)


@app.delete("/api/sessions/{session_id}", tags=["Coaching"])
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session and all its messages"""
    success = ChatService.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")

    # Also remove from active coaches if present
    if session_id in active_coaches:
        del active_coaches[session_id]

    return {"message": "Session deleted successfully"}


@app.put("/api/sessions/{session_id}/status", tags=["Coaching"])
async def update_session_status(session_id: str, status: str, db: Session = Depends(get_db)):
    """Update session status (active, completed, paused)"""
    valid_statuses = ["active", "completed", "paused"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    session = ChatService.update_session_status(db, session_id, status)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": f"Session status updated to {status}"}


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
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("uvicorn not installed. Install with: pip install uvicorn")
