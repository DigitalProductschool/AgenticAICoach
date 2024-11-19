from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
from openai_api import generate_confident_text
from typing import Optional
from uuid import uuid4

# Initialize the FastAPI app
app = FastAPI()


# Temporary in-memory store for user sessions
user_sessions = {}


class FeedbackInput(BaseModel):
    session_id: Optional[str] = None  # To track sessions
    text: str
    terminate: Optional[bool] = False  # User can terminate the loop


class FeedbackResponse(BaseModel):
    session_id: str
    original_text: str
    revised_text: Optional[str] = None
    highlights: Optional[list] = None
    confidence_score: Optional[int] = None
    overall_feedback: Optional[str] = None
    message: Optional[str] = None

# Request model for input text
class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to the Confidence Coach API!"}

@app.post("/analyze")
def analyze_text(input: TextInput):
    doc = nlp(input.text)

    response = {
        "original_text": input.text,
        "issues": [],
        "suggestions": [],
        "confidence_score": 5
    }

    # Analyze for low-confidence language
    for category, phrases in LOW_CONFIDENCE_PHRASES.items():
        for phrase in phrases:
            if phrase in input.text.lower():
                response["issues"].append(f"'{phrase}' is a {category} phrase.")
                if category == "hedging":
                    suggestion = input.text.lower().replace(phrase, "I recommend")
                elif category == "apologizing":
                    suggestion = input.text.lower().replace(phrase, "Thank you for pointing this out")
                elif category == "minimizing":
                    suggestion = input.text.lower().replace(phrase, "")
                response["suggestions"].append(suggestion)

    # Confidence score: penalize for each issue found
    response["confidence_score"] = max(1, 5 - len(response["issues"]))

    return response

@app.post("/generate_confident_text/")
async def generate_confident_text_endpoint(input: TextInput):
    output = generate_confident_text(input.text)
    if "Error" in output:
        raise HTTPException(status_code=500, detail=output)
    return {"confident_text": output}

@app.post("/feedback_loop/", response_model=FeedbackResponse)
async def feedback_loop(input: FeedbackInput):
    """
    Endpoint for the iterative feedback loop with OpenAI API integration.
    """
    session_id = input.session_id or str(uuid4())  # Generate a new session ID if not provided

    # Handle termination of the loop
    if input.terminate:
        user_sessions.pop(session_id, None)
        return FeedbackResponse(
            session_id=session_id,
            original_text=input.text,
            message="Feedback loop terminated. Thank you!"
        )

    # Analyze the input text
    try:
        analysis = generate_confident_text(input.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Store the session in memory
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "original_text": input.text,
            "revisions": []
        }

    user_sessions[session_id]["revisions"].append({
        "text": input.text,
        "analysis": analysis
    })

    # Check if further suggestions are needed
    highlights = analysis.get("highlights", [])
    if not highlights:  # If no low-confidence phrases are detected
        return FeedbackResponse(
            session_id=session_id,
            original_text=user_sessions[session_id]["original_text"],
            revised_text=input.text,
            highlights=None,
            confidence_score=analysis["confidence_score"],
            overall_feedback="Your communication is confident. No further revisions needed!",
            message="Feedback loop complete."
        )

    # Provide feedback
    return FeedbackResponse(
        session_id=session_id,
        original_text=user_sessions[session_id]["original_text"],
        revised_text=input.text,
        highlights=highlights,
        confidence_score=analysis["confidence_score"],
        overall_feedback=analysis["overall_feedback"],
        message="Submit a revised version to continue improving."
    )
