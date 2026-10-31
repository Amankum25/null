# CivicFlow — Team Boundaries and Integration Architecture

## 1. Team ownership

### Member 1 — Core Backend, Frontend and Integration Owner

Owns:
- Core FastAPI service and API gateway/orchestrator.
- PostgreSQL schema and authoritative application/session state.
- Authentication, users, service catalog, state/department taxonomy, documents metadata, approvals and tracking.
- Frontend route/component integration and final merge.
- AI and Browser HTTP clients, retries/timeouts, idempotency, policy checks and event handling.
- Infrastructure/local Docker Compose and integration tests.

Must not embed AI reasoning or Playwright implementation into Core. Keep adapters clean.

### Member 2 — AI Agent Owner

Owns an independently runnable AI service:
- FastAPI service with LangGraph orchestration.
- Intent classification and natural-language service interpretation.
- State/department/service resolution and ambiguity handling.
- Official-source retrieval/RAG with citations and source metadata.
- Eligibility/document/process reasoning where verified source data exists.
- Browser form interpretation and field-mapping proposals.
- AI conversation/task state in its own storage/checkpoint mechanism.

Must not:
- import Playwright/browser implementation;
- directly write Core PostgreSQL tables;
- make external submission or irreversible actions;
- claim a portal is official without source verification;
- receive passwords, OTPs, CAPTCHA answers or auth secrets.

### Member 3 — Browser Automation Owner

Owns an independently runnable Browser service:
- FastAPI + Playwright + Chromium worker.
- Browser session lifecycle and isolation.
- Verified URL navigation and redirect safety checks.
- Page/DOM/accessibility inspection and grounded element handles.
- Approved field fill and action execution.
- Screenshot/stream channel, pause, takeover, resume and stop.
- Sanitized browser evidence and session events.

Must not:
- import LangGraph/LLM internals;
- directly write Core PostgreSQL tables;
- independently decide application authorization or final user consent;
- bypass CAPTCHA/MFA, portal access restrictions or user confirmation;
- store secrets in normal logs or event payloads.

## 2. Service boundaries

Recommended local ports (adjust to existing repo standards):
- Core API: `8000`
- AI service: `8001`
- Browser service: `8002`
- PostgreSQL: `5432`
- Redis: `6379`
- Optional object storage (MinIO): `9000/9001`

Only Core owns the authoritative application database. AI owns its checkpoint/session context in its own persistence namespace; Browser uses ephemeral session storage/Redis. No shared write access to Core DB.

## 3. Contract-first workflow

Place shared versioned schemas in a contract package, e.g.:

```text
backend/contracts/civicflow_contracts/
  common/
  discovery/
  ai/
  browser/
  application/
  events/
  json_schema/
  examples/
```

- Version contracts (`1.0.0` initially or preserve an existing established version).
- Generate Pydantic models and JSON Schema/OpenAPI from one authoritative definition where possible.
- Add example request/response payloads and contract tests.
- After the initial freeze, changes require a proposal and version compatibility check.
- Each service can use local mocks generated from the contract to work independently.

## 4. Core orchestration flow

1. Frontend sends custom service request to Core.
2. Core creates a discovery/application record and correlation ID.
3. Core calls AI service using typed request/response.
4. AI returns intent, possible service matches, official source references, unresolved facts and proposed next step.
5. Core applies policy and decides what is shown/allowed.
6. When citizen chooses a candidate, Core persists verified service/source selection.
7. Core asks Browser service to start an isolated session for the selected allowed official portal.
8. Browser inspects page and sends grounded field data/events.
9. Core passes safe page/field context to AI; AI returns field-mapping proposals.
10. Core evaluates policy and asks for user confirmation where needed.
11. Browser executes approved actions and reports results.
12. Core updates application state and event timeline.
13. Any final submission requires a fresh user confirmation and verified outcome evidence.

## 5. Suggested adapter interfaces

Core should depend on interfaces, not concrete internals:
- `AIServiceClient`: interpret request, discover service, explain process, propose field mappings.
- `BrowserServiceClient`: create session, navigate approved URL, inspect page, execute approved grounded action, pause/take control/resume/stop, fetch safe evidence.

Provide real HTTP and mock implementations so Core/frontend can be built and tested before M2/M3 are finished.

## 6. Branch ownership

Suggested branches (adapt to repo's existing branch policy):
- `feature/core-backend-member1`
- `feature/ai-agent-member2`
- `feature/browser-agent-member3`
- `integration/backend-main`

Member 1 owns contract package and integration branch. M2 and M3 own their module directories and tests. Avoid overlapping ownership of the same files.

## 7. Local repository layout (suggestion, not mandatory)

```text
backend/
  contracts/civicflow_contracts/
  services/
    core_api/
    ai_agent/
    browser_agent/
  integration/
    adapters/
    mocks/
    tests/
infrastructure/
  docker-compose.yml
  postgres/
  redis/
  minio/
docs/
  architecture/
  contracts/
  member-1-guide.md
  member-2-guide.md
  member-3-guide.md
  integration-guide.md
```

Keep the existing repository structure if already present and healthy. Don't mass-move files just to match this suggested tree.

## 8. Integration milestone order

1. Freeze request/response contracts and service ownership.
2. M1 builds Core state machine + mock AI/Browser clients and front-end flow.
3. M2 implements AI endpoints against contract and standalone tests.
4. M3 implements Browser endpoints against contract and local mock government portal.
5. Each member passes contract tests independently.
6. Integrate through HTTP adapters, not internal module imports.
7. Run end-to-end scenario: custom request → source candidate → user chooses → browser session → inspect → AI proposes values → browser fills approved values → user takeover → review → explicit submit confirmation → evidence/tracking.

## 9. Required contract tests

- API request/response schema compatibility.
- Core rejects mismatched contract versions.
- Correlation ID propagation across Core, AI, Browser and events.
- Idempotent session/application creation.
- AI cannot call Browser tools directly.
- Browser does not accept arbitrary unverified origins.
- Browser rejects stale/un-grounded element handles.
- Core rejects action without permission/user confirmation.
- Sensitive field values are redacted.
- Submission event requires verified evidence; otherwise `submission_unconfirmed`.
