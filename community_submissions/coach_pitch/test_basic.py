import requests

# Test the basic API functionality
def test_basic_api():
    print("Testing basic API functionality...")
    
    # Test the root endpoint
    response = requests.get("http://localhost:8000/")
    print(f"Root endpoint: {response.status_code}")
    print(response.json())
    
    # Test a simple pitch analysis with minimal content
    simple_pitch = "AI resume optimizer for job seekers."
    
    print("\nSending a very simple pitch for analysis...")
    response = requests.post(
        "http://localhost:8000/analyze_pitch",
        json={
            "pitch_content": simple_pitch,
            "stage": "initial",
            "user_id": "test_basic"
        },
        timeout=300  # 5-minute timeout
    )
    
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Here's the pitch_id:", result["pitch_id"])
    else:
        print("Error response:", response.text)

if __name__ == "__main__":
    test_basic_api()