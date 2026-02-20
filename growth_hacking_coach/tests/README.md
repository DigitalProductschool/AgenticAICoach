# Growth Hacking Coach Tests

This directory contains tests for the Growth Hacking Coach application.

## Test Structure

The tests are organized into three main files:

1. `test_api.py` - Tests for the FastAPI endpoints
2. `test_streamlit.py` - Tests for the Streamlit interface functions
3. `test_crew.py` - Tests for the CrewAI functionality

## Running the Tests
 
### Running All Tests

To run all tests, use the `run_tests.py` script:

```bash
python tests/run_tests.py
```

### Running Individual Test Files

You can also run individual test files:

```bash
python -m unittest tests/test_api.py
python -m unittest tests/test_streamlit.py
python -m unittest tests/test_crew.py
```

### Running Specific Test Cases

To run a specific test case:

```bash
python -m unittest tests.test_api.TestGrowthHackingCoachAPI.test_read_root
```

## Test Dependencies

The tests require the following dependencies:

- unittest (standard library)
- unittest.mock (standard library)
- fastapi.testclient
- requests

## Mocking

The tests use mocking to isolate the components being tested:

- API tests mock the CrewAI components
- Streamlit tests mock the Streamlit library and API requests
- Crew tests mock the CrewAI Agent, Task, and Crew classes

## Adding New Tests

When adding new functionality to the Growth Hacking Coach, please add corresponding tests to maintain code quality and prevent regressions.
