import pytest
from fastapi.testclient import TestClient
from src.main import app
from io import BytesIO

client = TestClient(app)

def test_assess_pdf():
    try:
        with open("sample.pdf", "rb") as f:
            file_content = f.read()
        
        response = client.post(
            "/assess/",
            files={"file": ("sample.pdf", BytesIO(file_content), "application/pdf")},
            data={"guidelines": "Check for clarity."}
        )
        assert response.status_code == 200
        assert "report" in response.json()
    except FileNotFoundError:
        pytest.skip("sample.pdf not found, skipping test")


def test_assess_unsupported_file():
    response = client.post(
        "/assess/",
        files={"file": ("sample.txt", b"some text", "text/plain")},
        data={"guidelines": "Check for clarity."}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

