import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_coaching_flow():
    print("\n=== Testing AI Pitch Coach API ===\n")
    
    # Step 1: Start a new coaching session
    print("Starting a new coaching session...")
    try:
        response = requests.post(
            f"{BASE_URL}/start_session",
            json={"user_id": "test_user"}
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
            
        result = response.json()
        session_id = result["session_id"]
        welcome_message = result["welcome_message"]
        
        print(f"Session ID: {session_id}")
        print(f"Welcome message: {welcome_message}")
        
        # Step 2: Send a test message
        print("\nSending a test message...")
        response = requests.post(
            f"{BASE_URL}/send_message",
            json={
                "session_id": session_id,
                "message": "We're building an AI-powered resume optimizer.",
                "user_id": "test_user"
            }
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
            
        result = response.json()
        coach_response = result["response"]
        
        print(f"Coach response: {coach_response}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure the API server is running with 'python run_api.py'")

if __name__ == "__main__":
    test_coaching_flow()