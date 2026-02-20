# Growth Hacking Coach Testing Guide

This document provides detailed information about the test suite for the Growth Hacking Coach application.

## Overview

The Growth Hacking Coach test suite is designed to ensure the reliability and functionality of the application. It includes tests for the API endpoints, CrewAI functionality, and Streamlit interface.

The tests use mocking extensively to isolate components and avoid external dependencies, making them fast and reliable.

## Test Structure

The test suite is organized into the following files:

1. `test_api.py` - Tests for the FastAPI endpoints
   - Tests the root endpoint
   - Tests the query endpoint with successful responses
   - Tests error handling in the query endpoint

2. `test_crew.py` - Tests for the CrewAI functionality
   - Tests crew initialization
   - Tests search tool initialization
   - Tests the crew kickoff method with sample conversation history

3. `test_streamlit.py` - Tests for the Streamlit interface functions (currently disabled)
   - Tests the mock response generator
   - Tests API communication with successful responses
   - Tests handling of connection errors
   - Tests handling of error responses

4. `test_data.py` - Contains sample data used across all tests
   - Sample user messages
   - Sample conversation histories
   - Sample API responses
   - Sample error messages

5. `run_tests.py` - Script to run all tests
   - Dynamically loads test classes
   - Creates and runs a test suite
   - Reports test results

6. `test_run_tests.py` - Tests for the run_tests.py script

## Running Tests

### Prerequisites

Before running the tests, make sure you have the required dependencies installed:

```bash
pip install fastapi pytest pytest-cov requests unittest-mock
```

### Running All Tests

To run all tests, use the `run_tests.py` script:

```bash
python tests/run_tests.py
```

This will run the API and Crew tests. The Streamlit tests are currently disabled in the run_tests.py script because they require more complex mocking.

Expected output:
```
test_query_endpoint (module.name.TestGrowthHackingCoachAPI.test_query_endpoint)
Test the query endpoint with a mock crew ... ok
test_query_endpoint_with_error (module.name.TestGrowthHackingCoachAPI.test_query_endpoint_with_error)
Test the query endpoint handles errors correctly ... ok
test_read_root (module.name.TestGrowthHackingCoachAPI.test_read_root)
Test the root endpoint returns a welcome message ... ok
test_crew_initialization (module.name.TestGrowthHackingCrew.test_crew_initialization)
Test that the crew initializes correctly ... ok
test_crew_kickoff (module.name.TestGrowthHackingCrew.test_crew_kickoff)
Test that the crew kickoff method works correctly ... ok
test_search_tool_initialization (module.name.TestGrowthHackingCrew.test_search_tool_initialization)
Test that the search tool is initialized correctly ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.041s

OK
```

### Running Individual Test Files

You can also run individual test files:

```bash
python -m unittest tests/test_api.py
python -m unittest tests/test_crew.py
```

### Running with pytest

You can also use pytest to run the tests:

```bash
pytest tests/test_api.py -v
pytest tests/test_crew.py -v
```

### Running Streamlit Tests

The Streamlit tests require more complex mocking and are currently disabled in the run_tests.py script. If you want to run them, you'll need to modify the test_streamlit.py file to properly mock the Streamlit module.

### Running with Coverage

To run tests with coverage reporting:

```bash
pytest --cov=src.growth_hacking_coach tests/
```

## Test Data

The `test_data.py` file contains sample data used across all tests:

```python
# Sample user messages for testing
SAMPLE_USER_MESSAGES = [
    "How can I grow my startup?",
    "I need help with user engagement for my mobile app.",
    "What are the best viral marketing techniques for a SaaS product?",
    # ...
]

# Sample conversation history for testing
SAMPLE_CONVERSATION_HISTORY = [
    [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you with growth hacking today?"}
    ],
    # ...
]

# Sample API responses for testing
SAMPLE_API_RESPONSES = [
    {
        "response": "To grow your startup effectively, I recommend focusing on these key areas:..."
    },
    # ...
]

# Sample error messages for testing
SAMPLE_ERROR_MESSAGES = [
    "Connection refused",
    "Internal Server Error",
    # ...
]
```

