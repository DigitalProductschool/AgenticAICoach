from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class AudioTranscriberInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Path to the audio file to be transcribed.")

class AudioTranscriberTool(BaseTool):
    name: str = "AudioTranscriber"
    description: str = (
        "A tool to transcribe audio to text."
    )
    args_schema: Type[BaseModel] = AudioTranscriberInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        audio_file= open(argument, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
        )
        return transcription
    