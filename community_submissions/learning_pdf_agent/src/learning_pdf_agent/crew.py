from crewai import Crew, Process, Task
from agent import create_learning_pdf_coach

def create_learning_pdf_coach_crew(agent):
    """
    Creates a Crew for handling PDF-based tasks using the provided agent.
    Captures and logs detailed steps of tool usage and task execution in the
    Thought-Action-Observation format.

    Args:
        agent (Agent): The agent responsible for processing user questions.

    Returns:
        Crew: Initialized Crew that can be kicked off to execute tasks.
    """
    
    # Define the task for the agent, specifying that it should use the PDF search tool.
    # The description should guide the agent on what actions to perform.
    task = Task(
        description="Use the tool 'Search a PDF's content' to find relevant information in the uploaded documents.",
        expected_output="A friendly, conversational response that answers the user's question based on the document content. Summarize it always to the key points.",
        agent=agent,
        verbose=True  # Enable verbose logging to capture each step of the task execution
    )

    # Create and return a Crew instance that manages the execution of tasks sequentially.
    # The Crew orchestrates the agent's actions according to the defined task.
    return Crew(
        agents=[agent],          # List of agents involved in the task execution
        tasks=[task],            # List of tasks that the agent should complete
        process="sequential",    # Define the process to execute tasks sequentially
        enforce_action_names=True  # Ensure that the action name is explicitly used in the task
    )
