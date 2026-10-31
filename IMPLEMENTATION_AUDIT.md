# CivicFlow implementation audit

Audit based on the current local working tree. Existing uncommitted work was preserved.

## What the screenshot showed

The workspace is localStorage-backed (`lib/civicflow-store.tsx`). The selected Domicile Certificate record had no portal URL, so `BrowserViewer` could not create a session. The browser service was configured to default to `mock` mode; that mode stores session metadata but does not launch Chromium or render a live portal. The viewer did not check service readiness before presenting a connection state.

## Member 1 / Core

| Area | Current evidence | Status |
|---|---|---|
| Service registry | `backend/services/core_api/app/api/services.py` uses a small static list; frontend uses `src/data/serviceCatalog.ts`. | Partial; not canonical or India-wide |
| Inventory | `CivicFlow_India_Service_Inventory_Important_Files_v1/` contains 36 gateways and 900 candidate rows; `backend/scripts/ingest_inventory.py` validates but does not persist/import them. | Staging inventory only |
| Applications | `app/api/applications.py` uses a process-local dictionary; frontend also persists local demo state. | Demo persistence only |
| Database | SQLAlchemy models exist in `app/models/core.py`; no migration or route repository layer is wired. | Schema foundation only |
| Auth | `ENFORCE_AUTH` defaults false and application APIs are not consistently ownership-protected. | Development-only |
| Review / approval / evidence | Frontend review state is locally mutable; no end-to-end Core approval/evidence gate. | Partial/demo |
| Documents and notifications | UI routes exist; storage, owner authorization, durable read state, and verification integration are incomplete. | Partial/demo |
| AI boundary | `backend/services/ai_agent` exists, but discovery and form reasoning are not a production feature; Member 2 owns this work. | Handoff needed |

## Member 3 Browser Agent

| Capability | Local implementation | Status |
|---|---|---|
| Playwright engine | `backend/services/browser_agent/browser_agent/browser/controller.py` owns Playwright/Chromium contexts; `app/playwright_runtime.py` adapts it. | Implemented, runtime depends on Chromium installation |
| Session API | `backend/services/browser_agent/app/main.py` stores session maps in memory. | Partial; not durable/owner-authorized |
| URL validation | HTTPS and host allowlist checks. Redirect validation, DNS rebinding defenses and approved service lookup by Core are incomplete. | Partial |
| Inspect and ground | Page observer and element grounder return safe metadata and require fresh snapshots. | Implemented in package; API integration partial |
| Field fill | `/commands` supports `fill` by description with grounding and action validation. | Partial; only text fill exposed through HTTP |
| Live viewer | Browser Agent now streams JPEG frames over its single-use WebSocket token; frontend renders received frames. | Implemented, runtime not exercised in this pass |
| Takeover and control | API status endpoints exist, but no attached interactive viewer or robust server-side policy gate. | Partial |
| Sensitive fields | Validator blocks sensitive/consequential actions and result models redact values. | Implemented in package; broader system needs validation |
| Final submit/evidence | No complete explicit approval, receipt capture and Core evidence persistence path. | Missing |

## Changes in this pass

- Added official Maharashtra Aaple Sarkar citizen-service listing URLs to the Maharashtra income and domicile preparation records, so the workspace can open the official listing page. This is a discovery/listing destination, not a verified service-specific application URL.
- Set the browser client default to `http://localhost:8002` for local development and added Browser Agent CORS for the local frontend origins.
- The viewer now checks `/health/ready` and refuses to label a mock session as a live Playwright connection.
- Added image-frame consumption, page inspection, safe field metadata display, and takeover/return-control requests to the viewer.
- Added opt-in `http://localhost:9090` target support, guarded by `CIVICFLOW_ALLOW_LOCAL_MOCK=true`, and a clearly labelled fictional public-service form with a deterministic mock receipt.
- Added Core geography endpoints for the 36 inventory states/UTs, a districts endpoint that explicitly reports the source lacks district lists, and an application portal lookup endpoint.
- Added direct service-card and preparation-workspace entry actions in the New Application flow in the preceding change.

## Remaining work before CivicFlow can be called complete

Core persistence and ownership/auth enforcement; durable application workspace loading; inventory import into a review queue; service facets and service-level evidence; remote browser session authorization; live browser streaming; interactive takeover; inspect/fill/select/check/radio/upload command coverage; Core action approval and submission evidence; secure document storage; durable notifications; and the Member 2 contract handoff. No real government form should be submitted during development.

Member 2 must implement intent and service resolution, source-grounded eligibility/document reasoning, and typed field guidance/proposals. Core remains the policy gate and Member 3 remains the browser executor. `MEMBER_2_HANDOFF.md` records the required boundary.
