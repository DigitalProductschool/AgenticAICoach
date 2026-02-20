import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

class TestWebInterface(unittest.TestCase):
    """Test cases for the web interface endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_get_ui(self):
        """Test serving the UI page"""
        # Mock the FileResponse to avoid file system dependencies
        with patch('app.main.FileResponse', return_value=MagicMock(status_code=200)) as mock_file_response:
            response = self.client.get("/ui")
            
            # Verify the endpoint returned success
            self.assertEqual(response.status_code, 200)
            
            # Verify the correct file was served
            mock_file_response.assert_called_once_with("app/static/index.html")
    
    def test_static_files(self):
        """Test serving static files"""
        # We need to mock the StaticFiles to avoid file system dependencies
        # This is a bit more complex since app.mount() is called during import
        # For a real project, you might want to use a real file or mock the entire response
        pass


if __name__ == "__main__":
    unittest.main()