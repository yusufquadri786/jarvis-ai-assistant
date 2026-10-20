"""Integration metadata and approval policy for Yusuf AI Assistant.

This module describes planned integration capabilities; it does not connect
accounts or execute actions. Real adapters must verify OAuth/API permissions.
"""
from typing import Literal

from pydantic import BaseModel, Field


ActionRisk = Literal["read", "local", "external_effect", "destructive"]


class IntegrationDescriptor(BaseModel):
    """Public, secret-free description of an integration and its current state."""

    integration_id: str
    name: str
    platform: Literal["windows", "android", "web", "social", "productivity", "storage"]
    implementation_state: Literal["planned", "prototype", "available"] = "planned"
    connection_state: Literal["not_connected", "connected", "needs_setup"] = "not_connected"
    capabilities: list[str] = Field(default_factory=list)
    approval_required_actions: list[str] = Field(default_factory=list)
    notes: str = ""


# These actions always require a clear user confirmation immediately before execution.
APPROVAL_REQUIRED_ACTIONS = frozenset({
    "send_message",
    "publish_post",
    "comment",
    "delete_file",
    "overwrite_file",
    "purchase",
    "change_account_settings",
    "run_shell_command",
    "install_software",
})


def approval_required(action: str, risk: ActionRisk | None = None) -> bool:
    """Return whether an action needs explicit confirmation before execution.

    Unknown actions fail closed: callers must confirm them unless they explicitly
    classify them as read-only. This function does not execute any action.
    """
    normalized = action.strip().lower()
    if normalized in APPROVAL_REQUIRED_ACTIONS:
        return True
    if risk in {"external_effect", "destructive"}:
        return True
    if risk == "read":
        return False
    return True


def planned_integrations() -> list[IntegrationDescriptor]:
    """Return a safe catalogue of future integrations, not live connections."""
    return [
        IntegrationDescriptor(
            integration_id="windows_companion",
            name="Windows companion",
            platform="windows",
            capabilities=["open_allowlisted_apps", "open_url", "local_status"],
            approval_required_actions=["run_shell_command", "install_software", "delete_file"],
            notes="Planned; local agent and device authentication are not implemented.",
        ),
        IntegrationDescriptor(
            integration_id="android_companion",
            name="Android companion",
            platform="android",
            capabilities=["launch_supported_intents", "voice_input", "notifications_with_permission"],
            approval_required_actions=["send_message", "change_account_settings"],
            notes="Planned; requires an Android client and user-granted permissions.",
        ),
        IntegrationDescriptor(
            integration_id="todoist",
            name="Todoist",
            platform="productivity",
            capabilities=["tasks", "reminders"],
            approval_required_actions=["delete_task"],
            notes="Planned; account connection and API permissions are not configured.",
        ),
        IntegrationDescriptor(
            integration_id="dropbox",
            name="Dropbox",
            platform="storage",
            capabilities=["list_files", "read_files"],
            approval_required_actions=["delete_file", "overwrite_file"],
            notes="Planned; account connection is not configured.",
        ),
        IntegrationDescriptor(
            integration_id="instagram_meta",
            name="Instagram via official Meta APIs",
            platform="social",
            capabilities=["eligible_account_publishing", "supported_insights"],
            approval_required_actions=["publish_post", "comment", "send_message"],
            notes="Planned; account eligibility, permissions, and platform limits apply.",
        ),
        IntegrationDescriptor(
            integration_id="whatsapp_business",
            name="WhatsApp Business Platform",
            platform="social",
            capabilities=["approved_business_messaging"],
            approval_required_actions=["send_message"],
            notes="Planned; this is not unrestricted control of personal WhatsApp.",
        ),
    ]
