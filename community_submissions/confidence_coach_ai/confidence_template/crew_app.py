# Fix SQLite first (must be absolute first lines)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Then fix asyncio event loop before other imports
import asyncio
import os
if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# Now import other packages
import streamlit as st
import requests
import uuid
import tempfile
from crew import ConfidenceCrew
import subprocess
import atexit
import time
from threading import Thread

# Initialize the crew
crew = ConfidenceCrew()

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_absolute_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

# API Configuration
API_PORT = 8000
API_URL = f"http://localhost:{API_PORT}"
API_PROCESS = None

def run_api():
    """Run the API in a separate thread"""
    global API_PROCESS
    API_PROCESS = subprocess.Popen(
        [sys.executable, get_absolute_path("crewapi.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    atexit.register(stop_api)

def stop_api():
    """Stop the API process"""
    if API_PROCESS:
        API_PROCESS.terminate()
        API_PROCESS.wait()

# Start API in background thread
api_thread = Thread(target=run_api, daemon=True)
api_thread.start()
time.sleep(5)  # Give API time to start

# Verify API is running
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    if response.status_code != 200:
        st.error("API failed to start properly")
except:
    st.error("Could not connect to API. Check logs for details.")


def local_css(file_name):
    """Load local CSS with absolute path"""
    try:
        path = get_absolute_path(file_name)
        with open(path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file {path} not found")

local_css("style.css")



# Configuration
USER_ID = str(uuid.uuid4())  # Generate a unique user ID for the session
API_URL = "http://localhost:8000" 

async def analyze_text(text):
    """Calls the analyze API analyze text"""
    try:
        response = requests.post(f"{API_URL}/analyze", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to the API. Please ensure the API is running. Details: {e}")
        return None
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None


async def transcribe_and_analyze(audio_path):
    """Transcribe locally, then send transcript to backend for analysis"""
    try:
        transcript = crew.transcribe_audio(audio_path)  # Local transcription
        if not transcript:
            st.error("Transcription failed")
            return None
        return await analyze_text(transcript)
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None


async def get_emotional_advice(text):
    """Calls emotional advice API"""
    try:
        response = requests.post(f"{API_URL}/emotional-advice", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to the API. Please ensure the API is running. Details: {e}")
        return None
    except Exception as e:
        st.error(f"Advice Error: {str(e)}")
        return None


# Streamlit UI
def main():
    st.title("🎙️ Confidence Coach AI")
    st.markdown("""
    Improve your communication confidence with AI-powered analysis and feedback.
    """)

    tab1, tab2, tab3 = st.tabs([
        "Text Analysis",
        "Voice Analysis",
        "Emotional Advice"
    ])

    # Text Analysis
    with tab1:
        st.header("Text Confidence Analysis")
        text_input = st.text_area("Enter your text to analyze:", height=150,
                                  placeholder="Type your text here for confidence analysis...")

        if st.button("Analyze Text", key="analyze_text"):
            if text_input.strip():
                with st.spinner("Analyzing your text..."):
                    result = asyncio.run(analyze_text(text_input))
                    if result:
                        st.success("Analysis Complete!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📊 Confidence Rating")
                            st.write(result.get("rating", "No rating analysis available"))

                            st.subheader("💡 Confidence Advice")
                            st.write(result.get("advice", "No advice available"))
                        with col2:
                            st.subheader("✏️ Suggested Improvement")
                            st.write(result.get("correction", "No correction available"))
            else:
                st.warning("Please enter some text to analyze")

    # Voice Analysis
    with tab2:
        st.header("Voice Confidence Analysis")
        audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"], key="audio_upload")
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_path = tmp_file.name

            if st.button("Transcribe and Analyze", key="analyze_upload"):
                with st.spinner("Processing your audio..."):
                    result = asyncio.run(transcribe_and_analyze(tmp_path))
                    if result:
                        st.success("Analysis Complete!")
                        st.subheader("Transcription:")
                        st.info(result.get("original_text", "No transcription available"))

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📊 Confidence Rating")
                            st.write(result.get("rating", "No rating analysis available"))

                            st.subheader("💡 Confidence Advice")
                            st.write(result.get("advice", "No advice available"))
                        with col2:
                            st.subheader("✏️ Suggested Improvement")
                            st.write(result.get("correction", "No correction available"))

            os.unlink(tmp_path)

    # Emotional Advice
    with tab3:
        st.header("Emotional Support Coach")
        st.markdown("Share how you're feeling and get personalized advice:")

        feeling_text = st.text_area("Tell the coach how you feel:",
                                    height=150,
                                    placeholder="I feel... (describe your emotions here)")

        if st.button("Get Emotional Advice"):
            if feeling_text.strip().lower().startswith("i feel"):
                with st.spinner("Analyzing your feelings..."):
                    advice = asyncio.run(get_emotional_advice(feeling_text))
                    if advice:
                        st.success("Here's some advice for you:")
                        st.write(advice.get("advice", "No advice available"))
            else:
                st.warning("Please start your sentence with 'I feel...'")

if __name__ == "__main__":
    run_api()
    main()