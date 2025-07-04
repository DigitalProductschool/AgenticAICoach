import streamlit as st
import requests

# Set Streamlit app configuration
st.set_page_config(page_title="Clarity Coach Chat", layout="centered")

# API endpoint for backend chat processing
API_URL = "http://localhost:8000"

# Reset the session if page refreshed or reloaded
if "reset_done" not in st.session_state:
    requests.post(f"{API_URL}/reset")
    st.session_state["reset_done"] = True

# Custom CSS for improved styling
st.markdown("""
    <style>
    .chat-container {
        padding: 1rem;
        max-width: 800px;
        margin: auto;
    }
    .message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        line-height: 1.5;
        font-size: 1rem;
    }
    .user-message {
        background-color: #dbeafe;
        text-align: right;
        margin-left: 10%;
    }
    .assistant-message {
        background-color: #f0fdf4;
        text-align: left;
        margin-right: 10%;
    }
    .thinking {
        color: gray;
        font-style: italic;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state and add starter assistant message
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "👋 Hello! What brings you here today?"}
    ]

# Title
st.title("🧠 AI Feature Clarity Coach")
st.caption("Guiding you step-by-step to build something amazing.")

# Render past messages in chat history
for msg in st.session_state["messages"]:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Chat input field
user_input = st.chat_input("What's on your mind?")

# Handle new user input
if user_input:
    # Append user's message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)

    # Show thinking animation
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("💭 Thinking...")

    # Send input to FastAPI backend and get assistant response
    try:
        response = requests.post(f"{API_URL}/chat", params={"user_input": user_input})
        response.raise_for_status()
        data = response.json()
        bot_msg = data["response"]

        # Append assistant's response to session
        st.session_state["messages"].append({"role": "assistant", "content": bot_msg})
        thinking_placeholder.empty()
        st.markdown(f'<div class="message assistant-message">{bot_msg}</div>', unsafe_allow_html=True)
    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Failed to get response: {e}")


# Reset the entire coaching session
if st.button("🔄 Reset Conversation"):
    try:
        requests.post(f"{API_URL}/reset")
        st.session_state["messages"] = [{"role": "assistant", "content": "👋 Hello! What brings you here today?"}]
        st.session_state["current_phase"] = "core_problem"
        st.success("Conversation reset.")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to reset conversation: {e}")
