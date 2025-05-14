import os
import unittest
import sys
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from agents.corrector import ConfidenceCorrectorAgent
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class TestConfidenceCorrectorAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.training_file = os.path.join(
            project_root,
            'training',
            'corrector_examples.json'
        )
        self.corrector_agent = ConfidenceCorrectorAgent(self.training_file)
        self.corrector = self.corrector_agent.create_agent()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)

        # Directly use gemini-2.0-flash
        self.model_name = 'gemini-2.0-flash'
        self.model = genai.GenerativeModel(self.model_name)

    def test_load_examples(self):
        """Test that the examples are loaded correctly."""
        self.assertIsNotNone(self.corrector_agent.examples, "Examples should not be None")
        self.assertNotEqual(self.corrector_agent.examples, "", "Examples should not be empty")
        print("Loaded Examples:\n", self.corrector_agent.examples)  # Print loaded examples for inspection

    def test_correct_text(self):
        """Test that the agent provides a correction and that it is not empty."""
        test_text = "Just putting this out there, I believe it could be this method, i'm not sure"
        correction = self.corrector_agent.correct_text(test_text) # Get the LLM's correction

        try:
            print("LLM Correction:\n", correction)
            self.assertIsNotNone(correction, "LLM correction should not be None")
            self.assertNotEqual(correction, "", "LLM correction should not be empty")
        except Exception as e:
            self.fail(f"LLM call failed: {e}")

if __name__ == '__main__':
    unittest.main()