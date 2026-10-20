"""Tests for integration metadata and sensitive-action approval policy."""
from fastapi.testclient import TestClient

from integrations import approval_required, planned_integrations
from main import app

client = TestClient(app)


def test_sensitive_actions_always_require_confirmation():
    for action in ("send_message", "publish_post", "comment", "delete_file", "run_shell_command"):
        assert approval_required(action) is True


def test_external_and_destructive_risks_require_confirmation():
    assert approval_required("custom_action", risk="external_effect") is True
    assert approval_required("custom_action", risk="destructive") is True


def test_read_only_action_can_skip_confirmation():
    assert approval_required("list_files", risk="read") is False


def test_unknown_action_fails_closed():
    assert approval_required("unknown_action") is True


def test_catalogue_does_not_claim_integrations_are_connected():
    integrations = planned_integrations()
    assert integrations
    assert all(item.connection_state == "not_connected" for item in integrations)
    assert all(item.implementation_state == "planned" for item in integrations)
    assert any(item.integration_id == "android_companion" for item in integrations)
    assert any(item.integration_id == "windows_companion" for item in integrations)


def test_integrations_endpoint_is_explicit_about_unconnected_state():
    response = client.get("/api/integrations")
    assert response.status_code == 200
    payload = response.json()
    assert "no external app accounts are connected" in payload["note"]
    assert payload["integrations"]
    assert all(item["connection_state"] == "not_connected" for item in payload["integrations"])
