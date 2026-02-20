import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI default URL

def test_get_environmental_advice():
    test_input = {
        "location": "London",
        "user_input": "How can I reduce air pollution?",
        "user_points": 0
    }
    
    response = requests.post(f"{BASE_URL}/environmental-advice", json=test_input)
    
    # Print response details for debugging
    print(f"\nResponse Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    if response.status_code != 200:
        try:
            error_detail = response.json().get('detail', 'No error detail available')
            print(f"Error Detail: {error_detail}")
        except:
            print("Could not parse error response")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if all required fields are present in the response
    expected_fields = [
        "research", "action_plan", "quiz_question", "quiz_options",
        "user_points", "correct_answer", "pm25", "pm10"
    ]
    
    for field in expected_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check data types
    assert isinstance(data["quiz_options"], list)
    assert isinstance(data["user_points"], int)

def test_submit_quiz_answer():
    test_input = {
        "user_answer": "b",
        "correct_answer": "b",
        "user_points": 10
    }
    
    response = requests.post(f"{BASE_URL}/quiz-answer", json=test_input)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "feedback" in data
    assert "points" in data
    assert data["points"] == 11  # Should increment by 1 for correct answer

def test_invalid_input():
    test_input = {
        "invalid_field": "test"
    }
    
    response = requests.post(f"{BASE_URL}/environmental-advice", json=test_input)
    assert response.status_code == 422  # Validation error
