import requests
import json
import time

# Test the iterative pitch improvement
base_url = "http://localhost:8000"

# Initial pitch
initial_pitch = """
We're building an AI-powered resume optimizer to help job seekers improve their job applications.
Our solution analyzes resumes against job descriptions and provides tailored recommendations.
We target recent graduates and career changers who struggle with the job application process.
"""

# Test the API
def test_iteration():
    print("Testing iterative pitch improvement...")
    
    # Submit initial pitch
    print("\n1. Submitting initial pitch...")
    response = requests.post(
        f"{base_url}/analyze_pitch",
        json={
            "pitch_content": initial_pitch,
            "stage": "initial",
            "user_id": "test_user"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    pitch_id = result["pitch_id"]
    print(f"Received pitch_id: {pitch_id}")
    print("Initial analysis received.")
    
    # Improved pitch based on feedback
    improved_pitch = f"{initial_pitch}\n\nWe've partnered with 50+ recruiters to train our AI model on what makes a successful application. Our first beta showed a 40% improvement in interview rates."
    
    # Submit improved pitch
    print("\n2. Submitting improved pitch...")
    response = requests.post(
        f"{base_url}/analyze_pitch",
        json={
            "pitch_content": improved_pitch,
            "stage": "refinement",
            "pitch_id": pitch_id,
            "user_id": "test_user"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    print("Refinement analysis received.")
    
    # Get pitch history
    print("\n3. Retrieving pitch history...")
    response = requests.post(
        f"{base_url}/pitch_history",
        json={
            "pitch_id": pitch_id,
            "user_id": "test_user"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    history = response.json()
    print(f"Pitch has {len(history['history']['iterations'])} iterations")
    print(f"Improvement metrics: {json.dumps(history['metrics'], indent=2)}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    # Make sure the API is running before testing
    print("Make sure your API is running (python run_api.py)")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    
    test_iteration()