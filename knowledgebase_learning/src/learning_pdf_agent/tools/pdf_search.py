import logging
import tempfile
from crewai_tools import PDFSearchTool
from learning_pdf_agent.agent import create_learning_pdf_coach
from crewai import LLM
import os

def load_data(uploaded_files):
    """
    Processes the uploaded PDF files and creates instances of PDFSearchTool for each file.
    The function also initializes the language models (LLMs) needed for PDF content extraction 
    and document embedding. If tools are successfully created for the uploaded PDFs, an agent 
    is created and returned; otherwise, it returns None.

    Args:
        uploaded_files (list): List of uploaded PDF files from the user interface.

    Returns:
        Agent: Returns the initialized agent with tools if files are processed successfully.
        None: Returns None if no valid documents are processed.
    """
    tools = []  # List to hold the tools (PDFSearchTool) for each processed PDF
    
    # Initialize the language model (GPT-4)
    llm_gpt4o = LLM(
        model="gpt-4o",  # GPT-4 language model
        api_key=os.getenv("OPENAI_API_KEY"),  # API key fetched from environment variables
        temperature=0.2  # Controls the randomness of the language model output
    )

    # Initialize the embedding model (for text embeddings)
    embed_model = LLM(
        model="text-embedding-ada-002",  # Embedding model for document embeddings
        api_key=os.getenv("OPENAI_API_KEY")  # API key fetched from environment variables
    )

    # Process each uploaded PDF file
    if uploaded_files:
        logging.info("Processing uploaded PDF files.")
        for uploaded_file in uploaded_files:
            # Save the uploaded file to a temporary location on the server
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())  # Write file content to the temp file
                tmp_file_path = tmp_file.name  # Save the file path for the PDFSearchTool

            # Initialize the PDFSearchTool with the PDF file and language models
            pdf_tool = PDFSearchTool(
                pdf=tmp_file_path,  # Path to the temporary PDF file
                llm=llm_gpt4o,  # Language model for answering questions about the PDF
                embedder=embed_model,  # Embedding model for document searching
                verbose=True  # Enable verbose logging for tool usage
            )
            tools.append(pdf_tool)  # Add the tool to the list of tools

    # If tools are successfully created, return an agent
    if tools:
        # Create the agent using the tools and return it
        agent = create_learning_pdf_coach(tools, llm_gpt4o)
        return agent
    else:
        # Log a warning if no valid documents were processed
        logging.warning("No documents found to process.")
        return None
