"""Browser Agent service contracts — request/response schemas for Core ↔ Browser communication."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from civicflow_contracts import CONTRACT_VERSION
from civicflow_contracts.common import ContractMeta


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BrowserSessionStatusEnum(str, Enum):
    creating = "creating"
    active = "active"
    paused = "paused"
    user_control = "user_control"
    closing = "closing"
    closed = "closed"
    failed = "failed"
    expired = "expired"


class BrowserCommandType(str, Enum):
    navigate = "navigate"
    click = "click"
    type_text = "type_text"
    select_option = "select_option"
    scroll = "scroll"
    screenshot = "screenshot"
    inspect_dom = "inspect_dom"
    inspect_accessibility = "inspect_accessibility"
    find_form_fields = "find_form_fields"
    fill_form = "fill_form"
    wait = "wait"
    evaluate_js = "evaluate_js"


class BrowserEventType(str, Enum):
    session_created = "session_created"
    navigation_completed = "navigation_completed"
    page_inspected = "page_inspected"
    form_fields_identified = "form_fields_identified"
    form_fields_filled = "form_fields_filled"
    sensitive_input_required = "sensitive_input_required"
    user_control_started = "user_control_started"
    user_control_returned = "user_control_returned"
    submission_attempt_started = "submission_attempt_started"
    submission_evidence_captured = "submission_evidence_captured"
    submission_outcome_uncertain = "submission_outcome_uncertain"
    session_failed = "session_failed"
    session_closed = "session_closed"
    screenshot_captured = "screenshot_captured"
    error = "error"


class SessionCapability(str, Enum):
    navigation = "navigation"
    form_filling = "form_filling"
    screenshots = "screenshots"
    streaming = "streaming"
    dom_inspection = "dom_inspection"
    user_takeover = "user_takeover"


# ---------------------------------------------------------------------------
# Session Policy
# ---------------------------------------------------------------------------

class SessionPolicy(BaseModel):
    """Security and resource policy for a browser session."""
    max_duration_seconds: int = Field(default=1800, ge=60, le=7200)
    allowed_domains: list[str] = Field(default_factory=list)
    block_downloads: bool = True
    block_uploads: bool = False
    block_private_ips: bool = True
    screenshot_on_navigation: bool = True


# ---------------------------------------------------------------------------
# Session Lifecycle
# ---------------------------------------------------------------------------

class BrowserSessionCreateRequest(BaseModel):
    """POST /internal/v1/browser/sessions"""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    user_id: str
    application_id: str
    service_id: str
    approved_portal_url: str
    allowed_domains: list[str] = Field(default_factory=list)
    session_policy: SessionPolicy = Field(default_factory=SessionPolicy)
    requested_capabilities: list[SessionCapability] = Field(
        default_factory=lambda: list(SessionCapability)
    )


class BrowserSessionResponse(BaseModel):
    """Response after creating or querying a browser session."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    browser_session_id: str
    session_status: BrowserSessionStatusEnum
    stream_endpoint: str | None = None
    expiry: str | None = None
    capabilities: list[SessionCapability] = Field(default_factory=list)
    current_url: str | None = None
    page_title: str | None = None


# ---------------------------------------------------------------------------
# Browser Commands
# ---------------------------------------------------------------------------

class BrowserCommand(BaseModel):
    """POST /internal/v1/browser/sessions/{id}/commands"""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    command_type: BrowserCommandType
    parameters: dict[str, Any] = Field(default_factory=dict)
    timeout_ms: int = Field(default=30000, ge=1000, le=120000)


class BrowserCommandResult(BaseModel):
    meta: ContractMeta = Field(default_factory=ContractMeta)
    command_type: BrowserCommandType
    success: bool
    result: dict[str, Any] = Field(default_factory=dict)
    screenshot_url: str | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Browser Events (emitted from Browser → Core)
# ---------------------------------------------------------------------------

class BrowserEvent(BaseModel):
    """Event emitted by the browser service back to Core."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    browser_session_id: str
    event_type: BrowserEventType
    payload: dict[str, Any] = Field(default_factory=dict)
    screenshot_url: str | None = None


class SensitiveFieldNotice(BaseModel):
    """Notification that user must enter a sensitive value directly."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    browser_session_id: str
    field_selector: str
    field_label: str | None = None
    field_type: str = "password"
    reason: str = "This field contains sensitive information that must be entered by the user directly."


class SubmissionEvidence(BaseModel):
    """Evidence captured after a form submission attempt."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    browser_session_id: str
    application_id: str
    screenshot_urls: list[str] = Field(default_factory=list)
    page_title: str | None = None
    page_url: str | None = None
    confirmation_text: str | None = None
    reference_number: str | None = None
    outcome: str = Field(default="uncertain", pattern="^(success|failed|uncertain)$")
    raw_page_content: str | None = None
    captured_at: str | None = None


# ---------------------------------------------------------------------------
# Session Status (detailed query)
# ---------------------------------------------------------------------------

class BrowserSessionStatus(BaseModel):
    """GET /internal/v1/browser/sessions/{session_id} — detailed status."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    browser_session_id: str
    session_status: BrowserSessionStatusEnum
    current_url: str | None = None
    page_title: str | None = None
    capabilities: list[SessionCapability] = Field(default_factory=list)
    events_count: int = 0
    created_at: str | None = None
    expires_at: str | None = None
    last_activity_at: str | None = None


# ---------------------------------------------------------------------------
# Browser Capabilities
# ---------------------------------------------------------------------------

class BrowserCapabilities(BaseModel):
    """GET /internal/v1/browser/capabilities"""
    contract_version: str = CONTRACT_VERSION
    supported_commands: list[BrowserCommandType] = Field(
        default_factory=lambda: list(BrowserCommandType)
    )
    supported_capabilities: list[SessionCapability] = Field(
        default_factory=lambda: list(SessionCapability)
    )
    max_concurrent_sessions: int = 5
    mock_mode: bool = False
