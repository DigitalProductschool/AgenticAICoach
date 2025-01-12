import os
import pytest
from fastapi.testclient import TestClient
from cv_reviewer.app.api import app

# Create a test client for FastAPI
client = TestClient(app)

def get_test_file(file_name):
    """
    Retrieves the absolute path of a test file located in the 'data' directory.
    :param file_name: Name of the test file.
    :return: Absolute path of the test file.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, "data", file_name)

@pytest.fixture
def setup_test_environment():
    """
    Fixture to set up the test environment.
    Ensures required directories exist before running tests.
    """
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def test_analyze_with_jd(setup_test_environment):
    """
    Test analyzing a CV with a provided job description.
    """
    cv_file_path = get_test_file("sample_cv.pdf")
    jd_file_path = get_test_file("sample_jd.txt")

    with open(cv_file_path, "rb") as cv_file, open(jd_file_path, "r", encoding="utf-8") as jd_file:
        files = {"cv_file": cv_file}
        data = {"job_description": jd_file.read()}

        response = client.post("/api/analyze/", files=files, data=data)

    # Verify response status and structure
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    json_response = response.json()

    assert "result" in json_response.keys(), "Response does not contain 'result'."
    assert json_response["status"] == "success", f"Expected status 'success', got {json_response['status']}"

def test_analyze_without_jd(setup_test_environment):
    """
    Test analyzing a CV without a provided job description.
    """
    cv_file_path = get_test_file("sample_cv.pdf")

    with open(cv_file_path, "rb") as cv_file:
        files = {"cv_file": cv_file}
        data = {"job_description": ""}

        response = client.post("/api/analyze/", files=files, data=data)

    # Verify response status and structure
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    json_response = response.json()

    assert "result" in json_response.keys(), "Response does not contain 'result'."
    assert json_response["status"] == "success", f"Expected status 'success', got {json_response['status']}"

def test_no_cv_uploaded(setup_test_environment):
    """
    Test uploading a request without a CV file.
    """
    data = {"job_description": "Sample Job Description"}

    response = client.post("/api/analyze/", data=data)

    assert response.status_code == 422
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "Field required"

@pytest.mark.parametrize("task_name", ["structure", "relevance", "language", "power", "report"])
def test_download_reports(task_name):
    """
    Test downloading the output files for various tasks.
    """
    response = client.get(f"/api/{task_name}")
    
    # Verify the response status and content type
    assert response.status_code == 200, f"Failed to download {task_name}.md"
    assert "text/markdown" in response.headers["content-type"], \
        f"Expected 'text/markdown', got {response.headers['content-type']}"
    
    # Verify file content is returned
    assert response.content, f"The content of {task_name}.md is empty"
