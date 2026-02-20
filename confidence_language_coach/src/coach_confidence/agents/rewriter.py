from crewai import Agent
from src.coach_confidence.llm.gemini import get_gemini_llm

rewriter_agent = Agent(
    role="Confidence Rewriter",
    goal="Suggest assertive alternatives to low-confidence language",
    backstory="You are a communication strategist helping people sound more confident, clear, and direct.",
    verbose=True,
    llm=get_gemini_llm(),
    allow_delegation=False
)
