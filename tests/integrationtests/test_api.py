import json

import pytest
from danish_to_english_llm.api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_process_text_successful():
    """Test successful text processing with a valid input."""
    test_input = "Hej, hvordan har du det?"
    response = client.post("/process-text/", content=json.dumps({"text": test_input}))

    assert response.status_code == 200
    assert "text" in response.json()
    assert isinstance(response.json()["text"], str)
    assert len(response.json()["text"]) > 0


def test_process_text_empty_input():
    """Test API behavior with an empty input string."""
    response = client.post("/process-text/", content=json.dumps({"text": ""}))

    assert response.status_code == 200
    assert "text" in response.json()


def test_process_text_invalid_request():
    """Test API behavior with an invalid request format."""
    response = client.post("/process-text/", content=json.dumps({"invalid_key": "some text"}))

    assert response.status_code == 422  # Unprocessable Entity


def test_process_text_non_string_input():
    """Test API behavior with non-string input."""
    response = client.post("/process-text/", content=json.dumps({"text": 12345}))

    assert response.status_code == 422  # Unprocessable Entity


def test_process_text_unicode_input():
    """Test API with Unicode characters."""
    test_input = "Jeg elsker København! 🇩🇰"
    response = client.post("/process-text/", content=json.dumps({"text": test_input}))

    assert response.status_code == 200
    assert "text" in response.json()
    assert isinstance(response.json()["text"], str)


def test_process_text_long_input():
    """Test API with a longer input text."""
    test_input = "Dansk er et skandinavisk sprog, som tales i Danmark og nogle dele af Grønland. Det er et germansk sprog med rødder i de nordiske sprog."
    response = client.post("/process-text/", content=json.dumps({"text": test_input}))

    assert response.status_code == 200
    assert "text" in response.json()
