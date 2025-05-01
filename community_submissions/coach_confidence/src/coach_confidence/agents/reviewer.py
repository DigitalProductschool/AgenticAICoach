from crewai import Agent
from src.coach_confidence.llm.gemini import get_gemini_llm

reviewer_agent = Agent(
    role="Confidence Reviewer",
    goal="Track improvement and give encouragement",
    backstory="You provide feedback on how much more confident the revised message sounds and encourage growth.",
    verbose=True,
    llm=get_gemini_llm(),
    allow_delegation=False
)
