from pydantic import BaseModel
from typing import Optional

# Request model for input text
class TextInput(BaseModel):
    text: str

# Feedback models
class FeedbackInput(BaseModel):
    session_id: Optional[str] = None  # To track sessions
    text: str
    terminate: Optional[bool] = False  # User can terminate the loop


class FeedbackResponse(BaseModel):
    session_id: str
    original_text: str
    revised_text: Optional[str] = None
    highlights: Optional[list] = None
    confidence_score: Optional[int] = None
    overall_feedback: Optional[str] = None
    message: Optional[str] = None

