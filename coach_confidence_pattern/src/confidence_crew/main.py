from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.confidence_crew.crew import ConfidenceCoachCrew
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

mistral_api_key = os.getenv("MISTRAL_API_KEY")



app = FastAPI(
    title="AI Confidence Coach",
    description="Analyze and improve communication confidence",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can restrict this to a specific domain in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {
        "message": "AI Confidence Coach API",
        "version": "1.0.0",
        "endpoints": {
            "communicate": "/communicate - POST - Analyze text for confidence",
        }
    }

# Define the input schema
class UserInput(BaseModel):
    text: str
    
    
class Suggestion(BaseModel):
    from_: str  # The original text that needs modification
    to: str 
    
# Define the response model for the structured output
class ChatResponse(BaseModel):
    revised_text: str
    suggestions: List[Suggestion]
    feedback: str


@app.post("/communicate")
async def analyze_communication(user_input: UserInput):

    input = {"text": user_input.text}

    result = ConfidenceCoachCrew().crew().kickoff(inputs=input)
    revised_text = result["revised_text"]
    suggestions = result["suggestions"]
       # Calculate confidence score based on the number of suggestions and text length
    suggestions_count = len(suggestions)
    confidence_score = calculate_confidence_score(suggestions_count, user_input.text)

    # Get feedback based on the confidence score
    feedback = get_confidence_feedback(confidence_score)

    response = ChatResponse(revised_text=revised_text, suggestions=suggestions, feedback=feedback)
    print(response)

    return response


# Confidence score calculation function using both suggestions and word count
def calculate_confidence_score(suggestions_count: int, text: str) -> float:
    word_count = len(text.split())
    score = min(5.0, 1.0 + (suggestions_count / max(word_count, 1)) * 20)
    return round(score, 2)


# Confidence level feedback function
def get_confidence_feedback(confidence_score: float) -> str:
    """Generate feedback for a confidence score from 1 (high) to 5 (low)."""
    if confidence_score == 1.0:
        return "Excellent! Your communication shows strong confidence."
    elif confidence_score <= 2.5:
        return "Good foundation! A few adjustments will boost your confidence."
    elif confidence_score <= 3.5:
        return "There's room for improvement. Focus on using more direct, assertive language."
    elif confidence_score <= 4.5:
        return "Let's work together to build more confident communication habits."
