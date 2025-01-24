import random

from locust import HttpUser, between, task


class TranslationUser(HttpUser):
    """A Locust user class that simulates load on the translation API."""

    wait_time = between(1, 3)

    danish_texts = [
        "Hej, jeg er gay",
        "Hej, hvordan har du det?",
        "Velkommen til Danmark",
        "Jeg elsker at rejse",
        "Tak for din hjælp",
    ]

    @task
    def translate_text(self) -> None:
        """Task that simulates translating Danish texts."""
        text_to_translate = random.choice(self.danish_texts)

        payload = {"text": text_to_translate}

        self.client.post("/process-text/", json=payload, headers={"Content-Type": "application/json"})
