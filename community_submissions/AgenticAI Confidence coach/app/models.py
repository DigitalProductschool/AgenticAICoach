from pydantic import BaseModel
from typing import List

class TextAnalysisRequest(BaseModel):
    """
    Input structure for text analysis.
    """
    text: str

class AnalysisResult(BaseModel):
    """
    Analysis result returned by the API.
    """
    hedging_count: int
    apologizing_count: int
    minimizing_count: int
    passive_voice_count: int
    total_issues: int
    suggestions: List[str]
    confidence_rating: str
    confidence_score: int
