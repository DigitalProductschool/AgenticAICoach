import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os
import json

# Add the src directory to the path so we can import the API
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the API
from growth_hacking_coach.api import app

# Import test data
from test_data import SAMPLE_USER_MESSAGES, SAMPLE_CONVERSATION_HISTORY, SAMPLE_API_RESPONSES, SAMPLE_ERROR_MESSAGES

# Create a test client
client = TestClient(app)

class TestGrowthHackingCoachAPI(unittest.TestCase):
    """Tests for the Growth Hacking Coach API"""

    def test_read_root(self):
        """Test the root endpoint returns a welcome message"""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the Growth Hacking & Viral Marketing Coach API"})

    @patch('growth_hacking_coach.api.GrowthHackingCrew')
    def test_query_endpoint(self, mock_crew_class):
        """Test the query endpoint with a mock crew"""
        # Set up the mock
        mock_crew_instance = MagicMock()
        mock_crew = MagicMock()
        mock_crew_instance.crew.return_value = mock_crew
        mock_crew_class.return_value = mock_crew_instance

        # Mock the kickoff method to return a result
        mock_result = MagicMock()
        mock_result.raw = SAMPLE_API_RESPONSES[0]["response"]
        mock_crew.kickoff.return_value = mock_result

        # Test data
        test_data = {
            "message": SAMPLE_USER_MESSAGES[0],
            "conversation_history": SAMPLE_CONVERSATION_HISTORY[0]
        }

        # Make the request
        response = client.post("/query", json=test_data)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": SAMPLE_API_RESPONSES[0]["response"]})

        # Verify the mock was called correctly
        mock_crew_class.assert_called_once()
        mock_crew_instance.crew.assert_called_once()
        mock_crew.kickoff.assert_called_once()

        # Check that the kickoff method was called with the correct inputs
        call_args = mock_crew.kickoff.call_args[1]
        self.assertIn('inputs', call_args)
        self.assertIn('user_message', call_args['inputs'])
        self.assertEqual(call_args['inputs']['user_message'], SAMPLE_USER_MESSAGES[0])
        self.assertIn('conversation_history', call_args['inputs'])

    @patch('growth_hacking_coach.api.GrowthHackingCrew')
    def test_query_endpoint_with_error(self, mock_crew_class):
        """Test the query endpoint handles errors correctly"""
        # Set up the mock to raise an exception
        mock_crew_instance = MagicMock()
        mock_crew = MagicMock()
        mock_crew_instance.crew.return_value = mock_crew
        mock_crew_class.return_value = mock_crew_instance
        mock_crew.kickoff.side_effect = Exception(SAMPLE_ERROR_MESSAGES[0])

        # Test data
        test_data = {
            "message": SAMPLE_USER_MESSAGES[1],
            "conversation_history": []
        }

        # Make the request and expect an HTTP error
        response = client.post("/query", json=test_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], SAMPLE_ERROR_MESSAGES[0])

if __name__ == "__main__":
    unittest.main()
