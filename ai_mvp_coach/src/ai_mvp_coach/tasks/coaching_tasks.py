"""
Coaching Task Factory Module

Defines structured coaching workflows for MVP validation methodology.
Each task represents a distinct phase in lean startup validation process.
"""
from crewai import Task  # type: ignore


def create_risk_identification_task(agent):
    """
    Risk Assessment Phase Task Factory

    Creates task for identifying critical business assumptions requiring validation.
    Implements systematic assumption discovery through structured questioning.

    Args:
        agent: Configured coaching agent for task execution

    Returns:
        Task: Risk identification coaching task
    """
    return Task(
        description="""Conduct systematic risk assessment to identify critical business assumptions.

        METHODOLOGY:
        1. Analyze core value proposition components
        2. Identify uncertainty areas with highest business impact
        3. Isolate assumptions that invalidate entire concept if false
        4. Maintain single-question interaction pattern

        ASSESSMENT FRAMEWORK:
        - Core functionality viability
        - Market demand validation requirements
        - Technical feasibility assumptions
        - Business model sustainability factors

        DELIVERABLE: Prioritized critical assumption requiring immediate validation""",

        agent=agent,
        expected_output="""Specific, testable business assumption identified as highest priority
                         for validation. Must be fundamental to product success and measurable
                         through rapid experimentation."""
    )


def create_validation_design_task(agent):
    """
    Experiment Design Phase Task Factory

    Creates task for designing rapid validation experiments.
    Focuses on minimal viable experiments with clear success criteria.

    Args:
        agent: Configured coaching agent for task execution

    Returns:
        Task: Validation experiment design task
    """
    return Task(
        description="""Design rapid validation experiments for identified critical assumptions.

        EXPERIMENT DESIGN PRINCIPLES:
        1. Convert assumption into falsifiable hypothesis
        2. Design multiple validation approaches for triangulation
        3. Optimize for speed and cost constraints (12-24 hour execution)
        4. Ensure clear, measurable outcomes

        VALIDATION APPROACHES:
        - Customer interview protocols
        - Landing page conversion tests
        - Prototype feedback sessions
        - Market research validation

        DELIVERABLE: Portfolio of 3 distinct validation experiments with execution plans""",

        agent=agent,
        expected_output="""Three distinct validation experiments, each containing:
                         1. Clear hypothesis being tested
                         2. Execution methodology within 24-hour constraint
                         3. Resource requirements and costs
                         4. Success/failure criteria definition"""
    )


def create_prototyping_task(agent):
    """
    Resource Assessment Phase Task Factory

    Creates task for evaluating implementation capacity and defining minimal viable prototype.
    Focuses on leveraging existing resources for rapid validation.

    Args:
        agent: Configured coaching agent for task execution

    Returns:
        Task: Resource assessment and prototyping task
    """
    return Task(
        description="""Assess available resources and define minimal viable prototype strategy.

        RESOURCE EVALUATION:
        1. Inventory existing technical capabilities and tools
        2. Assess time and budget constraints for prototype development
        3. Identify skill gaps and external dependencies
        4. Define minimum viable implementation scope

        PROTOTYPE STRATEGY:
        - Leverage existing platforms and frameworks
        - Focus on core assumption testing functionality
        - Minimize custom development requirements
        - Ensure rapid iteration capability

        DELIVERABLE: Executable prototype plan matching available resources""",

        agent=agent,
        expected_output="""Detailed prototype implementation plan including:
                         1. Resource utilization strategy
                         2. Development scope and timeline
                         3. Technical architecture decisions
                         4. Risk mitigation for execution barriers"""
    )


def create_success_metrics_task(agent):
    """
    Success Criteria Definition Phase Task Factory

    Creates task for establishing measurable validation thresholds and next steps.
    Ensures actionable outcomes from validation experiments.

    Args:
        agent: Configured coaching agent for task execution

    Returns:
        Task: Success criteria and next steps definition task
    """
    return Task(
        description="""Define measurable success criteria and establish post-validation workflow.

        SUCCESS CRITERIA FRAMEWORK:
        1. Establish quantitative validation thresholds
        2. Define qualitative indicators of assumption validation
        3. Create decision matrix for experiment outcomes
        4. Plan iteration strategy based on results

        OUTCOME PLANNING:
        - Success: scaling and expansion strategies
        - Failure: pivot options and assumption refinement
        - Mixed results: additional validation requirements
        - Execution barriers: resource reallocation strategies

        DELIVERABLE: Comprehensive validation framework with clear next steps""",

        agent=agent,
        expected_output="""Structured validation framework containing:
                         1. Quantitative success thresholds for each experiment
                         2. Qualitative validation indicators
                         3. Decision tree for post-experiment actions
                         4. Timeline for validation execution and review"""
    )
