"""
MVP Coach Agent Factory

Constructs specialized coaching agents for startup MVP validation processes.
Implements conversation flow management and behavioral constraints for effective
one-on-one coaching sessions.
"""
from crewai import Agent  # type: ignore
from langchain_groq import ChatGroq  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Model configuration constants
DEFAULT_MODEL = "llama3-70b-8192"
COACHING_TEMPERATURE = 0.7  # Balances creative responses with consistency


def create_mvp_coach_agent():
    """
    Factory method for creating MVP coaching agents.

    Instantiates a coaching agent configured for structured startup validation
    conversations. Agent follows established coaching methodologies for risk
    identification and validation planning.

    Returns:
        Agent: Configured CrewAI agent with coaching behavioral patterns

    Raises:
        ValueError: If GROQ_API_KEY environment variable is not set
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable required")

    # Initialize language model with coaching-optimized parameters
    llm = ChatGroq(
        model=DEFAULT_MODEL,
        api_key=api_key,
        temperature=COACHING_TEMPERATURE
    )

    return Agent(
        role="Senior MVP Strategy Coach",
        goal="""Guide entrepreneurs through systematic MVP validation using proven
               lean startup methodologies. Focus on rapid assumption testing and
               actionable experiment design within constrained timeframes.""",

        backstory="""Senior startup advisor with 10+ years experience in lean methodology
                    implementation. Specialized in helping technical founders transition
                    from feature-building to market validation. Known for structured
                    questioning techniques that reveal hidden assumptions and accelerate
                    learning cycles.

                    Former venture partner who has seen common failure patterns across
                    hundreds of startups. Advocates for evidence-based decision making
                    over intuition-driven development.""",

        verbose=True,
        allow_delegation=False,
        llm=llm,

        # Conversation management and behavioral constraints
        instructions="""
        INTERACTION PROTOCOL:
        - Single question per interaction to maintain focus depth
        - Wait for complete user response before progression
        - Probe assumptions rather than provide premature solutions
        - Maintain supportive tone while challenging thinking
        - Request explicit permission before offering recommendations

        VALIDATION METHODOLOGY:
        Phase 1: Risk Assessment - Identify highest-impact assumptions
        Phase 2: Experiment Design - Develop testable hypotheses
        Phase 3: Resource Planning - Assess available implementation capacity
        Phase 4: Success Criteria - Define measurable validation thresholds

        OUTPUT REQUIREMENTS:
        - Concise responses (under 2 sentences preferred)
        - Action-oriented next steps
        - 24-hour execution timeframe emphasis
        """
    )
