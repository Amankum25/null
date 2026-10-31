"""Independent AI agent API. Mock mode is explicit until a provider is configured."""
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from civicflow_contracts import CONTRACT_VERSION
from civicflow_contracts.ai import (AgentTurnRequest, AgentTurnResponse, EligibilityRequest,
    EligibilityResult, ServiceDiscoveryRequest, DocumentRequirementsRequest,
    DocumentRequirement)
from app.graph.workflow import run_workflow

app = FastAPI(title="CivicFlow AI Agent", version="0.1.0")

@app.get("/health/live")
async def live(): return {"status": "alive", "service": "ai_agent"}

@app.get("/health/ready")
async def ready(): return {"status": "ready", "service": "ai_agent", "contract_version": CONTRACT_VERSION, "mode": "deterministic_mock"}

@app.get("/internal/v1/agent/capabilities")
async def capabilities():
    return {"contract_version": CONTRACT_VERSION, "mode": "deterministic_mock", "capabilities": ["intent_understanding", "eligibility", "service_discovery", "document_requirements"]}

@app.post("/internal/v1/agent/turn", response_model=AgentTurnResponse)
async def turn(request: AgentTurnRequest):
    workflow = run_workflow(request.message, request.sanitized_application_context.model_dump(mode="json") if request.sanitized_application_context else {})
    msg = "I can help you explore this service. This response is from deterministic mock mode."
    if request.selected_service_context:
        msg = f"I can help you prepare for {request.selected_service_context.service.name}. This is deterministic mock guidance, not an eligibility decision."
    return AgentTurnResponse(contract_version=CONTRACT_VERSION, correlation_id=request.correlation_id,
        run_id=str(uuid4()), assistant_message=msg, intent=workflow.get("intent", "service_assistance"),
        selected_service=request.selected_service_context, missing_information=workflow.get("missing_information", []),
        confidence=0.25, uncertainty=["AI provider is not configured; deterministic mock mode is active."], mode="deterministic_mock")

@app.get("/internal/v1/agent/runs/{run_id}")
async def get_run(run_id: str):
    return {"contract_version": CONTRACT_VERSION, "run_id": run_id, "status": "completed", "mode": "deterministic_mock"}

@app.post("/internal/v1/agent/eligibility/evaluate", response_model=EligibilityResult)
async def eligibility(request: EligibilityRequest):
    rules = request.service_context.eligibility_rules
    missing = [str(k) for k in rules if k not in request.applicant]
    if not rules:
        return EligibilityResult(outcome="unknown", eligible=None, reasons=["No deterministic rules are configured for this service."], confidence=0.0)
    if missing:
        return EligibilityResult(outcome="needs_information", eligible=None, missing_information=missing, reasons=["Applicant information is incomplete."], confidence=0.5)
    return EligibilityResult(outcome="unknown", eligible=None, reasons=["Rules were present, but no approved evaluator is registered."], confidence=0.0)

@app.post("/internal/v1/agent/services/discover")
async def discover(request: ServiceDiscoveryRequest):
    return {"contract_version": CONTRACT_VERSION, "correlation_id": request.correlation_id, "results": [], "mode": "deterministic_mock"}

@app.post("/internal/v1/agent/documents/requirements")
async def requirements(request: DocumentRequirementsRequest):
    docs = [DocumentRequirement(document_type=name, reason="Configured for this service.") for name in request.service_context.required_documents]
    return {"contract_version": CONTRACT_VERSION, "correlation_id": request.correlation_id, "requirements": docs, "mode": "deterministic_mock"}
