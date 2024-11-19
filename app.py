from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
from openai_api import generate_confident_text

# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Initialize OpenAI API
# openai.api_key = OPENAI_API_KEY

# Initialize the FastAPI app
app = FastAPI()


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

LOW_CONFIDENCE_PHRASES = {
    "hedging": ["I think", "maybe", "possibly", "I feel like"],
    "apologizing": ["I'm sorry", "apologies", "excuse me"],
    "minimizing": ["just", "only", "a little"]
}

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