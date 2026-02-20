import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.coaching_flow import PitchCoachFlow

class TestPitchCoachFlow(unittest.TestCase):
    """Test cases for the PitchCoachFlow class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the ChatOpenAI instance
        self.llm_patcher = patch('utils.coaching_flow.ChatOpenAI')
        self.mock_llm = self.llm_patcher.start()
        
        # Create a mock LLM response
        self.mock_llm_instance = MagicMock()
        self.mock_llm.return_value = self.mock_llm_instance
        
        # Create a mock response content
        self.mock_response = MagicMock()
        self.mock_response.content = "This is a mock response from the LLM"
        self.mock_llm_instance.invoke.return_value = self.mock_response
        
        # Initialize the coaching flow
        self.coach = PitchCoachFlow()
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.llm_patcher.stop()
    
    def test_start_conversation(self):
        """Test that the conversation starts with a welcome message"""
        welcome_message = self.coach.start_conversation()
        self.assertIn("work on your startup pitch", welcome_message.lower())
        self.assertEqual(self.coach.current_stage, "one_liner")
        self.assertEqual(len(self.coach.history), 1)
        self.assertEqual(self.coach.history[0]["speaker"], "coach")
    
def test_process_response_one_liner(self):
    """Test processing a response for the one-liner stage"""
    # Start the conversation (which adds the first coach message to history)
    self.coach.start_conversation()
    
    # Now the history should have one entry from the coach
    self.assertEqual(len(self.coach.history), 1)
    self.assertEqual(self.coach.history[0]["speaker"], "coach")
    
    # Process the user's one-liner
    response = self.coach.process_response("We're building an AI-powered resume optimizer.")
    
    # Now the history should have two entries (coach, user)
    self.assertEqual(len(self.coach.history), 3)  # Initial coach + user response + coach reply
    self.assertEqual(self.coach.history[0]["speaker"], "coach")  # Initial welcome message
    self.assertEqual(self.coach.history[1]["speaker"], "user")   # User's one-liner
    self.assertEqual(self.coach.history[2]["speaker"], "coach")  # Coach's response
    
    # Verify the one-liner was stored
    self.assertEqual(self.coach.pitch_components["one_liner"], 
                     "We're building an AI-powered resume optimizer.")
    
    # Verify the next stage is set to problem
    self.assertEqual(self.coach.current_stage, "problem")
    
    def test_process_response_problem(self):
        """Test processing a response for the problem stage"""
        # Set up the initial state
        self.coach.current_stage = "problem"
        self.coach.pitch_components["one_liner"] = "We're building an AI-powered resume optimizer."
        
        # Process the user's problem statement
        response = self.coach.process_response("Job seekers struggle to get past ATS systems.")
        
        # Verify the problem was stored
        self.assertEqual(self.coach.pitch_components["problem"], 
                         "Job seekers struggle to get past ATS systems.")
        
        # Verify the next stage is set
        self.assertEqual(self.coach.current_stage, "solution")
        
        # LLM should have been called to generate feedback
        self.mock_llm_instance.invoke.assert_called_once()
    
    def test_generate_complete_pitch(self):
        """Test generating a complete pitch"""
        # Set up pitch components
        self.coach.pitch_components = {
            "one_liner": "We're building an AI-powered resume optimizer.",
            "problem": "Job seekers struggle to get past ATS systems.",
            "solution": "Our AI analyzes job descriptions and optimizes resumes.",
            "market": "Recent college graduates and job changers.",
            "business_model": "SaaS subscription model $15/month.",
            "unique_value": "Real-time feedback and optimization suggestions.",
            "traction": "500 beta users with 70% improved interview rates.",
            "team": "Former HR tech professionals with ML expertise.",
            "ask": "Seeking $500K seed funding."
        }
        
        # Generate the complete pitch
        pitch = self.coach._generate_complete_pitch()
        
        # Verify all components are in the pitch
        for component, value in self.coach.pitch_components.items():
            if value and value.strip():
                self.assertIn(value, pitch)
    
    def test_get_investor_questions(self):
        """Test generating investor questions"""
        # Set up pitch components
        self.coach.pitch_components = {
            "one_liner": "We're building an AI-powered resume optimizer.",
            "problem": "Job seekers struggle to get past ATS systems."
        }
        
        # Mock the LLM response for this specific call
        mock_questions = "1. How do you plan to acquire customers?\nTip: Focus on channels."
        mock_response = MagicMock()
        mock_response.content = mock_questions
        self.mock_llm_instance.invoke.return_value = mock_response
        
        # Get investor questions
        questions = self.coach.get_investor_questions()
        
        # Verify the result
        self.assertEqual(questions, mock_questions)
        self.mock_llm_instance.invoke.assert_called_once()

    def test_get_pitch_clarity_feedback(self):
        """Test generating pitch clarity feedback"""
        # Set up pitch components
        self.coach.pitch_components = {
            "one_liner": "We're building an AI-powered resume optimizer.",
            "problem": "Job seekers struggle to get past ATS systems."
        }
        
        # Mock the LLM response for this specific call
        mock_feedback = "Clarity & Simplicity: Your pitch is clear."
        mock_response = MagicMock()
        mock_response.content = mock_feedback
        self.mock_llm_instance.invoke.return_value = mock_response
        
        # Get pitch clarity feedback
        feedback = self.coach.get_pitch_clarity_feedback()
        
        # Verify the result
        self.assertEqual(feedback, mock_feedback)
        self.mock_llm_instance.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()