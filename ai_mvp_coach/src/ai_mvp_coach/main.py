"""
MVP Coaching Application Entry Point

Provides command-line interface for structured startup validation coaching.
Implements lean methodology principles through guided conversation workflows.
"""
import os
import sys
from dotenv import load_dotenv  # type: ignore

# Module path configuration for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai_mvp_coach.crew import MVPCoachingCrew  # noqa: E402

# Application configuration constants
APP_NAME = "MVP Validation Coach"
REQUIRED_ENV_VARS = ["GROQ_API_KEY"]


def validate_environment():
    """
    Verify required environment configuration.

    Returns:
        bool: True if environment is properly configured
    """
    load_dotenv()

    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            print(f"Configuration Error: {var} environment variable required")
            print("Please configure your .env file with required API credentials")
            return False
    return True


def collect_initial_context():
    """
    Gather initial product concept from user input.

    Returns:
        str: Product concept description for coaching analysis
    """
    print(f"\n{APP_NAME}")
    print("=" * len(APP_NAME))
    print("Structured validation coaching for startup concepts\n")

    print("Describe your product concept:")
    user_input = input("> ").strip()

    if not user_input:
        return "Unspecified startup concept requiring validation"

    return user_input


def execute_coaching_workflow(product_concept):
    """
    Run complete coaching session workflow.

    Args:
        product_concept: Initial product description

    Returns:
        bool: True if session completed successfully
    """
    try:
        coaching_crew = MVPCoachingCrew()
        result = coaching_crew.execute_coaching_session(product_concept)

        if result:
            summary = coaching_crew.get_session_summary()
            print("\nSession completed successfully")
            print(f"Outcome: {summary['outcome']}")
            print(f"Next steps: {summary['next_steps']}")
            return True
        else:
            print("Session execution failed. Check configuration and retry.")
            return False

    except KeyboardInterrupt:
        print("\nSession terminated by user")
        return False
    except Exception as e:
        print(f"Session error: {e}")
        return False


def main():
    """Application entry point."""
    if not validate_environment():
        return

    product_concept = collect_initial_context()
    execute_coaching_workflow(product_concept)


if __name__ == "__main__":
    main()