Using consistent test data across all tests makes them more maintainable and easier to understand.

## Mocking Strategy

The tests use extensive mocking to isolate components and avoid external dependencies:

### API Tests
- Mock the `GrowthHackingCrew` class to test API endpoints without requiring actual LLM calls
- Mock the crew's `kickoff` method to return predefined responses
- Mock error conditions to test error handling

### Streamlit Tests
- Mock the `streamlit` module to test UI functions without a running Streamlit app
- Mock `requests.post` to test API communication without a running API server
- Mock session state to test state management

### Crew Tests
- Mock CrewAI components (`Agent`, `Task`, `Crew`, `LLM`) to test crew functionality without actual AI models
- Test the search tool initialization without making actual API calls
- Test the crew kickoff method with sample conversation history

## Adding New Tests

When adding new functionality to the Growth Hacking Coach, please add corresponding tests:

1. For new API endpoints, add tests to `test_api.py`
   ```python
   def test_new_endpoint(self):
       """Test the new endpoint"""
       response = client.get("/new-endpoint")
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.json(), {"expected": "response"})
   ```

2. For new CrewAI functionality, add tests to `test_crew.py`
   ```python
   @patch('growth_hacking_coach.crew.Agent')
   def test_new_agent(self, mock_agent):
       """Test the new agent"""
       crew = GrowthHackingCrew()
       self.assertIsNotNone(crew.new_agent())
       mock_agent.assert_called_once()
   ```

3. For new Streamlit UI functions, add tests to `test_streamlit.py` (once mocking is fixed)
   ```python
   @patch('requests.post')
   def test_new_ui_function(self, mock_post):
       """Test the new UI function"""
       result = new_ui_function("test input")
       self.assertIsInstance(result, str)
   ```

4. If needed, add new test data to `test_data.py`
   ```python
   # Add new test data
   NEW_TEST_DATA = [
       {"input": "test", "expected_output": "result"}
   ]
   ```

## Best Practices

1. **Use descriptive test names** that clearly indicate what is being tested
2. **Keep tests independent** - each test should be able to run on its own
3. **Use mocks appropriately** to isolate the code being tested
4. **Test both success and failure cases** to ensure robust error handling
5. **Keep test data separate** from test logic for better maintainability
6. **Add comments** to explain complex test setups or assertions

## Continuous Integration

These tests can be integrated into a CI/CD pipeline using GitHub Actions. A sample workflow:

```yaml
name: Growth Hacking Coach Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'community_submissions/growth_hacking_coach/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'community_submissions/growth_hacking_coach/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        cd community_submissions/growth_hacking_coach
        python -m pip install --upgrade pip
        pip install pytest pytest-cov requests fastapi
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd community_submissions/growth_hacking_coach
        python tests/run_tests.py
```

## Troubleshooting

If you encounter issues running the tests:

1. **Import errors**: Make sure the path to the source code is correct in the test files
   ```python
   # Add the src directory to the path
   sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
   ```

2. **Mocking issues**: Verify that mock objects are set up correctly
   ```python
   # Example of proper mocking
   @patch('growth_hacking_coach.crew.Agent')
   def test_function(self, mock_agent):
       mock_agent.return_value = MagicMock()
   ```

3. **Test data issues**: Ensure test data is properly formatted and accessible
   ```python
   # Import test data at the top of the file
   from test_data import SAMPLE_USER_MESSAGES
   ```

4. **Streamlit mocking**: If working on Streamlit tests, use a comprehensive mock
   ```python
   # Create a more comprehensive mock for streamlit
   streamlit_mock = MagicMock()
   streamlit_mock.session_state = MagicMock()
   sys.modules['streamlit'] = streamlit_mock
   ```
