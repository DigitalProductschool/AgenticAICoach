import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from crewapi import app, _load_json_file, _save_json_file, ANALYSIS_HISTORY_FILE, RATING_HISTORY_FILE, REFINEMENT_HISTORY_FILE
import os
import json
from datetime import datetime
import uuid
from crew import ConfidenceCrew # Import ConfidenceCrew

# Create a test client
client = TestClient(app)

# Mock ConfidenceCrew for testing
@pytest.fixture
def mock_crew():
    with patch("crew.ConfidenceCrew") as MockCrew:  # Corrected patch target
        mock_crew_instance = MockCrew.return_value
        yield mock_crew_instance

# Helper function to clear data files after each test
def clear_data_files():
    for file in [ANALYSIS_HISTORY_FILE, RATING_HISTORY_FILE, REFINEMENT_HISTORY_FILE]:
        if os.path.exists(file):
            os.remove(file)

# Use pytest's autouse feature to run clear_data_files after each test
@pytest.fixture(autouse=True)
def cleanup_data_files():
    clear_data_files()

# Test cases
def test_analyze_text_endpoint(mock_crew):
    mock_crew.analyze_text.return_value = {"rating": "Some Rating Analysis", "advisor": "Some advice", "corrector": "Corrected text"}
    response = client.post("/analyze", json={"text": "This is a test."})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "Confidence Rating" in data["rating"]

def test_transcribe_audio_endpoint(mock_crew):
    mock_crew.transcribe_audio.return_value = "This is the transcribed text."
    response = client.post("/transcribe", json={"audio_path": "testaudio.mp3"})
    assert response.status_code == 200
    data = response.json()
    assert data["audio_path"] == "testaudio.mp3"



def test_get_emotional_advice_endpoint(mock_crew):
    mock_crew.give_advice.return_value = "Some emotional advice."  # Mock a simple string
    response = client.post("/emotional-advice", json={"text": "I'm feeling down."})
    assert response.status_code == 200