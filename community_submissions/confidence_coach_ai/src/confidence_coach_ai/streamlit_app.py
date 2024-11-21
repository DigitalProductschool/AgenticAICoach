#CHAT UI
import streamlit as st
import requests
import uuid
from datetime import datetime

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Custom CSS to expand containers
st.markdown("""
    <style>
        /* Base styles */
        .main > div {
            min-height: 100vh;
            background-color: #1e1e1e;  /* Dark background */
            color: white !important;
        }
        
        /* Container styling */
        .block-container {
            padding: 2rem 2rem 0 2rem !important;  /* Added right padding */
            max-width: 100% !important;
        }
        
        /* Column styling */
        [data-testid="column"] {
            height: calc(100vh - 100px);
            overflow-y: auto;
            background-color: #2d2d2d;  /* Dark background for columns */
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.2);
            padding: 1.5rem;
            color: white !important;
        }

        /* Analysis column specific */
        [data-testid="column"]:first-child {
            margin-right: 1.5rem;
        }

        /* Chat column specific */
        [data-testid="column"]:last-child {
            padding: 0;
            border-radius: 12px;        
            display: flex;
            flex-direction: column;
            margin-right: 2rem;  /* Added right margin */
        }

        /* Chat messages styling */
        .stChatMessage {
            background-color: transparent;
            padding: 1rem 1.5rem;
            color: white;
        }

        .stChatMessageContent {
            background-color: #3d3d3d;  /* Darker background for messages */
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            color: white !important;
        }

        /* User message specific */
        [data-testid="chat-message-user"] .stChatMessageContent {
            background-color: #4a4a4a;  /* Slightly lighter for user messages */
            color: white !important;
        }

        /* Assistant message specific */
        [data-testid="chat-message-assistant"] .stChatMessageContent {
            background-color: #3d3d3d;
            color: white !important;
        }

        /* Chat input container */
        .stChatInputContainer {
            padding: 1rem 1.5rem;
            border-top: 1px solid #444;
            background-color: #2d2d2d;
            margin-right: 0;
        }

        /* Ensure text color is white everywhere */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }

        /* Headers styling */
        .stMarkdown h3 {
            color: white !important;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }

        /* Analysis sections */
        .analysis-section {
            background-color: #3d3d3d;
            padding: 1.2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            border: 1px solid #444;
            color: white !important;
        }

        /* Style for subheaders */
        .stSubheader {
            color: white !important;
        }

        /* Style for chat input */
        .stChatInput {
            background-color: #3d3d3d !important;
            color: white !important;
            border-color: #444 !important;
        }

        /* Scrollbar styling */
        [data-testid="column"]::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        [data-testid="column"]::-webkit-scrollbar-track {
            background: #2d2d2d;
            border-radius: 3px;
        }

        [data-testid="column"]::-webkit-scrollbar-thumb {
            background: #4a4a4a;
            border-radius: 3px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Confidence Coach AI")

# Create two columns with more space
col1, col2 = st.columns([6, 4])  # Adjusted ratio for better space distribution

with col1:
    st.subheader("Analysis Dashboard")
    # Create a container for scrollable content
    analysis_container = st.container()
    
    with analysis_container:
        # Display analysis and summary for the latest message
        if st.session_state.messages:
            latest_msg = [m for m in st.session_state.messages if m["role"] == "assistant"]
            if latest_msg:
                latest_msg = latest_msg[-1]
                st.markdown("### Latest Analysis")
                st.write(latest_msg["analysis"])
                
                st.markdown("### Summary")
                st.write(latest_msg["summary"])

        # Add a button to show full history
        if st.button("Show Full History"):
            response = requests.get(
                f"http://localhost:8000/history/{st.session_state.session_id}"
            )
            if response.status_code == 200:
                history = response.json()
                st.markdown("### Chat History")
                for entry in history["history"]:
                    st.markdown(f"**Turn {entry['turn']}**")
                    st.markdown("*Analysis:*")
                    st.write(entry["analysis"])
                    st.markdown("*Summary:*")
                    st.write(entry["summary"])
                    st.markdown("---")

with col2:
    st.subheader("Chat Interface")
    # Create a container for chat messages
    chat_container = st.container()
    
    # Display chat messages in the container
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat input at the bottom
    if prompt := st.chat_input("Enter your message"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": datetime.now()})
        
        # Call API
        try:
            with st.spinner('Processing your message...'):
                response = requests.post(
                    "http://localhost:8000/analyze",
                    params={"session_id": st.session_state.session_id},
                    json={
                        "message": prompt,
                        "is_first_submission": len(st.session_state.messages) == 1
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Add assistant's response to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["feedback"],
                        "analysis": result["analysis"],
                        "summary": result["summary"],
                        "timestamp": datetime.now()
                    })
                    # Rerun to update the UI
                    st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")