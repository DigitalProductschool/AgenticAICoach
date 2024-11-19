from fastapi import FastAPI
from pydantic import BaseModel
import spacy

# Initialize the FastAPI app
app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Request model for input text
class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to the Confidence Coach API!"}

@app.post("/analyze")
def analyze_text(input: TextInput):
    """
    Analyze the text for low-confidence language patterns.
    """
    doc = nlp(input.text)

    # Response template
    response = {
        "original_text": input.text,
        "issues": [],
        "suggestions": [],
        "confidence_score": 0
    }

    # Placeholder for rules-based confidence analysis (to be implemented next)
    response["issues"].append("This is a placeholder for issues.")
    response["suggestions"].append("This is a placeholder for suggestions.")
    response["confidence_score"] = 3  # Placeholder confidence score (scale: 1-5)

    return response
