from fastapi.testclient import TestClient
from src.coach_confidence.main import app  # Ensure this path matches your project structure

client = TestClient(app)


def test_analyze_text():
    # Sample input for the test
    sample_input = {"user_text": "I am not sure if I can do this."}

    # Make the POST request to the analyze endpoint
    response = client.post("/analyze", json=sample_input)
    
    # Print the response JSON for debugging
    print("Response JSON:", response.json())
    
    # Check if the response status code is 200
    assert response.status_code == 200
    
    # Get the result from the response
    result = response.json()

    # Optionally print out other parts of the response for further inspection
    print("Result:", result)
