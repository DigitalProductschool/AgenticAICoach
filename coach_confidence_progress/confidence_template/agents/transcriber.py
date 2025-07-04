from crewai import Agent
import os
import io
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.tools import Tool
import logging
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




class TranscriberAgent:
    def __init__(self):
        self.client = self._create_speech_client()
    def _create_speech_client(self):
        """Creates and returns a Google Cloud Speech-to-Text client."""
        try:
            # Assemble credentials from environment variables
            credentials_dict = {
                "type": os.environ.get("GCP_TYPE"),
                "project_id": os.environ.get("GCP_PROJECT_ID"),
                "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("GCP_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
                "client_id": os.environ.get("GCP_CLIENT_ID"),
                "auth_uri": os.environ.get("GCP_AUTH_URI"),
                "token_uri": os.environ.get("GCP_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("GCP_AUTH_PROVIDER_CERT_URL"),
                "client_x509_cert_url": os.environ.get("GCP_CLIENT_CERT_URL"),
                "universe_domain": os.environ.get("GCP_UNIVERSE_DOMAIN")
            }
            
            # Create credentials object
            credentials = service_account.Credentials.from_service_account_info(credentials_dict)
            
            # Create and return client
            return speech.SpeechClient(credentials=credentials)
            
        except Exception as e:
            logger.error(f"Error creating Speech client: {str(e)}")
            raise

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
        """Transcribes the audio file using Google Cloud Speech-to-Text."""
        logger.info(f"Attempting to transcribe audio file: {audio_file_path}")

        try:
            # Load the audio file
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Adjust encoding if needed
                sample_rate_hertz=44100,  # Adjust sample rate if needed
                language_code="en-US",  # Adjust language code if needed
            )

            # Perform the transcription
            logger.info("Sending audio to Google Cloud Speech-to-Text...")
            response = self.client.recognize(config=config, audio=audio)

            # Extract the transcript
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript

            logger.info(f"Transcription: {transcript}")
            return transcript

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}", exc_info=True)
            return f"Error during transcription: {e}"