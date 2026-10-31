"""AI Agent service contracts — request/response schemas for Core ↔ AI communication."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from civicflow_contracts import CONTRACT_VERSION
from civicflow_contracts.common import (
    ApplicationContext,
    ApplicantContext,
    ContractMeta,
    DocumentRequirement,
    ServiceSummary,
    SourceCitation,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AgentIntent(str, Enum):
    """Intents the AI agent can classify from user messages."""
    greeting = "greeting"
    service_discovery = "service_discovery"
    eligibility_check = "eligibility_check"
    document_inquiry = "document_inquiry"
    form_help = "form_help"
    status_inquiry = "status_inquiry"
    general_question = "general_question"
    submission_request = "submission_request"
    unknown = "unknown"


class ConfidenceLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class ProposedActionType(str, Enum):
    """Types of actions AI may propose for Core to execute."""
    navigate_portal = "navigate_portal"
    fill_form = "fill_form"
    upload_document = "upload_document"
    start_browser_session = "start_browser_session"
    request_user_input = "request_user_input"
    check_eligibility = "check_eligibility"
    none = "none"


# ---------------------------------------------------------------------------
# Agent Turn (conversational exchange)
# ---------------------------------------------------------------------------

class AgentMessage(BaseModel):
    """A single message in the conversation."""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    timestamp: str | None = None


class AgentTurnRequest(BaseModel):
    """POST /internal/v1/agent/turn — request body."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    user_id: str
    conversation_id: str
    message: str
    selected_service_context: ServiceSummary | None = None
    sanitized_application_context: ApplicationContext | None = None
    applicant_context: ApplicantContext | None = None
    allowed_actions: list[ProposedActionType] = Field(default_factory=list)
    conversation_history: list[AgentMessage] = Field(default_factory=list)


class EligibilityResult(BaseModel):
    """Structured eligibility evaluation output."""
    eligible: bool | None = None
    confidence: ConfidenceLevel = ConfidenceLevel.medium
    reasons: list[str] = Field(default_factory=list)
    missing_criteria: list[str] = Field(default_factory=list)
    source_citations: list[SourceCitation] = Field(default_factory=list)


class ProposedAction(BaseModel):
    """An action the AI proposes — Core decides whether to accept."""
    action_type: ProposedActionType
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    requires_user_approval: bool = False


class AgentTurnResponse(BaseModel):
    """POST /internal/v1/agent/turn — response body."""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    assistant_message: str
    intent: AgentIntent = AgentIntent.unknown
    selected_service: ServiceSummary | None = None
    eligibility_result: EligibilityResult | None = None
    missing_information: list[str] = Field(default_factory=list)
    document_requirements: list[DocumentRequirement] = Field(default_factory=list)
    proposed_next_action: ProposedAction | None = None
    source_citations: list[SourceCitation] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.medium
    run_id: str | None = None


# ---------------------------------------------------------------------------
# Eligibility Evaluation (direct, non-conversational)
# ---------------------------------------------------------------------------

class EligibilityEvaluateRequest(BaseModel):
    """POST /internal/v1/agent/eligibility/evaluate"""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    service_id: str
    applicant_context: ApplicantContext
    application_context: ApplicationContext | None = None
    form_data: dict[str, Any] = Field(default_factory=dict)


class EligibilityEvaluateResponse(BaseModel):
    meta: ContractMeta = Field(default_factory=ContractMeta)
    service_id: str
    result: EligibilityResult


# ---------------------------------------------------------------------------
# Service Discovery
# ---------------------------------------------------------------------------

class ServiceDiscoverRequest(BaseModel):
    """POST /internal/v1/agent/services/discover"""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    query: str
    category: str | None = None
    jurisdiction: str | None = None
    max_results: int = Field(default=10, ge=1, le=50)


class ServiceDiscoverResponse(BaseModel):
    meta: ContractMeta = Field(default_factory=ContractMeta)
    services: list[ServiceSummary] = Field(default_factory=list)
    query_understanding: str | None = None


# ---------------------------------------------------------------------------
# Document Requirements
# ---------------------------------------------------------------------------

class DocumentRequirementsRequest(BaseModel):
    """POST /internal/v1/agent/documents/requirements"""
    meta: ContractMeta = Field(default_factory=ContractMeta)
    service_id: str
    applicant_context: ApplicantContext | None = None


class DocumentRequirementsResponse(BaseModel):
    meta: ContractMeta = Field(default_factory=ContractMeta)
    service_id: str
    documents: list[DocumentRequirement] = Field(default_factory=list)
    notes: str | None = None


# ---------------------------------------------------------------------------
# Agent Capabilities & Run Status
# ---------------------------------------------------------------------------

class AgentCapabilities(BaseModel):
    """GET /internal/v1/agent/capabilities"""
    contract_version: str = CONTRACT_VERSION
    supported_intents: list[AgentIntent] = Field(default_factory=lambda: list(AgentIntent))
    supported_actions: list[ProposedActionType] = Field(default_factory=lambda: list(ProposedActionType))
    mock_mode: bool = False


class AgentRunStatus(BaseModel):
    """GET /internal/v1/agent/runs/{run_id}"""
    run_id: str
    status: str  # "running" | "completed" | "failed"
    result: AgentTurnResponse | None = None
    error: str | None = None
