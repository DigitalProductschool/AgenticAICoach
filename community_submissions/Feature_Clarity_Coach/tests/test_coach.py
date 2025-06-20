import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew import FeatureClarityCoach, UserState


@pytest.fixture
def base_state():
    return UserState(user_input="I want to build a productivity app")


def test_initial_phase_is_core_problem(base_state):
    coach = FeatureClarityCoach(initial_state=base_state)
    assert coach.state.phase == "core_problem"


def test_uncertainty_forces_stay():
    user_state = UserState(user_input="I'm not sure what to build", phase="core_problem")
    coach = FeatureClarityCoach(initial_state=UserState())
    coach.kickoff(user_state.model_dump())
    assert coach.state.phase == "core_problem"


def test_phase_transitions_to_complete():
    user_state = UserState(
        user_input="Finalize this",
        phase="validate",
        phase_summaries={
            "core_problem": "Low engagement",
            "core_value": "Save time",
            "brainstorm_solution": "AI coach",
            "validate": "Validated with real users"
        }
    )
    coach = FeatureClarityCoach(initial_state=UserState())
    coach.kickoff(user_state.model_dump())
    assert coach.state.phase in ["validate", "complete"]


def test_assign_agent_mapping():
    user_state = UserState(phase="brainstorm_solution")
    coach = FeatureClarityCoach(initial_state=UserState())
    coach.kickoff(user_state.model_dump())
    assigned = coach.assign_agent()
    assert assigned == "brainstorm_solution_agent"


def test_run_agent_output_string():
    user_state = UserState(user_input="Let's validate this", phase="validate")
    coach = FeatureClarityCoach(initial_state=UserState())
    coach = FeatureClarityCoach(initial_state=UserState())
    response = coach.kickoff(user_state.model_dump())
    response_text = getattr(response, "output", str(response))
    assert isinstance(response_text, str)
    assert len(response_text.strip()) > 0
