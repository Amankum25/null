# Member 2 — AI Agent

Owns `services/ai_agent/` and its tests/docs. Use only `civicflow-contracts` for shared request and response types. Do not import Core or browser implementation packages or connect to Core PostgreSQL.

```powershell
uv sync --project backend/services/ai_agent
$env:PYTHONPATH="backend/contracts/civicflow_contracts;backend/services/ai_agent"
uv run --project backend/services/ai_agent uvicorn app.main:app --reload --port 8001
```

Endpoints: `/health/live`, `/health/ready`, `/internal/v1/agent/capabilities`, `/internal/v1/agent/turn`, `/internal/v1/agent/runs/{run_id}`, `/internal/v1/agent/eligibility/evaluate`, `/internal/v1/agent/services/discover`, and `/internal/v1/agent/documents/requirements`. The current API reports `deterministic_mock`; implement graph/provider/retrieval nodes as independently testable modules and preserve this label until a real provider is configured. Passwords, OTPs, CAPTCHA values and authentication secrets must never enter graph state.

Work on `feature/ai-agent-member2`. Propose contract changes to Member 1; do not edit frozen schemas directly. Deliver the branch with fixture-based tests and a short integration note.
