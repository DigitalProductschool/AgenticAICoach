from crewai import Agent
from src.coach_confidence.llm.gemini import get_gemini_llm

analyzer_agent = Agent(
    role="Confidence Analyzer",
    goal="Analyze user input for low-confidence language",
    backstory="You are a linguistic coach with expertise in identifying passive or minimizing communication styles.",
    verbose=True,
    llm=get_gemini_llm(),
    allow_delegation=False
)
