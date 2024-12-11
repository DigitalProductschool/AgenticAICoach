from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_valid_pdf():
    with open("tests/sample.pdf", "rb") as file:
        response = client.post("/upload/", files={"file": ("sample.pdf", file, "application/pdf")})
    assert response.status_code == 200
    assert "feedback" in response.json()

def test_upload_invalid_file_type():
    with open("tests/sample.txt", "rb") as file:
        response = client.post("/upload/", files={"file": ("sample.txt", file, "text/plain")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file type. Upload a PDF or DOCX file."
