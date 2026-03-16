from fastapi import FastAPI
from .models import SOPRequest, SOPResponse
from .agent import generate_sop

app = FastAPI(
    title="SOP Generator Agent",
    description="Agentic AI service that generates structured SOPs from process descriptions.",
    version="0.1.0",
)

@app.post("/generate_sop", response_model=SOPResponse)
def generate_sop_endpoint(request: SOPRequest):
    """
    Generate a structured SOP from a high-level process description.
    """
    sop = generate_sop(request)
    return sop
