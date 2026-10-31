from uuid import uuid4
from fastapi import APIRouter, HTTPException
from civicflow_contracts.application import AssistantMessageRequest
from civicflow_contracts.ai import AgentTurnRequest, ServiceContext
from civicflow_contracts.common import CONTRACT_VERSION
from app.api.applications import _applications
from app.adapters.clients import get_ai_client
router = APIRouter()

@router.post("/assistant/messages")
async def assistant_message(body: AssistantMessageRequest):
    record = _applications.get(body.application_id) if body.application_id else None
    if body.application_id and not record: raise HTTPException(404, "Application not found")
    ctx = None
    req = AgentTurnRequest(contract_version=CONTRACT_VERSION, user_id=uuid4(), conversation_id=body.conversation_id,
        message=body.message, selected_service_context=ctx,
        sanitized_application_context=None, allowed_actions=[])
    result = await get_ai_client().create_agent_turn(req)
    return {"message": result.assistant_message, "run_id": result.run_id, "mode": result.mode,
        "intent": result.intent, "source_citations": result.source_citations,
        "proposed_next_action": result.proposed_next_action}

@router.post("/eligibility/evaluate")
async def evaluate_eligibility():
    return {"outcome": "unknown", "eligible": None, "reasons": ["Provide service and applicant context to evaluate eligibility."], "confidence": 0.0}
