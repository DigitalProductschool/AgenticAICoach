import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

# Create a test client instance to simulate HTTP requests
client = TestClient(app)


# Test 1: Chat endpoint returns a valid response
def test_chat_endpoint_returns_valid_response():
    response = client.post("/chat", params={"user_input": "I want to build a chatbot"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "phase" in data
    assert "chat_history" in data
    assert isinstance(data["chat_history"], list)
    assert isinstance(data["response"], str)
    assert data["response"].strip() != ""


# Test 2: Chat can progress through phases without breaking
def test_chat_progresses_phase_resiliently():
    inputs = [
        "I want to build a chatbot",
        "The core problem is user distraction",
        "It should help focus better",
        "Here's an AI solution idea",
        "Let's validate this"
    ]

    final_phase = None
    for user_input in inputs:
        response = client.post("/chat", params={"user_input": user_input})
        assert response.status_code == 200
        data = response.json()
        final_phase = data["phase"]

    # We accept any of these as valid outcomes depending on LLM decisions
    allowed_phases = ["core_problem", "core_value", "brainstorm_solution", "validate", "complete"]
    assert final_phase in allowed_phases


# Test 3: Reset endpoint clears session state correctly
def test_reset_clears_state_and_resets_phase():
    # Start conversation
    client.post("/chat", params={"user_input": "Some initial input"})

    # Reset
    response = client.post("/reset")
    assert response.status_code == 200
    data = response.json()

    assert "chat_history" in data
    assert data["chat_history"] == []

    # After reset, send another message to check state is restarted
    restart_response = client.post("/chat", params={"user_input": "Starting over"})
    restart_data = restart_response.json()

    assert restart_data["phase"] == "core_problem"
    assert len(restart_data["chat_history"]) > 0
