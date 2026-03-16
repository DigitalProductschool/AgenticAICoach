import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# -----------------------------
# PATH FIX: allow "src." imports
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]  # project root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Load env early
load_dotenv(dotenv_path=ROOT / ".env")

# Disable CrewAI telemetry (keeps logs clean)
os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

# If you use Ollama only, keep OPENAI key empty to prevent accidental provider selection
os.environ.setdefault("OPENAI_API_KEY", "")

# -----------------------------
# Import your Crew runner funcs
# -----------------------------
from src.responsible_ai_coach.crew import run_intake, run_report  # noqa: E402


app = FastAPI(
    title="AI Ethics & Responsible AI Coach API",
    description="FastAPI endpoint for running the Responsible AI Coach (CrewAI + Ollama).",
    version="1.0.0",
)

# CORS (optional but helpful for future UI clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------
class IntakeRequest(BaseModel):
    product_description: str


class ReportRequest(BaseModel):
    product_description: str
    intake_answers: str


class ReportResponse(BaseModel):
    intake: Optional[str] = None
    risk_register: str
    action_plan: str
    templates: str


# -----------------------------
# Health / Debug
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AI Ethics Coach API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Main Endpoints
# -----------------------------
@app.post("/intake")
def generate_intake(req: IntakeRequest):
    """
    Step 1: Generate intake questions from product description.
    """
    intake = run_intake(req.product_description)
    return {"intake": intake}


@app.post("/report", response_model=ReportResponse)
def generate_report(req: ReportRequest):
    """
    Step 2: Generate the full report (risk register + action plan + templates)
    using product description + numbered intake answers.
    """
    final_context = f"""
AI Product Description:
{req.product_description.strip()}

User Intake Answers:
{req.intake_answers.strip()}
""".strip()

    outputs = run_report(final_context)

    return ReportResponse(
        intake=outputs.get("intake"),
        risk_register=str(outputs.get("risk_register", "")),
        action_plan=str(outputs.get("action_plan", "")),
        templates=str(outputs.get("templates", "")),
    )
