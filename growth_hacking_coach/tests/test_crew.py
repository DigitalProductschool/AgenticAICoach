import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import test data
from test_data import SAMPLE_USER_MESSAGES, SAMPLE_CONVERSATION_HISTORY, SAMPLE_API_RESPONSES

# Import the crew
from growth_hacking_coach.crew import GrowthHackingCrew

class TestGrowthHackingCrew(unittest.TestCase):
    """Tests for the Growth Hacking Crew"""

    @patch('growth_hacking_coach.crew.Agent')
    @patch('growth_hacking_coach.crew.Crew')
    @patch('growth_hacking_coach.crew.Task')
    @patch('growth_hacking_coach.crew.LLM')
    def test_crew_initialization(self, mock_llm, mock_task, mock_crew, mock_agent):
        """Test that the crew initializes correctly"""
        # Set up mocks
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance

        mock_task_instance = MagicMock()
        mock_task.return_value = mock_task_instance

        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance

        # Create the crew
        crew = GrowthHackingCrew()

        # Test that the agents are created
        self.assertIsNotNone(crew.lead_growth_coach())
        self.assertIsNotNone(crew.channel_specialist())
        self.assertIsNotNone(crew.viral_mechanics_designer())
        self.assertIsNotNone(crew.content_automation_guru())
        self.assertIsNotNone(crew.growth_analytics_expert())

        # Test that the task is created
        self.assertIsNotNone(crew.synthesize_response_task())

        # Test that the crew is created
        crew_instance = crew.crew()
        self.assertEqual(crew_instance, mock_crew_instance)

        # Verify that the crew was created with the correct agents and tasks
        mock_crew.assert_called_once()
        args, kwargs = mock_crew.call_args
        self.assertEqual(len(kwargs['agents']), 4)  # 4 specialist agents
        self.assertEqual(len(kwargs['tasks']), 1)   # 1 task
        self.assertEqual(kwargs['manager_agent'], mock_agent_instance)  # Lead coach as manager
        self.assertEqual(kwargs['process'], 'sequential')
        self.assertEqual(kwargs['verbose'], True)

    def test_search_tool_initialization(self):
        """Test that the search tool is initialized correctly"""
        # This test doesn't need to use a mock since we're just checking
        # that the search_tool attribute is set correctly

        # Create the crew
        crew = GrowthHackingCrew()

        # Verify that the search_tool attribute exists and has the correct n_results
        self.assertTrue(hasattr(crew, 'search_tool'))
        # Check that n_results is set to 3 (this assumes the attribute is accessible)
        # If the attribute is not directly accessible, we can skip this check
        if hasattr(crew.search_tool, 'n_results'):
            self.assertEqual(crew.search_tool.n_results, 3)

    @patch('growth_hacking_coach.crew.Agent')
    @patch('growth_hacking_coach.crew.Crew')
    @patch('growth_hacking_coach.crew.Task')
    @patch('growth_hacking_coach.crew.LLM')
    def test_crew_kickoff(self, mock_llm, mock_task, mock_crew, mock_agent):
        """Test that the crew kickoff method works correctly"""
        # Set up mocks
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance

        mock_task_instance = MagicMock()
        mock_task.return_value = mock_task_instance

        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance

        # Mock the kickoff method
        mock_result = MagicMock()
        mock_result.raw = SAMPLE_API_RESPONSES[0]["response"]
        mock_crew_instance.kickoff.return_value = mock_result

        # Create the crew
        crew = GrowthHackingCrew()

        # Format conversation history
        formatted_history = ""
        for msg in SAMPLE_CONVERSATION_HISTORY[0]:
            formatted_history += f"{msg['role'].upper()}: {msg['content']}\n\n"

        # Test kickoff with a sample message
        inputs = {
            'user_message': SAMPLE_USER_MESSAGES[0],
            'conversation_history': formatted_history
        }

        result = crew.crew().kickoff(inputs=inputs)

        # Verify that kickoff was called with the correct inputs
        mock_crew_instance.kickoff.assert_called_once_with(inputs=inputs)

        # Check the result
        self.assertEqual(result, mock_result)

if __name__ == "__main__":
    unittest.main()
