import os

import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from agents.transcriber import TranscriberAgent
from dotenv import load_dotenv



load_dotenv()

# Define the audio file path
AUDIO_FILE = 'testaudio.mp3'  # Make sure this file exists

# Initialize the TranscriberAgent
transcriber_agent = TranscriberAgent()
transcriber = transcriber_agent.create_agent()

# Transcribe the audio
try:
    transcript = transcriber_agent.transcribe_audio(AUDIO_FILE)

    print("Transcription:")
    print(transcript)

except Exception as e:
    print(f"Error: {e}")