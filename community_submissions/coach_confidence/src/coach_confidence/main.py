from fastapi import FastAPI
from src.confidence_coach.routers import analysis

app = FastAPI(
    title="AI Confidence Coach",
    description="Agent for analyzing communication patterns and providing confidence-building feedback",
    version="0.1.0"
)

app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])