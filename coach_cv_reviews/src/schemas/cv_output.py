from pydantic import BaseModel, Field
from typing import List

class CVReview(BaseModel):
    """
    A Pydantic model that defines the structured output for the CV review.
    This ensures the AI's output is always in a predictable, JSON-friendly format.
    """
    overall_score: str = Field(description="A score out of 10, as a string (e.g., '8.5/10').")
    score_justification: str = Field(description="A brief, one-sentence justification for the overall score.")
    cv_analysis: str = Field(description="A detailed summary of the CV's strengths and weaknesses, formatted as a Markdown string.")
    technical_analysis: str = Field(description="A detailed summary of the repository review, formatted as a Markdown string. If no repos were found, this should state that.")
    actionable_suggestions: List[str] = Field(description="A list of the top 3-4 most critical improvement suggestions.")
    suggested_job_roles: List[str] = Field(description="A list of 3-5 job titles that would be a good fit.")