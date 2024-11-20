from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from models import TextInput, FeedbackInput, FeedbackResponse
from openai_api import generate_confident_text
from uuid import uuid4
from dotenv import load_dotenv
import os 

load_dotenv()
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Initialize the FastAPI app
app = FastAPI()

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Front-end origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Temporary in-memory store for user sessions
user_sessions = {}

# API endpoints

@app.get("/")
@app.get("/", response_class=HTMLResponse)
def serve_html():
    return open("index.html").read()


@app.post("/generate_confident_text/")
async def generate_confident_text_endpoint(input: TextInput):
    """
    Endpoint to generate a more confident version of the provided text.

    This endpoint accepts an input string, processes it to identify areas where the language 
    can be made more assertive, and returns a revised version of the text. If an error occurs 
    during processing, it raises an HTTP 500 exception.

    **Request Body:**
    - `text` (TextInput): A Pydantic model containing the input text.

    **Response:**
    - `dict`: A dictionary containing the revised confident text.

    Example Response:
    - Input: `"I would like to go first."`
    - Output: 
    ```json
    {
        "confident_text": {
            "highlights": [
                {
                    "low_confidence_phrase": "I would like to",
                    "suggestion": "I will go first."
                }
                ],
            "confidence_score": 3,
            "overall_feedback": "Use more assertive language to increase confidence in your communication."
        }
    }
    ```

    Raises:
        HTTPException: If the text generation process encounters an error, an HTTP 500 error is raised with the error details.
    """
    output = generate_confident_text(input.text)
    if "Error" in output:
        raise HTTPException(status_code=500, detail=output)
    return {"confident_text": output}


@app.post("/feedback_loop/", response_model=FeedbackResponse)
async def feedback_loop(input: FeedbackInput):
    """
    This endpoint analyzes the confidence level of the input text and provides actionable feedback.

    **Request Body:**
    - `text`: The communication text to analyze.
    - `session_id`: A unique identifier for the user session.
    - `terminate`: A flag to terminate the feedback loop.

    **Response:**
    - `highlights`: A list of low-confidence phrases with improvement suggestions.
    - `confidence_score`: A score indicating the confidence level.
    - `overall_feedback`: General advice to improve communication confidence.

    Example:
    - Input: `"I'm sorry, but I think this might not work."`
    - Output:
    ```json
    {
        "highlights": [
            {"low_confidence_phrase": "I'm sorry", "suggestion": "I acknowledge"},
            {"low_confidence_phrase": "I think", "suggestion": "I believe"}
        ],
        "confidence_score": "2/5",
        "overall_feedback": "Avoid excessive apologizing and use more assertive language."
    }
    ```
    """
    
    # Generate a new session ID if not provided
    session_id = input.session_id or str(uuid4())  

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
