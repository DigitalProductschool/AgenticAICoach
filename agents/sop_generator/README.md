# SOP Generator Agent
This agentic AI application generates structured Standard Operating Procedures (SOPs) from high‑level process descriptions. It is built using FastAPI and returns a JSON‑formatted SOP with sections such as Purpose, Scope, Responsibilities, Materials, Steps, KPIs, Risks, and Versioning.

# How to Run Locally
Clone the repository and navigate to the project folder.
Create and activate a virtual environment:
python -m venv .venv .venv\Scripts\Activate

# Install dependencies:
pip install -r requirements.txt

# Start the FastAPI server:
uvicorn sop_agent.main:app --reload

# Open your browser and visit:
Swagger UI: http://127.0.0.1:8000/docs ReDoc: http://127.0.0.1:8000/redoc

# API Endpoint
POST /generate_sop Request Body: { "process_description": "Onboarding a new intern in a biotech lab" }

# Response:
Returns a structured SOP in JSON format.

# Deployment Instructions
This app can be deployed on Render or any free hosting platform.

# Render Setup:
Environment: Python 3.x Start command: uvicorn sop_agent.main:app --host 0.0.0.0 --port 8000 The public endpoint will be used to test the API.

# Project Structure
sop_agent/ ├─ main.py # FastAPI app ├─ agent.py # SOP generation logic ├─ models.py # Pydantic request/response models ├─ init.py requirements.txt README.md

# Example Output 
{ "title": "SOP: Onboarding a new intern in a biotech lab", "purpose": "...", "scope": "...", "responsibilities": ["..."], "materials": ["..."], "steps": ["..."], "kpis": ["..."], "risks": ["..."], "version": "v1.0", "notes": "..." }

# Notes
This agent is designed to demonstrate structured thinking, reproducible output, and production‑readiness for the DPS AI Engineering Challenge.
