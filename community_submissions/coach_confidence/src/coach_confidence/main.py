from fastapi import FastAPI
from src.coach_confidence.schemas import TextInput
from src.coach_confidence.orchestrator import run_confidence_coach_pipeline
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Confidence Coach")

@app.post("/analyze")
async def analyze_text(input_data: TextInput):
    result = run_confidence_coach_pipeline(input_data.user_text)
    return {"result": result}
