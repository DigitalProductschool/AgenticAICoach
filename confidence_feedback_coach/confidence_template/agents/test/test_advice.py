import os
import unittest
from dotenv import load_dotenv
import google.generativeai as genai

import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# absolute import
from agents.advice import ConfidenceAdviceAgent

load_dotenv()

class TestConfidenceAdviceAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
         # Use absolute path to training file
        self.training_file = os.path.join(
            project_root,
            'training',
            'advice_examples.json'
        )
        self.advice_agent = ConfidenceAdviceAgent(self.training_file)
        self.advisor = self.advice_agent.create_agent()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    def test_load_examples(self):
        """Test that the examples are loaded correctly."""
        self.assertIsNotNone(self.advice_agent.examples_content, "Examples content should not be None")
        self.assertNotEqual(self.advice_agent.examples_content, "", "Examples content should not be empty")
        print("Loaded Examples Content:\n", self.advice_agent.examples_content)

    def test_give_advice(self):
        """Test that the agent provides advice."""
        test_text = "I feel overwhelmed from the pressure at work and i constantly feel like i won't be able to execute my task"
        advice = self.advice_agent.give_advice(test_text)

        try:
            print("LLM Advice:\n", advice)
            self.assertIsNotNone(advice, "LLM advice should not be None")
            self.assertNotEqual(advice, "", "LLM advice should not be empty")
            #Add more assertion for a more concrete test
        except Exception as e:
            self.fail(f"LLM call failed: {e}")

if __name__ == '__main__':
    unittest.main()