import streamlit as st
import requests

st.set_page_config(page_title="Clarity Coach Chat", layout="centered")

API_URL = "http://localhost:8000"

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

# Display chat history
for msg in st.session_state["messages"]:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input field
user_input = st.chat_input("What's on your mind?")

# Handle user input
if user_input:
    # Append user's message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("💭 Thinking...")

    # Call FastAPI backend
    try:
        response = requests.post(f"{API_URL}/chat", params={"user_input": user_input})
        response.raise_for_status()
        data = response.json()
        bot_msg = data["response"]

        st.session_state["messages"].append({"role": "assistant", "content": bot_msg})
        thinking_placeholder.empty()
        st.markdown(f'<div class="message assistant-message">{bot_msg}</div>', unsafe_allow_html=True)
    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Failed to get response: {e}")

# Reset button
if st.button("🔄 Reset Conversation"):
    try:
        requests.post(f"{API_URL}/reset")
        st.session_state["messages"] = [{"role": "assistant", "content": "👋 Hello! What brings you here today?"}]
        st.session_state["current_phase"] = "core_problem"
        st.success("Conversation reset.")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to reset conversation: {e}")
