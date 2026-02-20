import unittest
import sys
import os

# Add the tests directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_coaching_flow import TestPitchCoachFlow
from tests.test_api import TestPitchCoachAPI
from tests.test_feedback_tracker import TestFeedbackTracker
from tests.test_web_interface import TestWebInterface

def run_tests():
    """Run all tests for the AI Pitch Coach application"""
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Use TestLoader instead of makeSuite
    loader = unittest.TestLoader()
    
    # Add test cases
    test_suite.addTests(loader.loadTestsFromTestCase(TestPitchCoachFlow))
    test_suite.addTests(loader.loadTestsFromTestCase(TestPitchCoachAPI))
    test_suite.addTests(loader.loadTestsFromTestCase(TestFeedbackTracker))
    test_suite.addTests(loader.loadTestsFromTestCase(TestWebInterface))
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return the result
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)