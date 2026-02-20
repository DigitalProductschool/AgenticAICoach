import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json
import tempfile
import shutil

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feedback_tracker import FeedbackTracker

class TestFeedbackTracker(unittest.TestCase):
    """Test cases for the FeedbackTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Patch the os.makedirs function to avoid creating directories
        self.makedirs_patcher = patch('os.makedirs')
        self.mock_makedirs = self.makedirs_patcher.start()
        
        # Patch open to avoid file operations
        self.open_patcher = patch('builtins.open', new_callable=mock_open, 
                               read_data='{"user_id": "test_user", "pitches": []}')
        self.mock_open = self.open_patcher.start()
        
        # Patch os.path.exists to control file existence checks
        self.exists_patcher = patch('os.path.exists', return_value=False)
        self.mock_exists = self.exists_patcher.start()
        
        # Test user ID
        self.user_id = "test_user"
        
        # Initialize tracker with patched dependencies
        self.tracker = FeedbackTracker(self.user_id)
        
        # Test data
        self.test_pitch = "We're building an AI-powered resume optimizer."
        self.test_feedback = "Great one-liner! Consider adding more specificity."
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.makedirs_patcher.stop()
        self.open_patcher.stop()
        self.exists_patcher.stop()
    
    def test_init_new_user(self):
        """Test initializing the tracker for a new user"""
        # Create a new tracker for a user that doesn't exist
        tracker = FeedbackTracker("new_user")
        
        # Check the feedback history initialization
        self.assertEqual(tracker.feedback_history["user_id"], "new_user")
        self.assertEqual(tracker.feedback_history["pitches"], [])
    
    def test_add_pitch_feedback_new_pitch(self):
        """Test adding feedback for a new pitch"""
        # Patch the save_feedback_history method to avoid file operations
        with patch.object(self.tracker, 'save_feedback_history'):
            # Add feedback for a new pitch
            pitch_id = self.tracker.add_pitch_feedback(self.test_pitch, self.test_feedback)
            
            # Check the result
            self.assertEqual(pitch_id, "1")  # First pitch should have ID "1"
            
            # Check the feedback was stored correctly
            self.assertEqual(len(self.tracker.feedback_history["pitches"]), 1)
            pitch = self.tracker.feedback_history["pitches"][0]
            self.assertEqual(pitch["pitch_id"], "1")
            self.assertEqual(pitch["iterations"][0]["pitch_content"], self.test_pitch)
            self.assertEqual(pitch["iterations"][0]["feedback"], self.test_feedback)
    
    def test_add_pitch_feedback_existing_pitch(self):
        """Test adding feedback for an existing pitch"""
        # Set up a test pitch in the feedback history
        pitch_id = "test_pitch_id"
        self.tracker.feedback_history["pitches"].append({
            "pitch_id": pitch_id,
            "created_at": "2023-01-01T00:00:00",
            "iterations": [{
                "timestamp": "2023-01-01T00:00:00",
                "pitch_content": self.test_pitch,
                "feedback": self.test_feedback
            }]
        })
        
        # Patch the save_feedback_history method to avoid file operations
        with patch.object(self.tracker, 'save_feedback_history'):
            # Add refinement feedback
            refined_pitch = self.test_pitch + " Our solution uses AI to optimize job applications."
            refined_feedback = "Much better! Now it's clearer what you do."
            
            # Update the same pitch
            updated_id = self.tracker.add_pitch_feedback(refined_pitch, refined_feedback, pitch_id)
            
            # Check the result
            self.assertEqual(updated_id, pitch_id)  # ID should remain the same
            
            # Check the feedback was stored correctly
            pitch = self.tracker.get_pitch_history(pitch_id)
            self.assertEqual(len(pitch["iterations"]), 2)
            self.assertEqual(pitch["iterations"][1]["pitch_content"], refined_pitch)
            self.assertEqual(pitch["iterations"][1]["feedback"], refined_feedback)
    
    def test_get_pitch_history(self):
        """Test retrieving a pitch's history"""
        # Set up a test pitch in the feedback history
        pitch_id = "test_pitch_id"
        self.tracker.feedback_history["pitches"].append({
            "pitch_id": pitch_id,
            "created_at": "2023-01-01T00:00:00",
            "iterations": [{
                "timestamp": "2023-01-01T00:00:00",
                "pitch_content": self.test_pitch,
                "feedback": self.test_feedback
            }]
        })
        
        # Get the history
        pitch_history = self.tracker.get_pitch_history(pitch_id)
        
        # Check the result
        self.assertEqual(pitch_history["pitch_id"], pitch_id)
        self.assertEqual(len(pitch_history["iterations"]), 1)
        self.assertEqual(pitch_history["iterations"][0]["pitch_content"], self.test_pitch)
        self.assertEqual(pitch_history["iterations"][0]["feedback"], self.test_feedback)
    
    def test_get_pitch_history_nonexistent(self):
        """Test retrieving history for a nonexistent pitch"""
        # Try to get history for a nonexistent pitch
        pitch_history = self.tracker.get_pitch_history("nonexistent_id")
        
        # Check the result
        self.assertIsNone(pitch_history)
    
    def test_get_all_pitches(self):
        """Test retrieving all pitches for a user"""
        # Set up test pitches in the feedback history
        self.tracker.feedback_history["pitches"] = [
            {
                "pitch_id": "pitch1",
                "created_at": "2023-01-01T00:00:00",
                "iterations": [{
                    "timestamp": "2023-01-01T00:00:00",
                    "pitch_content": self.test_pitch,
                    "feedback": self.test_feedback
                }]
            },
            {
                "pitch_id": "pitch2",
                "created_at": "2023-01-02T00:00:00",
                "iterations": [{
                    "timestamp": "2023-01-02T00:00:00",
                    "pitch_content": "Our app helps users create beautiful presentations.",
                    "feedback": "Good pitch but narrow down your target audience."
                }]
            }
        ]
        
        # Get all pitches
        all_pitches = self.tracker.get_all_pitches()
        
        # Check the result