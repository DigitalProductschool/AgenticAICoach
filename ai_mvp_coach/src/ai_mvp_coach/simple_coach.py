"""
Standalone MVP Coaching Implementation

Direct coaching implementation bypassing CrewAI framework dependencies.
Provides structured validation conversations using Groq LLM integration.
"""
from groq import Groq  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Coaching session configuration
DEFAULT_MODEL = "llama3-70b-8192"
MAX_RESPONSE_TOKENS = 200
COACHING_TEMPERATURE = 0.7


class MVPCoachingSession:
    """
    Implements structured MVP validation coaching methodology.

    Provides conversational guidance through lean startup validation phases
    using single-question interaction patterns for depth over breadth.
    """

    def __init__(self):
        """Initialize coaching session with LLM client and conversation state."""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable required")

        self.client = Groq(api_key=api_key)
        self.model = DEFAULT_MODEL
        self.conversation_history = []
        self.current_phase = "risk_assessment"

    def _get_coaching_prompt(self):
        """
        Generate context-aware system prompt for coaching interactions.

        Returns:
            str: System prompt optimized for current coaching phase
        """
        return """Senior startup advisor specializing in lean validation methodology.

INTERACTION PROTOCOL:
- Single question per response to maintain conversation depth
- Probe underlying assumptions rather than surface-level features
- Challenge thinking while maintaining supportive tone
- Request explicit permission before offering recommendations
- Guide toward rapid, low-cost validation experiments

CURRENT OBJECTIVE: Help entrepreneur identify and test their riskiest business assumption.

Ask ONE insightful question that reveals what they're most uncertain about."""

    def process_user_input(self, user_input):
        """
        Process user input and generate coaching response.

        Args:
            user_input: User's response to previous coaching question

        Returns:
            str: Coaching question or guidance for next interaction
        """
        self.conversation_history.append({"role": "user", "content": user_input})

        messages = [
            {"role": "system", "content": self._get_coaching_prompt()}
        ] + self.conversation_history

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=COACHING_TEMPERATURE,
                max_tokens=MAX_RESPONSE_TOKENS
            )

            response = completion.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": response})

            return response

        except Exception as e:
            return f"Session error: {e}. Please check configuration and retry."


def run_coaching_session():
    """
    Execute interactive coaching session workflow.

    Provides command-line interface for structured validation coaching.
    Implements graceful session termination and error handling.
    """
    try:
        coach = MVPCoachingSession()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    print("MVP Validation Coach")
    print("=" * 20)
    print("Structured startup validation coaching\n")
    print("Describe your startup concept:")

    initial_input = input("> ").strip()
    if not initial_input:
        print("Please provide your concept to begin coaching.")
        return

    print("\nBeginning structured validation coaching...")
    print("Type 'exit' to end session at any time.\n")

    response = coach.process_user_input(f"Product concept: {initial_input}")
    print(f"Coach: {response}")

    # Main coaching conversation loop
    while True:
        print("\n" + "-" * 40)
        user_response = input("You: ").strip()

        if user_response.lower() in ['exit', 'quit', 'done', 'stop']:
            print("\nSession complete. Execute your validation plan within 24 hours.")
            break

        if not user_response:
            print("Please respond to continue, or type 'exit' to end session.")
            continue

        response = coach.process_user_input(user_response)
        print(f"\nCoach: {response}")


if __name__ == "__main__":
    run_coaching_session()
