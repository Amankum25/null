# Implementation Map for the Existing CivicFlow Repository

This is a suggested map, not a mandate to move files. Codex must inspect the actual repository and keep its established patterns.

## Frontend areas

| Area | Existing/currently known location | Redesign target |
|---|---|---|
| App shell | `app/(app)/layout.tsx`, `components/app-shell.tsx` or current equivalent | Expanded deep-green sidebar + topbar with dropdowns |
| Dashboard | `app/(app)/dashboard/page.tsx` | Approved Indian Civic dashboard |
| New Application | `app/(app)/applications/new/page.tsx` | Preserve six-card category landing |
| Service directory | `app/(app)/services/page.tsx`, `components/service-catalog.tsx` | Search, state/department/category filters, capability status, custom CTA |
| Service details | `app/(app)/services/[slug]/page.tsx` | Verified details and capability-specific action |
| Application workspace | `app/(app)/applications/[id]/workspace/page.tsx`, `components/browser-viewer.tsx` | Three-panel actual browser/AI/user control surface |
| Form/review/tracking | Existing application-specific pages | Keep per-application state and real safety gates |
| Shared UI | `components/page-primitives.tsx` and existing UI kit | Re-skin and extend rather than duplicate primitives |
| Store | `lib/civicflow-store.tsx` or existing equivalent | Preserve unique ID and isolated per-app state; extend custom mode |

If these paths no longer exist, search for current canonical equivalent. Do not create duplicate routes/components.

## Backend areas

Inspect existing services first. Expected ownership:
- Core: API, DB and application orchestration.
- AI Agent: independent AI FastAPI/LangGraph service.
- Browser Agent: independent Playwright FastAPI service.
- Contract package: shared Pydantic/JSON Schema/OpenAPI.

## Repository work strategy

1. Create a route/component inventory before modification.
2. Implement tokens and shared app shell before pages.
3. Preserve the current application store and route semantics.
4. Add custom application support as an extension of the current application model if viable.
5. Add state/department filters against a normalized catalog model.
6. Add mock adapters if AI/Browser service is not connected yet.
7. Run existing scripts; report results truthfully.
