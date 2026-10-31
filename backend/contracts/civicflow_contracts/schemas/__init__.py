"""JSON Schema export utility — generates JSON Schema files from all Pydantic models."""

from __future__ import annotations

import json
from pathlib import Path

from civicflow_contracts.common import (
    ApplicationContext,
    ApplicantContext,
    ContractMeta,
    DocumentRequirement,
    ErrorDetail,
    ErrorResponse,
    ServiceContext,
    ServiceSummary,
    SourceCitation,
)
from civicflow_contracts.ai import (
    AgentCapabilities,
    AgentMessage,
    AgentRunStatus,
    AgentTurnRequest,
    AgentTurnResponse,
    DocumentRequirementsRequest,
    DocumentRequirementsResponse,
    EligibilityEvaluateRequest,
    EligibilityEvaluateResponse,
    EligibilityResult,
    ProposedAction,
    ServiceDiscoverRequest,
    ServiceDiscoverResponse,
)
from civicflow_contracts.browser import (
    BrowserCapabilities,
    BrowserCommand,
    BrowserCommandResult,
    BrowserEvent,
    BrowserSessionCreateRequest,
    BrowserSessionResponse,
    BrowserSessionStatus,
    SensitiveFieldNotice,
    SessionPolicy,
    SubmissionEvidence,
)
from civicflow_contracts.events import (
    ApplicationStatusEvent,
    EventEnvelope,
)


ALL_SCHEMAS: dict[str, type] = {
    # Common
    "ContractMeta": ContractMeta,
    "ErrorDetail": ErrorDetail,
    "ErrorResponse": ErrorResponse,
    "ServiceSummary": ServiceSummary,
    "ApplicantContext": ApplicantContext,
    "ApplicationContext": ApplicationContext,
    "ServiceContext": ServiceContext,
    "DocumentRequirement": DocumentRequirement,
    "SourceCitation": SourceCitation,
    # AI
    "AgentMessage": AgentMessage,
    "AgentTurnRequest": AgentTurnRequest,
    "AgentTurnResponse": AgentTurnResponse,
    "EligibilityResult": EligibilityResult,
    "EligibilityEvaluateRequest": EligibilityEvaluateRequest,
    "EligibilityEvaluateResponse": EligibilityEvaluateResponse,
    "ServiceDiscoverRequest": ServiceDiscoverRequest,
    "ServiceDiscoverResponse": ServiceDiscoverResponse,
    "DocumentRequirementsRequest": DocumentRequirementsRequest,
    "DocumentRequirementsResponse": DocumentRequirementsResponse,
    "ProposedAction": ProposedAction,
    "AgentCapabilities": AgentCapabilities,
    "AgentRunStatus": AgentRunStatus,
    # Browser
    "SessionPolicy": SessionPolicy,
    "BrowserSessionCreateRequest": BrowserSessionCreateRequest,
    "BrowserSessionResponse": BrowserSessionResponse,
    "BrowserCommand": BrowserCommand,
    "BrowserCommandResult": BrowserCommandResult,
    "BrowserEvent": BrowserEvent,
    "SensitiveFieldNotice": SensitiveFieldNotice,
    "SubmissionEvidence": SubmissionEvidence,
    "BrowserSessionStatus": BrowserSessionStatus,
    "BrowserCapabilities": BrowserCapabilities,
    # Events
    "EventEnvelope": EventEnvelope,
    "ApplicationStatusEvent": ApplicationStatusEvent,
}


def export_json_schemas(output_dir: str | Path = None) -> dict[str, dict]:
    """Export all contract schemas as JSON Schema files.

    Parameters
    ----------
    output_dir : optional path
        If provided, writes individual `<Name>.schema.json` files to this directory.

    Returns
    -------
    dict mapping schema name → JSON Schema dict
    """
    schemas: dict[str, dict] = {}
    for name, model in ALL_SCHEMAS.items():
        schemas[name] = model.model_json_schema()

    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for name, schema in schemas.items():
            (out / f"{name}.schema.json").write_text(
                json.dumps(schema, indent=2), encoding="utf-8"
            )
    return schemas


if __name__ == "__main__":
    here = Path(__file__).parent
    export_json_schemas(here / "exported")
    print(f"Exported {len(ALL_SCHEMAS)} schemas to {here / 'exported'}")
