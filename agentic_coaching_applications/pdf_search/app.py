import streamlit as st
import logging
import tempfile
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import PDFSearchTool
import nest_asyncio
from dotenv import load_dotenv

# Apply nest_asyncio
nest_asyncio.apply()
# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

def agentic_PDF_coach():
    st.header("Agentic PDF Coach")

    # Initialize session state for chat history and agent
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about your documents!"}
        ]
    if "agent" not in st.session_state:
        st.session_state.agent = None

    # Initialize the language model using OpenAI GPT-4
    llm_gpt4 = LLM(
        model="gpt-3.5-turbo",   #gpt-4
        api_key=os.getenv("OPENAI_API_KEY"),  # Get API key from environment variables
        temperature=0.2  # Adjust temperature as needed
    )

    # Initialize the embedding model
    embed_model = LLM(
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    with st.sidebar:
        uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True, type=['pdf'])

        if st.button("Process"):
            st.session_state.agent_created = load_data(uploaded_files, llm_gpt4, embed_model)

    if st.session_state.agent:
        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Get user input
        if prompt := st.chat_input("Your question"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user's message
            with st.chat_message("user"):
                st.write(prompt)

            # Process the user's question using the CrewAI agent
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Create a Task for the user's question
                        task = Task(
                            description=f"Use the available tools to find relevant information in the documents.\nBased on this information, answer the following question:\n{prompt}",
                            expected_output="A clear and concise answer to the user's question. At the end ask the user a follow-up question to continue the conversation. Remember you are a coach helping the user understand her document deeper. ",
                            agent=st.session_state.agent
                        )
                        # Create a Crew with the agent and task
                        crew = Crew(
                            agents=[st.session_state.agent],
                            tasks=[task],
                            process=Process.sequential
                        )
                        # Execute the task
                        assistant_response = crew.kickoff(inputs={"user_question": prompt})
                        # Display the result
                        st.markdown(assistant_response)
                        # Append assistant's response to messages
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    except Exception as e:
                        logging.error(f"Error during task execution: {e}")
                        st.write("An error occurred while processing your request. Please try again.")
    else:
        if len(st.session_state.messages) > 1:
            st.write("Please upload documents to proceed.")
        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

def load_data(uploaded_files, llm_gpt4, embed_model):
    tools = []
    if uploaded_files:
        logging.info("Processing uploaded PDF files.")
        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name
                # Initialize PDFSearchTool with the specific PDF
                pdf_tool = PDFSearchTool(
                    pdf=tmp_file_path,
                    llm=llm_gpt4,
                    embedder=embed_model
                )
                tools.append(pdf_tool)
    if tools:
        # Create the agent with GPT-4
        agent = Agent(
            role="Document Search Agent",
            goal="Search through all uploaded documents to find relevant answers",
            backstory="An agent adept at searching and extracting data from multiple documents. The agent is a coach helping the user understand her document deeper.",
            tools=tools,
            verbose=True,
            llm=llm_gpt4
        )
        st.session_state.agent = agent
        return True
    else:
        logging.warning("No documents found to process.")
        return False

# Run the Agentic AI Coach app
if __name__ == "__main__":
    agentic_PDF_coach()