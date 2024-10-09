from crewai import Agent, LLM

def create_learning_pdf_coach(tools, llm_gpt4o):
    """
    Creates a learning PDF coach agent responsible for searching through PDF documents and
    answering user questions based on the contents of those documents.

    Args:
        tools (list): List of tools that the agent will use, such as PDFSearchTool for document searching.
        llm_gpt4o (LLM): The language model instance (e.g., GPT-4) that the agent uses for generating responses.

    Returns:
        Agent: The initialized agent configured to handle PDF search tasks and respond to user queries.
    """
    return Agent(
        role="Document Search Agent",  # The agent's role, defining its core function
        goal="Search through all uploaded documents to find relevant answers.",  # The agent's primary goal
        backstory="An agent adept at searching and extracting data from multiple documents.",  # Agent's background story
        tools=tools,  # List of tools the agent uses to complete tasks
        max_execution_time=300,  # Maximum time (in seconds) allowed for task execution, set to 5 minutes
        verbose=True,  # Enable detailed logging for better insight into agent behavior and debugging
        llm=llm_gpt4o  # The language model (LLM) used for generating answers based on document content
    )
