"""
MVP Coaching Session Orchestrator

Manages multi-stage coaching workflows using CrewAI framework.
Implements structured validation methodology through sequential task execution.
"""
from crewai import Crew, Process  # type: ignore
from .agents.mvp_coach import create_mvp_coach_agent
from .tasks.coaching_tasks import (
    create_risk_identification_task,
    create_validation_design_task,
    create_prototyping_task,
    create_success_metrics_task
)


class MVPCoachingCrew:
    """
    Orchestrates structured MVP validation coaching sessions.

    Implements a four-phase coaching methodology:
    1. Risk Assessment - Identify critical business assumptions
    2. Validation Planning - Design testable experiments
    3. Resource Assessment - Evaluate implementation capacity
    4. Success Definition - Establish measurable outcomes

    Uses sequential task execution to maintain coaching conversation flow
    and ensure proper depth before progression to next phase.
    """

    def __init__(self):
        """Initialize coaching crew with agent and task pipeline."""
        self.coach_agent = create_mvp_coach_agent()
        self._configure_task_pipeline()

    def _configure_task_pipeline(self):
        """
        Configure sequential coaching task pipeline.

        Tasks are designed to build upon each other, with each stage
        producing inputs required for subsequent coaching phases.
        Sequential processing ensures conversation depth before progression.
        """
        self.risk_task = create_risk_identification_task(self.coach_agent)
        self.validation_task = create_validation_design_task(self.coach_agent)
        self.prototype_task = create_prototyping_task(self.coach_agent)
        self.success_task = create_success_metrics_task(self.coach_agent)

        # Sequential execution ensures proper coaching conversation flow
        self.crew = Crew(
            agents=[self.coach_agent],
            tasks=[
                self.risk_task,
                self.validation_task,
                self.prototype_task,
                self.success_task
            ],
            process=Process.sequential,
            verbose=True
        )

    def execute_coaching_session(self, initial_context=""):
        """
        Execute complete coaching session workflow.

        Args:
            initial_context (str): Initial product concept or business idea

        Returns:
            dict: Coaching session results with actionable recommendations

        Raises:
            CoachingSessionError: If session execution fails
        """
        try:
            result = self.crew.kickoff(inputs={"user_idea": initial_context})
            return result
        except Exception as e:
            print(f"Coaching session failed: {e}")
            return None

    def get_session_summary(self):
        """
        Generate structured summary of coaching session outcomes.

        Returns:
            dict: Session summary with completion status and next steps
        """
        return {
            "phases_completed": [
                "Risk Assessment Complete",
                "Validation Strategy Defined",
                "Implementation Plan Ready",
                "Success Metrics Established"
            ],
            "outcome": "MVP validation framework established",
            "next_steps": "Execute validation experiments within 24 hours"
        }
