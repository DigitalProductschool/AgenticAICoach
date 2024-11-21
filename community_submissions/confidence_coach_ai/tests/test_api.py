import unittest
import requests

class TestConfidenceCoachAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.session_id = "test_session"

    def test_analyze_message(self):
        """Test the /analyze endpoint with a sample message"""
        test_input = {
            "message": "Hello, I'm feeling nervous about my upcoming presentation.",
            "is_first_submission": True
        }
        
        response = requests.post(
            f"{self.base_url}/analyze?session_id={self.session_id}", 
            json=test_input
        )
        
        # Print debug information
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        # Assert response status
        self.assertEqual(response.status_code, 200)
        
        # Parse response data
        data = response.json()
        
        # Check required fields
        expected_fields = ["turn", "analysis", "summary", "feedback"]
        for field in expected_fields:
            self.assertIn(field, data, f"Missing field: {field}")
        
        # Check data types and content
        self.assertIsInstance(data["turn"], int)
        self.assertIsInstance(data["analysis"], str)
        self.assertIsInstance(data["summary"], str)
        self.assertIsInstance(data["feedback"], str)
        
        # Check non-empty content
        self.assertGreater(len(data["analysis"]), 0)
        self.assertGreater(len(data["summary"]), 0)
        self.assertGreater(len(data["feedback"]), 0)

    def test_chat_history(self):
        """Test the /history endpoint"""
        response = requests.get(f"{self.base_url}/history/{self.session_id}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("history", data)
        self.assertIsInstance(data["history"], list)

if __name__ == '__main__':
    unittest.main(verbosity=2)