import pytest
from environmental_ai_coach.crew import crew, interactive_session
from unittest.mock import patch, MagicMock
import sys
import os

# Get the absolute path to the src directory
src_path = os.path.abspath('/environmental_ai_coach/environmental_ai_coach/src/environmental_ai_coach')
# Add src to Python path
sys.path.append(src_path)

from fastapi.testclient import TestClient
from environmental_ai_coach.api import app
import pytest

client = TestClient(app)

@pytest.fixture
def mock_crew():
    # Mock the crew's kickoff method
    with patch('environmental_ai_coach.crew.Crew.kickoff') as mock_kickoff:
        mock_kickoff.return_value = "Mocked crew response"
        yield mock_kickoff

@pytest.fixture
def mock_tasks():
    # Mock the task outputs
    with patch('environmental_ai_coach.crew.research_task') as mock_research, \
         patch('environmental_ai_coach.crew.create_action_plan') as mock_action, \
         patch('environmental_ai_coach.crew.implement_gamification') as mock_gamification:
        
        # Setup mock output attributes
        mock_research.output = MagicMock()
        mock_research.output.raw = "Mocked research analysis"
        
        mock_action.output = MagicMock()
        mock_action.output.raw = "Mocked action plan"
        
        mock_gamification.output = MagicMock()
        mock_gamification.output.raw = """---QUIZ---
QUESTION: What is the most effective way to reduce your carbon footprint?
a) Drive more
b) Use public transportation
c) Leave lights on
d) Use single-use plastics
ANSWER: b
---END---"""
        
        yield (mock_research, mock_action, mock_gamification)

def test_crew_processing():
    """Test that the crew processes input correctly"""
    # Test input data
    test_input = {
        "user_input": "I want to reduce my carbon footprint",
        "location": "New York"
    }
    
    # Process the input through the crew
    result = crew.kickoff(test_input)
    
    # Assert that the crew returns a result
    assert result is not None
    
    # Check if all required agents are present
    assert len(crew.agents) == 3
    
    # Check if all required tasks are present
    assert len(crew.tasks) == 3

@pytest.mark.asyncio
async def test_interactive_session(mock_crew, mock_tasks, monkeypatch):
    """Test the interactive session flow"""
    # Mock user inputs
    inputs = iter(["New York", "I want to reduce my carbon footprint", "b", "quit()"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    # Mock print function to capture output
    printed_messages = []
    monkeypatch.setattr('builtins.print', lambda *args: printed_messages.append(' '.join(map(str, args))))
    
    # Run the interactive session
    interactive_session()
    
    # Verify the welcome message was printed
    assert any("Welcome to the Environmental AI Coach" in msg for msg in printed_messages)
    
    # Verify that the crew was called with correct inputs
    mock_crew.assert_called_once()
    
    # Verify that points were awarded for correct quiz answer
    assert any("Correct!" in msg for msg in printed_messages)

def test_crew_error_handling():
    """Test that the crew handles errors appropriately"""
    # Test with invalid input
    test_input = {
        "user_input": "",
        "location": ""
    }
    
    with pytest.raises(Exception):
        crew.kickoff(test_input)
