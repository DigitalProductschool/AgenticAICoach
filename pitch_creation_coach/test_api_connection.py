import requests

def test_api():
    try:
        # Test the root endpoint
        response = requests.get("http://localhost:8000/")
        print("API Connection Test:")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("\nAPI is running correctly!")
        else:
            print("\nAPI is running, but returned an unexpected status code.")
            
        return response.status_code == 200
    except Exception as e:
        print(f"\nError connecting to API: {str(e)}")
        print("\nMake sure the API server is running with 'python run_api.py'")
        return False

if __name__ == "__main__":
    test_api()