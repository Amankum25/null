"""Common base schemas shared across all CivicFlow services."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from civicflow_contracts import CONTRACT_VERSION


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ApplicationStatus(str, Enum):
    """Authoritative application statuses — only Core API may transition these."""
    draft = "draft"
    prepared = "prepared"
    validation_complete = "validation_complete"
    waiting_for_approval = "waiting_for_approval"
    approved_for_submission = "approved_for_submission"
    submission_in_progress = "submission_in_progress"
    submitted = "submitted"
    failed = "failed"
    uncertain = "uncertain"


class DocumentStatus(str, Enum):
    pending = "pending"
    uploaded = "uploaded"
    verified = "verified"
    rejected = "rejected"


class ServiceCategory(str, Enum):
    education = "education"
    certificates = "certificates"
    licenses = "licenses"
    benefits = "benefits"
    registrations = "registrations"
    other = "other"


class ServiceStatus(str, Enum):
    available = "available"
    coming_soon = "coming_soon"
    information_only = "information_only"


class ErrorSeverity(str, Enum):
    warning = "warning"
    error = "error"
    critical = "critical"


# ---------------------------------------------------------------------------
# Base Models
# ---------------------------------------------------------------------------

class ContractMeta(BaseModel):
    """Envelope metadata present in every service-to-service message."""
    contract_version: str = Field(default=CONTRACT_VERSION, description="Semantic version of the contract schema")
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID tracing the request across services")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID for this individual request")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorDetail(BaseModel):
    """Standard error structure returned by every service."""
    code: str = Field(..., description="Machine-readable error code, e.g. ELIGIBILITY_FAILED")
    message: str = Field(..., description="Human-readable error message")
    severity: ErrorSeverity = ErrorSeverity.error
    field: str | None = Field(default=None, description="Specific field that caused the error, if applicable")
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Top-level error response wrapper."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    errors: list[ErrorDetail]


class IdempotencyKey(BaseModel):
    """Idempotency key for safe retries on non-idempotent operations."""
    idempotency_key: str = Field(default_factory=lambda: str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# Identity References
# ---------------------------------------------------------------------------

class UserRef(BaseModel):
    user_id: str


class ApplicationRef(BaseModel):
    application_id: str


class ServiceRef(BaseModel):
    service_id: str


# ---------------------------------------------------------------------------
# Service & Application Context (shared read-only views)
# ---------------------------------------------------------------------------

class ServiceSummary(BaseModel):
    """Lightweight service information sent as context to AI / Browser agents."""
    service_id: str
    title: str
    category: ServiceCategory
    description: str
    jurisdiction: str | None = None
    department: str | None = None
    official_url: str | None = None
    status: ServiceStatus
    workflow_steps: list[str] = Field(default_factory=list)
    eligibility_criteria: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)


class ApplicantContext(BaseModel):
    """Sanitized applicant information (never includes passwords/OTPs)."""
    user_id: str
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None


class DocumentRequirement(BaseModel):
    """A single required document with its current status."""
    document_id: str
    name: str
    file_type: str = "PDF / JPG"
    status: DocumentStatus = DocumentStatus.pending
    notes: str | None = None


class ApplicationContext(BaseModel):
    """Sanitized application snapshot sent to downstream services."""
    application_id: str
    service_id: str
    status: ApplicationStatus
    form_data: dict[str, Any] = Field(default_factory=dict, description="Non-sensitive collected form values")
    documents: list[DocumentRequirement] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ServiceContext(BaseModel):
    """Full context bundle sent from Core to downstream services."""
    service: ServiceSummary
    applicant: ApplicantContext
    application: ApplicationContext


# ---------------------------------------------------------------------------
# Source Citation
# ---------------------------------------------------------------------------

class SourceCitation(BaseModel):
    """A reference to an official source backing an AI answer."""
    title: str
    url: str | None = None
    snippet: str | None = None
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)
