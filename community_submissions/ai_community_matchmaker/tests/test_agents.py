import unittest
import os
from unittest.mock import patch, MagicMock
from src.ai_community_matchmaker.crew import AiCommunityMatchmaker
from crewai import Agent

class TestAgents(unittest.TestCase):
    @classmethod
    @patch('embedchain.embedder.openai.OpenAIEmbedder', new=MagicMock())
    def setUpClass(cls):
        """
        Set up shared resources for the test case.
        """
        os.environ["OPENAI_API_KEY"] = "test_key"
        os.environ["OPENAI_MODEL"] = "text-embedding-ada-mock"  # Use a mock model
        cls.matchmaker = AiCommunityMatchmaker()  # Instantiate the class
        cls.crew = cls.matchmaker.crew()
        
    def test_cofounder_search_agent_creation(self):
        """
        Test the creation and initialization of the Cofounder Search agent.
        """
        agent = self.matchmaker.cofounder_search_agent()
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.role.strip(), "Cofounder Search Agent")

    def test_mentor_search_agent_creation(self):
        """
        Test the creation and initialization of the Mentor Search agent.
        """
        agent = self.matchmaker.mentor_search_agent()
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.role.strip(), "Mentor Search Agent")
    
    def test_community_matching_coach_creation(self):
        """
        Test the creation and initialization of the Mentor Search agent.
        """
        agent = self.matchmaker.community_matching_coach()
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.role.strip(), "Community Matching Coach")

    def test_crew_initialization(self):
        """
        Test that the crew is initialized correctly with agents and tasks.
        """
        self.assertIsNotNone(self.crew)
        self.assertEqual(len(self.crew.agents), 3)
        self.assertEqual(len(self.crew.tasks), 3)

if __name__ == "__main__":
    unittest.main()