from crewai import Agent
import whisper
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.tools import Tool
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriberAgent:
    def __init__(self):
        pass

    def create_agent(self):
        return Agent(
            role='Transcriber',
            goal='Convert audio files into text.',
            backstory="You are an expert transcriber.",
            allow_delegation=False,
            verbose=True,
            tools=[],
        )

    def transcribe_audio(self, audio_file_path):
        """Transcribes the audio file."""
        logger.info(f"Attempting to transcribe audio file: {audio_file_path}")  # Log the file path

        try:
            logger.info("Loading Whisper model...")
            model = whisper.load_model("base")      # Using Whisper for transcription
            logger.info("Whisper model loaded.")

            logger.info("Transcribing audio...")
            result = model.transcribe(audio_file_path)  # Where the transcription happens
            logger.info("Audio transcribed.")

            transcript = result["text"]
            logger.info(f"Transcription: {transcript}")  # Log the transcription

            return transcript

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}", exc_info=True)
            return f"Error during transcription: {e}"