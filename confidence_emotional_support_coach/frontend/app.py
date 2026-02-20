import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/communicate"  # Update if needed

st.title("AI Confidence Coach")
st.write("Chat with the coach to improve your communication!")

# Session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
# Function to query FastAPI
def get_response(user_text):
    response = requests.post(API_URL, json={"text": user_text})
    if response.status_code == 200:
        return response.json()
    else:
        return {"revised_text": "", "suggestions": []}

# Display chat history
for msg in st.session_state.messages:
    role, text = msg["role"], msg["text"]
    if role == "user":
        st.markdown(f"**You**: {text}")
    else:
        st.markdown(f"**AI Coach**: {text}")

# Input box
user_input = st.text_input("You:", key="input")

# Send button
if st.button("Send"):
    if user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        result = get_response(user_input)

        # Build coach reply
        revised = result.get("revised_text", "")
        suggestions = result.get("suggestions", [])
        feedback = result.get("feedback", "")
        sug_lines = "".join([
            f"🗑️ Remove **{s['from_']}**\n\n" if not s['to']
            else f"✅ Replace **{s['from_']}** ➡️ **{s['to']}**\n\n"
            for s in suggestions
        ])
        if suggestions:
            coach_reply = (
                f"\n📝 **Suggested Improvements**:\n\n"
                f"{sug_lines}\n\n"
                f"🔁 **Revised**: {revised}\n\n"
                f"💬 {feedback}"
            )
        else:
            coach_reply = f"💬 {feedback}"
        st.session_state.messages.append({"role": "coach", "text": coach_reply})
        # Clear the input after submission
        st.session_state.user_input = ""
        
        # Clear the text input after submission
        st.rerun()
