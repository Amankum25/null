"""Standalone browser session API. Session control is intentionally mock-backed initially."""
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
import secrets
from urllib.parse import urlparse
from uuid import UUID
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from civicflow_contracts import CONTRACT_VERSION
from civicflow_contracts.browser import (BrowserCommand, BrowserEvent, BrowserSessionCreateRequest,
    BrowserSessionResponse, BrowserSessionStatus, BrowserCapability)

app = FastAPI(title="CivicFlow Browser Agent", version="0.1.0")
sessions: dict[UUID, dict] = {}
stream_tokens: dict[str, tuple[UUID, datetime]] = {}

def validate_target(url: str, allowed: list[str]) -> None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().rstrip(".")
    if parsed.scheme != "https" or not host:
        raise HTTPException(400, "Only HTTPS portal URLs are allowed")
    try:
        address = ip_address(host)
        if not address.is_global:
            raise HTTPException(400, "Private and local network targets are blocked")
    except ValueError:
        if host in {"localhost", "localhost.localdomain"} or "." not in host:
            raise HTTPException(400, "Local network targets are blocked")
    if not any(host == d.lower().lstrip(".") or host.endswith("." + d.lower().lstrip(".")) for d in allowed):
        raise HTTPException(403, "Target host is not in the service-approved domain list")

@app.get("/health/live")
async def live(): return {"status": "alive", "service": "browser_agent"}

@app.get("/health/ready")
async def ready(): return {"status": "ready", "service": "browser_agent", "contract_version": CONTRACT_VERSION, "mode": "mock_session_store"}

@app.get("/internal/v1/browser/capabilities")
async def capabilities():
    return {"contract_version": CONTRACT_VERSION, "capabilities": ["navigate", "inspect", "fill_non_sensitive", "screenshot", "pause_resume", "user_takeover"], "mode": "mock_session_store"}

@app.post("/internal/v1/browser/sessions", response_model=BrowserSessionResponse)
async def create_session(req: BrowserSessionCreateRequest):
    validate_target(str(req.approved_portal_url), req.allowed_domains)
    sid = UUID(int=__import__("uuid").uuid4().int)
    expires = datetime.now(timezone.utc) + timedelta(seconds=req.session_policy.max_duration_seconds)
    token = secrets.token_urlsafe(32)
    stream_tokens[token] = (sid, expires)
    session = {"browser_session_id": sid, "session_status": BrowserSessionStatus.active,
        "expires_at": expires, "user_id": req.user_id, "application_id": req.application_id,
        "allowed_domains": req.allowed_domains, "url": str(req.approved_portal_url),
        "contract_version": CONTRACT_VERSION, "correlation_id": req.correlation_id, "stream_token": token}
    sessions[sid] = session
    return BrowserSessionResponse(browser_session_id=sid, session_status=BrowserSessionStatus.active,
        expires_at=expires, stream_endpoint=f"/internal/v1/browser/sessions/{sid}/stream?token={token}",
        capabilities=req.requested_capabilities or list(BrowserCapability))

@app.get("/internal/v1/browser/sessions/{session_id}")
async def get_session(session_id: UUID):
    session = sessions.get(session_id)
    if not session: raise HTTPException(404, "Browser session not found")
    return {k: v for k, v in session.items() if k not in {"allowed_domains", "user_id", "stream_token"}}

@app.post("/internal/v1/browser/sessions/{session_id}/commands")
async def command(session_id: UUID, req: BrowserCommand):
    session = sessions.get(session_id)
    if not session: raise HTTPException(404, "Browser session not found")
    if session["session_status"] != BrowserSessionStatus.active: raise HTTPException(409, "Session is not under automation control")
    if req.command_type == "navigate":
        if not req.target_url: raise HTTPException(422, "target_url is required")
        validate_target(str(req.target_url), session["allowed_domains"])
        session["url"] = str(req.target_url)
    # Sensitive values are never reflected, logged, or placed in event payloads.
    return {"contract_version": CONTRACT_VERSION, "command_id": req.command_id, "status": "accepted", "mode": "mock_session_store"}

async def _set(session_id: UUID, status: BrowserSessionStatus):
    if session_id not in sessions: raise HTTPException(404, "Browser session not found")
    sessions[session_id]["session_status"] = status
    if status in {BrowserSessionStatus.closed, BrowserSessionStatus.expired}:
        stream_tokens.pop(sessions[session_id].get("stream_token"), None)
    return await get_session(session_id)

@app.post("/internal/v1/browser/sessions/{session_id}/pause")
async def pause(session_id: UUID): return await _set(session_id, BrowserSessionStatus.paused)
@app.post("/internal/v1/browser/sessions/{session_id}/resume")
async def resume(session_id: UUID): return await _set(session_id, BrowserSessionStatus.active)
@app.post("/internal/v1/browser/sessions/{session_id}/take-control")
async def take_control(session_id: UUID): return await _set(session_id, BrowserSessionStatus.user_control)
@app.post("/internal/v1/browser/sessions/{session_id}/return-control")
async def return_control(session_id: UUID): return await _set(session_id, BrowserSessionStatus.active)
@app.post("/internal/v1/browser/sessions/{session_id}/close")
async def close(session_id: UUID): return await _set(session_id, BrowserSessionStatus.closed)

@app.websocket("/internal/v1/browser/sessions/{session_id}/stream")
async def stream(websocket: WebSocket, session_id: UUID, token: str):
    token_record = stream_tokens.pop(token, None)  # single-use opaque stream credential
    session = sessions.get(session_id)
    token_session, token_expires = token_record if token_record else (None, None)
    if token_session != session_id or not session or session["session_status"] in {BrowserSessionStatus.closed, BrowserSessionStatus.expired} or token_expires <= datetime.now(timezone.utc) or session["expires_at"] <= datetime.now(timezone.utc):
        await websocket.close(code=4401)
        return
    await websocket.accept()
    try:
        # Mock transport reports lifecycle state; the Playwright worker will publish frames/events here.
        await websocket.send_json({"contract_version": CONTRACT_VERSION, "event_type": "session_status", "status": session["session_status"].value})
        await websocket.close(code=1000, reason="mock stream snapshot complete")
    except WebSocketDisconnect:
        return
