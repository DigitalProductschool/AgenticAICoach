from pydantic import BaseModel
from typing import List, Dict, Optional

class AnalysisRequest(BaseModel):
    text: str
    session_id: Optional[str] = None

class FeedbackResponse(BaseModel):
    session_id: str
    confidence_score: int
    feedback_summary: str
    suggestions: List[str]
    revised_examples: List[str]
    history: List[Dict] = []