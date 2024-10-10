import streamlit as st
import logging
import os
from agent import create_learning_pdf_coach
from tools.pdf_search import load_data
from crew import create_learning_pdf_coach_crew  # Import the Crew creation function

# Setup logging to direct output to terminal
logging.basicConfig(level=logging.INFO)

def agentic_AI_coach():
    """
    Main function to run the Learning PDF Coach application using Streamlit.
    Manages user interactions, file uploads, and chat-based question answering using the created agent.
    Follows the Thought-Action-Observation structure and preserves context across questions.
    """
    st.header("Learning PDF Coach")

    # Initialize session state for chat history, agent, and crew
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about your documents!"}
        ]
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "crew" not in st.session_state:
        st.session_state.crew = None  # Store the crew for continued context

    # Sidebar for file upload and document processing
    with st.sidebar:
        uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True, type=['pdf'])
        if st.button("Process"):
            try:
                st.sidebar.info("Processing your documents. This might take a while for large files.")
                agent_created = load_data(uploaded_files)  # Load documents and create an agent
                if agent_created:
                    st.session_state.agent = agent_created
                    st.sidebar.success("Documents processed successfully. You can now ask your questions.")
                    # Create crew only once after processing documents
                    st.session_state.crew = create_learning_pdf_coach_crew(st.session_state.agent)
                else:
                    st.sidebar.warning("No valid documents uploaded.")
            except Exception as e:
                logging.error(f"Error processing documents: {e}")
                st.sidebar.error("An error occurred while processing the documents. Please check the logs.")

    # If the agent is initialized, display chat interface
    if st.session_state.agent:
        # Display previous conversation messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Get user input via chat interface
        if prompt := st.chat_input("Your question"):
            st.session_state.messages.append({"role": "user", "content": prompt})  # Save user's message

            # Display user's message in the chat
            with st.chat_message("user"):
                st.write(prompt)

            # Preserve conversation history to provide context for the agent
            conversation_history = "\n".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "assistant"])
            prompt_with_history = f"{conversation_history}\n{prompt}"

            # Process the user's question using the existing CrewAI agent
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Reuse the existing crew, if it hasn't been created
                        if st.session_state.crew is None:
                            st.session_state.crew = create_learning_pdf_coach_crew(st.session_state.agent)

                        # Kickoff the task execution with the user's question and conversation history
                        assistant_response = st.session_state.crew.kickoff(inputs={"user_question": prompt_with_history})

                        # Parse the response (can be a dict with output and intermediate steps)
                        if isinstance(assistant_response, dict):
                            if 'output' in assistant_response:
                                response = assistant_response['output']
                            else:
                                response = "No output found"
                            
                            # Display intermediate steps, if available (Thought-Action-Observation format)
                            if 'intermediate_steps' in assistant_response:
                                st.markdown("### Task Execution Details")
                                for step in assistant_response['intermediate_steps']:
                                    st.markdown(f"#### Thought: {step['thought']}")
                                    st.markdown(f"**Action**: {step['action']}")
                                    st.markdown(f"**Action Input**: {step['input']}")
                                    st.markdown(f"**Observation**: {step['output']}")

                        else:
                            # If the response is not a dict, it's the final response string
                            response = assistant_response

                        # Display the final answer in the chat
                        st.markdown(f"### Final Answer:\n{response}")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        logging.error(f"Error during task execution: {e}")
                        st.error("An error occurred while processing your request. Please try again.")
    else:
        # If agent is not ready, prompt the user to upload documents
        if len(st.session_state.messages) > 1:
            st.write("Please upload documents to proceed.")
        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

if __name__ == "__main__":
    agentic_AI_coach()
