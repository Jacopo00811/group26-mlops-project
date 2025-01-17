# from fastapi.testclient import TestClient
# from src.danish_to_english_llm.api import app

# client = TestClient(app)

# def test_translate_text():
#     # Test valid translation

#     response = client.post("/translate/", json={"danish_text": "Hej, hvordan har du det?"})
#     assert response.status_code == 200
#     assert response.json() == {"english_text": "Hello, how are you?"}

#     # Test empty input
#     response = client.post("/translate/", json={"danish_text": ""})
#     assert response.status_code == 422

# tests/test_api.py

from fastapi.testclient import TestClient

from src.danish_to_english_llm.api import app

client = TestClient(app)


def test_translate():
    # Test valid translation
    response = client.post("/translate", json={"text": "Hej, hvordan har du det?"})
    assert response.status_code == 200
    assert "translated_text" in response.json()

    # Test invalid input (empty text)
    response = client.post("/translate", json={"text": ""})
    assert response.status_code == 422  # Unprocessable Entity

    # Test if translation is returned as expected
    result = response.json()
    assert isinstance(result["translated_text"], str)
    assert result["translated_text"] != ""  # Ensure translation is not empty
