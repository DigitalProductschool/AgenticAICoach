import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

class TestPitchCoachAPI(unittest.TestCase):
    """Test cases for the AI Pitch Coach API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        
        # Create a mock for the PitchCoachFlow
        self.coaching_flow_patcher = patch('app.main.PitchCoachFlow')
        self.mock_coaching_flow = self.coaching_flow_patcher.start()
        
        # Create a mock instance
        self.mock_coach_instance = MagicMock()
        self.mock_coaching_flow.return_value = self.mock_coach_instance
        
        # Set up mock responses
        self.mock_coach_instance.start_conversation.return_value = "Let's work on your startup pitch!"
        self.mock_coach_instance.process_response.return_value = "That's a great start! Now, what's the core problem?"
        self.mock_coach_instance.get_investor_questions.return_value = "1. How do you plan to acquire customers?"
        self.mock_coach_instance.get_pitch_clarity_feedback.return_value = "Clarity & Simplicity: Your pitch is clear."
        self.mock_coach_instance._generate_complete_pitch.return_value = "Completed pitch text here."
        
        # Create a mock for the FeedbackTracker
        self.feedback_tracker_patcher = patch('app.main.FeedbackTracker')
        self.mock_feedback_tracker = self.feedback_tracker_patcher.start()
        
        # Create a mock instance
        self.mock_tracker_instance = MagicMock()
        self.mock_feedback_tracker.return_value = self.mock_tracker_instance
        
        # Set up mock responses
        self.mock_tracker_instance.add_pitch_feedback.return_value = "mock_pitch_id"
        
        # Create a mock for the CrewAI components
        self.crew_patcher = patch('app.main.PitchCoachCrew')
        self.mock_crew = self.crew_patcher.start()
        
        # Create a mock instance
        self.mock_crew_instance = MagicMock()
        self.mock_crew.return_value = self.mock_crew_instance
        
        # Set up mock responses
        self.mock_crew_instance.analyze_initial_pitch.return_value = "Analysis result"
        self.mock_crew_instance.simulate_investor_qa.return_value = "QA simulation result"
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.coaching_flow_patcher.stop()
        self.feedback_tracker_patcher.stop()
        self.crew_patcher.stop()
    
    def test_read_root(self):
        """Test the root endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to AI Pitch Coach API"})
    
    def test_start_session(self):
        """Test starting a coaching session"""
        response = self.client.post(
            "/start_session",
            json={"user_id": "test_user"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("session_id", data)
        self.assertEqual(data["welcome_message"], "Let's work on your startup pitch!")
        self.mock_coach_instance.start_conversation.assert_called_once()
    
    def test_send_message(self):
        """Test sending a message to the coach"""
        # We need to manually add a session first
        with patch('app.main.active_sessions', {
            "test_session_id": {
                "coach": self.mock_coach_instance,
                "user_id": "test_user",
                "created_at": 123456789
            }
        }):
            # Set current stage to not summary
            self.mock_coach_instance.current_stage = "problem"
            
            response = self.client.post(
                "/send_message",
                json={
                    "session_id": "test_session_id",
                    "message": "We're building an AI-powered resume optimizer.",
                    "user_id": "test_user"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["response"], "That's a great start! Now, what's the core problem?")
            self.assertFalse(data["is_pitch_complete"])
            self.assertIsNone(data["complete_pitch"])
            self.mock_coach_instance.process_response.assert_called_once_with(
                "We're building an AI-powered resume optimizer."
            )
    
    def test_send_message_pitch_complete(self):
        """Test sending a message that completes the pitch"""
        # We need to manually add a session first
        with patch('app.main.active_sessions', {
            "test_session_id": {
                "coach": self.mock_coach_instance,
                "user_id": "test_user",
                "created_at": 123456789
            }
        }):
            # Set current stage to summary
            self.mock_coach_instance.current_stage = "summary"
            
            response = self.client.post(
                "/send_message",
                json={
                    "session_id": "test_session_id",
                    "message": "Seeking $500K seed funding.",
                    "user_id": "test_user"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["response"], "That's a great start! Now, what's the core problem?")
            self.assertTrue(data["is_pitch_complete"])
            self.assertEqual(data["complete_pitch"], "Completed pitch text here.")
            self.mock_coach_instance.process_response.assert_called_once_with(
                "Seeking $500K seed funding."
            )
            self.mock_coach_instance._generate_complete_pitch.assert_called_once()
            self.mock_tracker_instance.add_pitch_feedback.assert_called_once()
    
    def test_session_action_qa(self):
        """Test performing a Q&A action"""
        # We need to manually add a session first
        with patch('app.main.active_sessions', {
            "test_session_id": {
                "coach": self.mock_coach_instance,
                "user_id": "test_user",
                "created_at": 123456789
            }
        }):
            response = self.client.post(
                "/session_action",
                json={
                    "session_id": "test_session_id",
                    "action": "qa",
                    "user_id": "test_user"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["action"], "qa")
            self.assertEqual(data["result"], "1. How do you plan to acquire customers?")
            self.mock_coach_instance.get_investor_questions.assert_called_once()
    
    def test_session_action_feedback(self):
        """Test performing a feedback action"""
        # We need to manually add a session first
        with patch('app.main.active_sessions', {
            "test_session_id": {
                "coach": self.mock_coach_instance,
                "user_id": "test_user",
                "created_at": 123456789
            }
        }):
            response = self.client.post(
                "/session_action",
                json={
                    "session_id": "test_session_id",
                    "action": "feedback",
                    "user_id": "test_user"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["action"], "feedback")
            self.assertEqual(data["result"], "Clarity & Simplicity: Your pitch is clear.")
            self.mock_coach_instance.get_pitch_clarity_feedback.assert_called_once()
    
    def test_analyze_pitch(self):
        """Test the analyze_pitch endpoint"""
        response = self.client.post(
            "/analyze_pitch",
            json={
                "pitch_content": "We're building an AI-powered resume optimizer.",
                "user_id": "test_user"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["pitch_id"], "mock_pitch_id")
        self.mock_crew_instance.analyze_initial_pitch.assert_called_once_with(
            "We're building an AI-powered resume optimizer."
        )
    
    def test_simulate_qa(self):
        """Test the simulate_qa endpoint"""
        response = self.client.post(
            "/simulate_qa",
            json={
                "pitch_content": "We're building an AI-powered resume optimizer.",
                "industry": "technology",
                "funding_stage": "seed",
                "user_id": "test_user"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["status"], "success")
        self.mock_crew_instance.simulate_investor_qa.assert_called_once_with(
            "We're building an AI-powered resume optimizer.",
            "technology",
            "seed"
        )


if __name__ == "__main__":
    unittest.main()