import unittest
import sys
import os
import importlib
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestRunTests(unittest.TestCase):
    """Tests for the run_tests.py script"""

    @patch('unittest.TestSuite')
    @patch('unittest.TestLoader')
    @patch('unittest.TextTestRunner')
    def test_run_tests_script(self, mock_runner, mock_test_loader, mock_test_suite):
        """Test that the run_tests.py script creates and runs a test suite"""
        # Set up mocks
        mock_suite_instance = MagicMock()
        mock_test_suite.return_value = mock_suite_instance

        mock_loader_instance = MagicMock()
        mock_test_loader.return_value = mock_loader_instance
        mock_loader_instance.loadTestsFromTestCase.side_effect = lambda x: f"Suite for {x.__name__}"

        mock_runner_instance = MagicMock()
        mock_runner.return_value = mock_runner_instance

        mock_result = MagicMock()
        mock_result.wasSuccessful.return_value = True
        mock_runner_instance.run.return_value = mock_result

        # Mock importlib.util functions
        with patch('importlib.util.spec_from_file_location') as mock_spec_from_file:
            with patch('importlib.util.module_from_spec') as mock_module_from_spec:
                # Set up the mocks
                mock_spec = MagicMock()
                mock_spec_from_file.return_value = mock_spec

                mock_module = MagicMock()
                mock_module_from_spec.return_value = mock_module

                # Mock the test classes
                mock_api_test = MagicMock()
                mock_api_test.__name__ = "TestGrowthHackingCoachAPI"
                mock_crew_test = MagicMock()
                mock_crew_test.__name__ = "TestGrowthHackingCrew"

                # Set up the module to return our mock test classes
                mock_module.TestGrowthHackingCoachAPI = mock_api_test
                mock_module.TestGrowthHackingCrew = mock_crew_test

                # Mock sys.exit to prevent the test from exiting
                with patch('sys.exit') as mock_exit:
                    # Import the run_tests module
                    run_tests = importlib.import_module('run_tests')

                    # Verify that the test suite was created
                    mock_test_suite.assert_called_once()

                    # Verify that loadTestsFromTestCase was called for each test class
                    self.assertEqual(mock_loader_instance.loadTestsFromTestCase.call_count, 2)

                    # Verify that the test suite was run
                    mock_runner_instance.run.assert_called_once_with(mock_suite_instance)

                    # Verify that sys.exit was called with the correct code (0 for success)
                    mock_exit.assert_called_once_with(0)

if __name__ == "__main__":
    unittest.main()
