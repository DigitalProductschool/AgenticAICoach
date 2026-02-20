import unittest
import sys
import os
import importlib.util

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Function to load a test class from a file without importing it directly
def load_test_class(file_path, class_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load test classes
    TestGrowthHackingCoachAPI = load_test_class(
        os.path.join(current_dir, "test_api.py"),
        "TestGrowthHackingCoachAPI"
    )

    TestGrowthHackingCrew = load_test_class(
        os.path.join(current_dir, "test_crew.py"),
        "TestGrowthHackingCrew"
    )

    # Add the test cases
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestGrowthHackingCoachAPI))
    # Skip Streamlit tests for now as they require more complex mocking
    # test_suite.addTest(loader.loadTestsFromTestCase(TestStreamlitApp))
    test_suite.addTest(loader.loadTestsFromTestCase(TestGrowthHackingCrew))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())
