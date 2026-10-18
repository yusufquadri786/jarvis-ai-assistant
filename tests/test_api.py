"""Basic local tests for the Yusuf AI Assistant API."""
import os
from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_homepage_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Yusuf AI Assistant" in response.text


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_status_does_not_reveal_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "example-not-a-real-key")
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["api_key_configured"] is True
    assert "example-not-a-real-key" not in response.text


def test_chat_requires_api_key_when_not_configured(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "language": "auto"},
    )
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]
