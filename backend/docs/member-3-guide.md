# Member 3 — Browser Agent

Owns `services/browser_agent/` and its tests/docs. Use only `civicflow-contracts` for shared requests, commands and events. Do not import Core/AI code or connect to Core PostgreSQL.

```powershell
uv sync --project backend/services/browser_agent
uv run playwright install chromium
$env:PYTHONPATH="backend/contracts/civicflow_contracts;backend/services/browser_agent"
uv run --project backend/services/browser_agent uvicorn app.main:app --reload --port 8002
```

Endpoints cover health/capabilities and session create/read/commands/pause/resume/take-control/return-control/close. The current service is an explicitly labeled in-memory session scaffold, not a live Playwright implementation. Its WebSocket returns a one-use-token authenticated lifecycle snapshot only; replace that with a worker-backed isolated context, live frame streaming, Redis TTL namespace `civicflow:browser:`, and signed Core event callbacks before claiming browser automation is complete.

Validate HTTPS and approved host on every navigation, block loopback/private IPs, redact sensitive values, and require user entry for password/OTP/CAPTCHA. Never automate a real government portal in tests. Use branch `feature/browser-agent-member3`, and deliver local mock portal scenarios with your branch.
