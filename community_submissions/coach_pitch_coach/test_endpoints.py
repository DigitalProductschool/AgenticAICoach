"""
Test script to demonstrate all API endpoints for screenshots.
Run this after starting the FastAPI server.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60 + "\n")

def test_health():
    print_section("1. Health Check Endpoint")
    print(f"GET {BASE_URL}/health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_coach_mode():
    print_section("2. Coach Mode - Step-by-step Pitch Building")
    url = f"{BASE_URL}/coach"
    data = {
        "mode": "coach",
        "user_message": "We help CFOs close the books in hours instead of days using AI automation.",
        "audience": "VC",
        "funding_stage": "pre-seed"
    }
    print(f"POST {url}")
    print(f"Request Body:\n{json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_refine_mode():
    print_section("3. Refine Mode - Polish Existing Pitch")
    url = f"{BASE_URL}/coach"
    data = {
        "mode": "refine",
        "user_message": "Our product uses AI to make finance teams more efficient by automating repetitive tasks.",
        "audience": "VC",
        "funding_stage": "seed"
    }
    print(f"POST {url}")
    print(f"Request Body:\n{json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_qa_mode():
    print_section("4. Q&A Mode - Practice Investor Questions")
    url = f"{BASE_URL}/coach"
    data = {
        "mode": "qa",
        "user_message": "We automate monthly close for mid-market SaaS companies, reducing close time from 10 days to 2 days.",
        "industry": "FinTech",
        "audience": "VC",
        "funding_stage": "seed"
    }
    print(f"POST {url}")
    print(f"Request Body:\n{json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_session(session_id):
    print_section("5. Get Session Data")
    url = f"{BASE_URL}/sessions/{session_id}"
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def main():
    print("\n🚀 Testing AI Pitch Coach API")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    try:
        # Test all endpoints
        results = []
        
        results.append(("Health Check", test_health()))
        results.append(("Coach Mode", test_coach_mode()))
        results.append(("Refine Mode", test_refine_mode()))
        results.append(("Q&A Mode", test_qa_mode()))
        
        # Summary
        print_section("Test Summary")
        all_passed = True
        for name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {name}")
            if not passed:
                all_passed = False
        
        print("\n" + ("="*60))
        if all_passed:
            print("✅ All tests passed! Ready for screenshots.")
        else:
            print("⚠️  Some tests failed. Check the output above.")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Make sure the server is running:")
        print("  uvicorn src.pitch_coach.api:app --reload --port 8000")
        print("\nOr with Docker:")
        print("  docker run -p 8000:8000 -e OPENAI_API_KEY=your_key pitch-coach-api")

if __name__ == "__main__":
    main()
