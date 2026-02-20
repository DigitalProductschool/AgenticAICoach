import sys
import os

# Add the src directory to sys.path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/learning_pdf_agent')))

import unittest
from unittest.mock import patch, MagicMock
import tempfile
from crewai import Agent, LLM
from learning_pdf_agent.agent import create_learning_pdf_coach
from learning_pdf_agent.tools.pdf_search import load_data
from learning_pdf_agent.crew import create_learning_pdf_coach_crew

# Custom Mock Tool Class for Simulating PDF Search
class MockPDFSearchTool:
    """
    A mock class for simulating the behavior of PDFSearchTool during unit tests.
    This class mocks the functionality needed to simulate PDF search actions without using the actual tool.
    """
    def __init__(self, pdf, llm, embedder, verbose=True):
        self.name = "Mock PDF Search Tool"
        self.args = {"type": "mock"}  # Adding the required args attribute for LangChain compatibility
        self.description = "This is a mock tool for testing purposes."
        self.pdf = pdf
        self.llm = llm
        self.embedder = embedder
        self.verbose = verbose  # Added verbose parameter to match the actual implementation

    def to_langchain(self):
        """
        Simulate a method to provide a LangChain-compatible version of the tool.
        """
        return "LangChain-Compatible Mock Tool"

class TestLearningPDFCoach(unittest.TestCase):
    """
    Unit tests for the Learning PDF Coach agent and related functions.
    This class contains tests for agent creation, loading data, and interaction with Streamlit UI.
    """
    
    def setUp(self):
        """
        Set up common resources for each test, such as initializing the LLMs and creating mock tools.
        This method is called before every test case.
        """
        # Initialize language models for testing
        self.llm_gpt4 = LLM(
            model="gpt-4o",
            api_key="test_key",  # Placeholder API key
            temperature=0.2
        )
        self.embed_model = LLM(
            model="text-embedding-ada-002",
            api_key="test_key"  # Placeholder API key
        )

    @patch('learning_pdf_agent.agent.LLM')
    def test_create_learning_pdf_coach(self, MockLLM):
        """
        Test the creation of a Learning PDF Coach agent using a mock PDF search tool.
        Ensure that the agent is correctly instantiated with the provided tools.
        """
        mock_tool = MockPDFSearchTool(pdf="mock.pdf", llm=self.llm_gpt4, embedder=self.embed_model)
        
        # Create the agent using the mock tool
        tools = [mock_tool]
        agent = create_learning_pdf_coach(tools, self.llm_gpt4)
        
        # Assert that the agent is correctly instantiated
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.role, "Document Search Agent")
        self.assertTrue(agent.tools)  # Check that the agent has tools

    def test_load_data_with_valid_files(self):
        """
        Test the load_data function by providing valid PDF files.
        Ensure that the agent is created successfully with the mock PDF files.
        """
        # Create a temporary PDF file for testing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(b"Test PDF Content")  # Simulate writing PDF content
            tmp_file_path = tmp_file.name

        uploaded_files = [MagicMock()]  # Mock the uploaded file
        uploaded_files[0].getbuffer.return_value = b"Test PDF Content"

        # Patch the PDFSearchTool to use the mock version during this test
        with patch('learning_pdf_agent.tools.pdf_search.PDFSearchTool', new=MockPDFSearchTool):
            agent = load_data(uploaded_files)
            # Check that the agent was successfully created with valid tools
            self.assertIsNotNone(agent)

        # Clean up the temporary file
        os.remove(tmp_file_path)

    def test_load_data_with_no_files(self):
        """
        Test the load_data function when no files are uploaded.
        Ensure that no agent is created when there are no files.
        """
        uploaded_files = []  # No files provided
        agent = load_data(uploaded_files)
        # Assert that no agent is created
        self.assertIsNone(agent)

    @patch('learning_pdf_agent.crew.Task')  # Mock Task directly
    @patch('learning_pdf_agent.crew.Crew')
    def test_create_learning_pdf_coach_crew(self, MockCrew, MockTask):
        """
        Test the creation of a Crew using a mock agent and verify that the crew is set up with
        the expected tasks and agents.
        """
        mock_tool = MockPDFSearchTool(pdf="mock.pdf", llm=self.llm_gpt4, embedder=self.embed_model)
        agent = Agent(
            role="Mock Role",
            goal="Mock Goal",
            backstory="Mock backstory",
            tools=[mock_tool],
            llm=self.llm_gpt4
        )
        
        # Create the crew using the mock agent
        crew = create_learning_pdf_coach_crew(agent)
        
        # Ensure Crew was called
        self.assertTrue(MockCrew.called)

        # Check that the Task description and expected output match the expected values
        MockTask.assert_called_once_with(
            description="Use the tool 'Search a PDF's content' to find relevant information in the uploaded documents.",
            expected_output="A friendly, conversational response that answers the user's question based on the document content. Summarize it always to the key points.",
            agent=agent,
            verbose=True
        )

    @patch('streamlit.sidebar')
    @patch('streamlit.file_uploader')
    def test_streamlit_app_sidebar(self, mock_file_uploader, mock_sidebar):
        """
        Test the behavior of the Streamlit app's sidebar, including file upload functionality.
        Ensure that the sidebar's elements are called correctly when no files are uploaded.
        """
        mock_file_uploader.return_value = []  # Simulate no files uploaded
        mock_sidebar.return_value = None  # Simulate no sidebar button press

        from learning_pdf_agent.main import agentic_AI_coach
        agentic_AI_coach()

        # Assert that the file uploader was called correctly
        mock_file_uploader.assert_called_once_with("Upload documents", accept_multiple_files=True, type=['pdf'])

    @patch('learning_pdf_agent.tools.pdf_search.logging')
    def test_logging_no_documents(self, mock_logging):
        """
        Test the logging behavior when no documents are uploaded to the load_data function.
        Ensure that a warning is logged when no documents are processed.
        """
        load_data([])  # Call load_data with an empty list of files
        # Assert that the logging.warning method was called once with the correct message
        mock_logging.warning.assert_called_once_with("No documents found to process.")

if __name__ == '__main__':
    unittest.main()
