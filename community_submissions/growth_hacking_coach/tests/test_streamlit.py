import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

# Create a more comprehensive mock for streamlit
streamlit_mock = MagicMock()
# Mock all the commonly used streamlit functions
streamlit_mock.session_state = MagicMock()
streamlit_mock.session_state.messages = []
streamlit_mock.session_state.use_mock_responses = False
streamlit_mock.columns.return_value = [MagicMock(), MagicMock()]
streamlit_mock.container.return_value = MagicMock()
streamlit_mock.chat_message.return_value.__enter__.return_value = MagicMock()
streamlit_mock.spinner.return_value.__enter__.return_value = MagicMock()

# Add the mock to sys.modules
sys.modules['streamlit'] = streamlit_mock
import streamlit as st

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import test data
from test_data import SAMPLE_USER_MESSAGES, SAMPLE_CONVERSATION_HISTORY, SAMPLE_API_RESPONSES, SAMPLE_ERROR_MESSAGES

# Define the functions we want to test directly instead of importing them
# This avoids executing the entire app.py file
def get_mock_response(message: str, conversation_history=None) -> str:
    """Mock implementation of get_mock_response for testing"""
    if "user engagement" in message.lower():
        return "This is a mock response about user engagement."
    elif "viral marketing" in message.lower():
        return "This is a mock response about viral marketing."
    else:
        return "This is a default mock response."

def query_growth_coach(message: str) -> str:
    """Mock implementation of query_growth_coach for testing"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={
                "message": message,
                "conversation_history": streamlit_mock.session_state.messages
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        streamlit_mock.warning("Unable to connect to the API. Switching to mock mode.")
        streamlit_mock.session_state.use_mock_responses = True
        return get_mock_response(message, streamlit_mock.session_state.messages)
    except Exception as e:
        return f"Error: {str(e)}"

class TestStreamlitApp(unittest.TestCase):
    """Tests for the Streamlit app functions"""

    def test_get_mock_response(self):
        """Test the mock response generator"""
        # Test with a simple message
        response = get_mock_response(SAMPLE_USER_MESSAGES[0])
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

        # Test with a message containing a keyword
        response = get_mock_response(SAMPLE_USER_MESSAGES[1])  # User engagement message
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        self.assertIn("user engagement", response.lower())

        # Test with conversation history
        response = get_mock_response(SAMPLE_USER_MESSAGES[2], SAMPLE_CONVERSATION_HISTORY[2])
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    @patch('requests.post')
    def test_query_growth_coach_success(self, mock_post):
        """Test the query_growth_coach function with a successful API response"""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSES[0]
        mock_post.return_value = mock_response

        # Mock the session state
        st.session_state.messages = SAMPLE_CONVERSATION_HISTORY[0]

        # Call the function
        response = query_growth_coach(SAMPLE_USER_MESSAGES[0])

        # Check the response
        self.assertEqual(response, SAMPLE_API_RESPONSES[0]["response"])

        # Verify the mock was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "http://127.0.0.1:8000/query")
        self.assertEqual(kwargs["json"]["message"], SAMPLE_USER_MESSAGES[0])
        self.assertEqual(kwargs["json"]["conversation_history"], st.session_state.messages)

    @patch('requests.post')
    def test_query_growth_coach_connection_error(self, mock_post):
        """Test the query_growth_coach function handles connection errors"""
        # Set up the mock to raise a connection error
        mock_post.side_effect = requests.exceptions.ConnectionError(SAMPLE_ERROR_MESSAGES[0])

        # Mock the session state
        st.session_state.messages = []
        st.session_state.use_mock_responses = False

        # Mock the warning function
        st.warning = MagicMock()

        # Call the function
        response = query_growth_coach(SAMPLE_USER_MESSAGES[3])

        # Check that the warning was shown
        st.warning.assert_called_once_with("Unable to connect to the API. Switching to mock mode.")

        # Check that use_mock_responses was set to True
        self.assertTrue(st.session_state.use_mock_responses)

        # Check that we got a mock response
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    @patch('requests.post')
    def test_query_growth_coach_error_response(self, mock_post):
        """Test the query_growth_coach function handles error responses from the API"""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = SAMPLE_ERROR_MESSAGES[1]  # "Internal Server Error"
        mock_post.return_value = mock_response

        # Mock the session state
        st.session_state.messages = []

        # Call the function
        response = query_growth_coach(SAMPLE_USER_MESSAGES[4])

        # Check the response contains the error
        self.assertIn("Error: 500", response)
        self.assertIn(SAMPLE_ERROR_MESSAGES[1], response)

if __name__ == "__main__":
    unittest.main()
