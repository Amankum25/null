# Member 1 — Core and integration

Owns `contracts/`, `services/core_api/`, `integration/`, `infrastructure/`, and shared integration documentation. Core is intended to be the only writer of authoritative application state.

Install/run from the repo root with `uv`:

```powershell
uv sync --project backend/services/core_api
$env:PYTHONPATH="backend/contracts/civicflow_contracts;backend/services/core_api"
uv run --project backend/services/core_api uvicorn app.main:app --reload --port 8000
```

`USE_MOCK_AI` and `USE_MOCK_BROWSER` select adapter implementations. Set them false only when the matching service is reachable. The current Core stores are process-local development stores; do not deploy or run multiple workers until persistence and auth ownership checks are completed.

Create feature branch `feature/core-backend-member1` from the agreed integration base. Merge contract changes first, then service branches, and review state transitions, security boundaries and evidence handling before accepting any integration.
