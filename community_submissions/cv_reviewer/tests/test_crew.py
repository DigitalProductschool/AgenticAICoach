import pytest
from unittest.mock import patch, MagicMock
from src.schemas.cv_output import CVReview
from src.utils.agent_helper import run_cv_review_crew
from crewai import CrewOutput

@pytest.fixture
def mock_crew_output():
    """
    Creates a mock Pydantic CVReview object and wraps it in a mock CrewOutput.
    This simulates the expected successful result from a crew.kickoff() call.
    """
    # 1. Create an instance of our Pydantic model with sample data
    mock_pydantic_result = CVReview(
        overall_score="8.5/10",
        score_justification="A strong CV with clear, quantifiable achievements.",
        cv_analysis="The CV is well-structured and uses strong action verbs. However, the summary could be more concise.",
        technical_analysis="No GitHub repositories were provided for analysis.",
        actionable_suggestions=[
            "Condense the professional summary into 2-3 impactful sentences.",
            "Add a link to your live project portfolio."
        ],
        suggested_job_roles=[
            "Senior Software Engineer",
            "Full-Stack Developer"
        ]
    )

    mock_output = MagicMock(spec=CrewOutput)
    mock_output.pydantic = mock_pydantic_result
    
    return mock_output

def test_run_cv_review_crew_with_no_github_urls(mock_crew_output):
    """
    Tests the run_cv_review_crew function to ensure it correctly calls the crew
    and returns a valid, structured Pydantic model when given zero GitHub URLs.
    """
    sample_cv_text = "This is a sample CV."
    github_urls = []

    # Intercept the crew's kickoff method to return our mock output
    with patch('src.cv_reviewer.crew.Crew.kickoff', return_value=mock_crew_output) as mock_kickoff:
        
        # --- ACT ---
        # Call the function we are testing
        result = run_cv_review_crew(sample_cv_text, github_urls)

        # --- ASSERT ---
        # 1. Assert that the crew's kickoff method was actually called once
        mock_kickoff.assert_called_once()
        
        # 2. Assert that the result from our helper function is the mocked output we defined
        assert result == mock_crew_output

        # 3. Assert that the result contains a pydantic object
        assert hasattr(result, 'pydantic')
        assert result.pydantic is not None
        
        # 4. Assert that the pydantic object is an instance of our CVReview model
        assert isinstance(result.pydantic, CVReview)

        # 5. Assert that the content of the Pydantic model is correct
        assert result.pydantic.overall_score == "8.5/10"
        assert "No GitHub repositories were provided for analysis." in result.pydantic.technical_analysis

