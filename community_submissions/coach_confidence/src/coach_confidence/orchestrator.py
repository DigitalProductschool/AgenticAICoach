from crewai import Crew, Task
from src.coach_confidence.agents.analyzer import analyzer_agent
from src.coach_confidence.agents.rewriter import rewriter_agent
from src.coach_confidence.agents.reviewer import reviewer_agent

def run_confidence_coach_pipeline(user_text: str):
    analyze_task = Task(
        description=f"Analyze the following text for low-confidence language: \"{user_text}\"",
        agent=analyzer_agent,
        expected_output=(
            "List specific low-confidence patterns found in the text (hedging, minimizing, passive voice, etc.), "
            "with examples and clear suggestions for more assertive alternatives."
        )
    )

    rewriter_task = Task(
        description="Propose more assertive alternatives to the weak or minimizing phrases found above.",
        agent=rewriter_agent,
        expected_output=(
            "Rewrite the input text using confident, assertive language. Highlight changed phrases and explain why the new version is stronger."
        )
    )

    review_task = Task(
        description="Evaluate the revised message and rate its confidence from 1 to 5, suggesting further improvements if needed.",
        agent=reviewer_agent,
        expected_output=(
        "Return a confidence score from 1 to 5. Explain the score, list strengths in the revised message, and offer suggestions for further improvement."
    )
    )

    crew = Crew(
        agents=[analyzer_agent, rewriter_agent, reviewer_agent],
        tasks=[analyze_task, rewriter_task, review_task],
        verbose=True
    )

    return crew.kickoff()
