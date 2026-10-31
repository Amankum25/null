"""Application-level contracts used by Core API and exposed to frontend."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from civicflow_contracts.common import (
    ApplicationStatus,
    ContractMeta,
    DocumentRequirement,
    DocumentStatus,
    ServiceCategory,
    ServiceStatus,
)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., min_length=5, max_length=320)
    password: str = Field(..., min_length=8, max_length=128)
    phone: str | None = None
    location: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None = None
    location: str | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# Service Registry
# ---------------------------------------------------------------------------

class ServiceListItem(BaseModel):
    id: str
    title: str
    category: ServiceCategory
    description: str
    jurisdiction: str | None = None
    department: str | None = None
    status: ServiceStatus


class ServiceDetail(ServiceListItem):
    official_url: str | None = None
    workflow_steps: list[str] = Field(default_factory=list)
    eligibility_criteria: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)


class CategoryInfo(BaseModel):
    key: str
    label: str
    description: str
    service_count: int = 0


# ---------------------------------------------------------------------------
# Application CRUD
# ---------------------------------------------------------------------------

class CreateApplicationRequest(BaseModel):
    service_id: str
    form_data: dict[str, Any] = Field(default_factory=dict)
    selected_scholarship: str | None = None


class ApplicationSummary(BaseModel):
    id: str
    service_id: str
    service_title: str | None = None
    status: ApplicationStatus
    progress: int = 0
    created_at: str
    updated_at: str


class ApplicationDetail(BaseModel):
    id: str
    service_id: str
    user_id: str
    status: ApplicationStatus
    current_step: int = 0
    progress: int = 0
    form_data: dict[str, Any] = Field(default_factory=dict)
    documents: list[DocumentRequirement] = Field(default_factory=list)
    review_state: dict[str, bool] = Field(default_factory=dict)
    approval_state: str = "not_started"
    tracking: TrackingInfo | None = None
    created_at: str
    updated_at: str
    selected_scholarship: str | None = None


class UpdateApplicationRequest(BaseModel):
    form_data: dict[str, Any] | None = None
    current_step: int | None = None
    progress: int | None = None
    status: ApplicationStatus | None = None
    selected_scholarship: str | None = None


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

class UploadDocumentRequest(BaseModel):
    name: str
    file_type: str = "PDF / JPG"
    notes: str | None = None


class DocumentResponse(BaseModel):
    document_id: str
    name: str
    file_type: str
    status: DocumentStatus
    notes: str | None = None
    upload_url: str | None = None
    uploaded_at: str | None = None


# ---------------------------------------------------------------------------
# Review & Approval
# ---------------------------------------------------------------------------

class ReviewChecklist(BaseModel):
    application_id: str
    items: dict[str, bool] = Field(default_factory=dict)
    all_reviewed: bool = False


class UpdateReviewRequest(BaseModel):
    items: dict[str, bool]


class ApproveRequest(BaseModel):
    """Explicit user approval — required before submission."""
    confirmation: bool = Field(..., description="Must be true to approve")
    approval_note: str | None = None


class ApprovalResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    approved_at: str
    approved_by: str


# ---------------------------------------------------------------------------
# AI Interaction (frontend-facing)
# ---------------------------------------------------------------------------

class AssistantMessageRequest(BaseModel):
    message: str
    application_id: str | None = None
    service_id: str | None = None
    conversation_id: str | None = None


class AssistantMessageResponse(BaseModel):
    assistant_message: str
    intent: str | None = None
    eligibility_result: dict[str, Any] | None = None
    missing_information: list[str] = Field(default_factory=list)
    document_requirements: list[DocumentRequirement] = Field(default_factory=list)
    source_citations: list[dict[str, Any]] = Field(default_factory=list)
    proposed_action: dict[str, Any] | None = None
    conversation_id: str | None = None


# ---------------------------------------------------------------------------
# Browser Session (frontend-facing)
# ---------------------------------------------------------------------------

class CreateBrowserSessionRequest(BaseModel):
    service_id: str


class BrowserSessionSummary(BaseModel):
    session_id: str
    status: str
    stream_url: str | None = None
    current_url: str | None = None
    page_title: str | None = None
    expires_at: str | None = None


# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

class TrackingInfo(BaseModel):
    reference_number: str | None = None
    submitted_at: str | None = None
    official_status: str | None = None
    demo_mode: bool = True


class ActivityEvent(BaseModel):
    id: str
    label: str
    timestamp: str
    tone: str | None = None  # "blue" | "green" | "amber"


class TrackingEventsResponse(BaseModel):
    application_id: str
    events: list[ActivityEvent] = Field(default_factory=list)
