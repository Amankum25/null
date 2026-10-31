# CODEX MASTER PROMPT — Redesign the Complete CivicFlow Website

You are working in the **existing CivicFlow repository**. Implement a complete website redesign using the handoff in this folder. Do not create a new project, do not replace the repository, and do not perform a backend rewrite under the guise of UI work.

Read these files first:
1. `README_START_HERE.md`
2. `PRODUCT_VISION_AND_CONTEXT.md`
3. `DESIGN_SYSTEM.md`
4. `design-tokens.json`
5. `ROUTE_AND_SCREEN_MAP.json`
6. `SERVICE_DISCOVERY_AND_CUSTOM_APPLICATION.md`
7. `BROWSER_WORKSPACE_SPEC.md`
8. `TEAM_ARCHITECTURE_AND_CONTRACTS.md`
9. `DATA_MODEL_AND_API_CONTRACTS.md`
10. `ACCEPTANCE_CHECKLIST.md`

Inspect the assets in `assets/` and the clickable static reference in `prototype/index.html`.

---

## A. Start with a repository audit — do not code blindly

Before changing anything, inspect:
- package manager and scripts;
- Next.js App Router route tree;
- current sidebar, topbar and layout components;
- current `components/service-catalog.tsx` or equivalent service catalog;
- current `/applications/new` flow;
- current application store and persistence (`lib/civicflow-store.tsx` or current equivalent);
- service catalog records and status definitions;
- application workspace, browser preview, form, review, approvals and tracking pages;
- existing backend endpoints and API client adapters;
- CSS/Tailwind tokens, fonts and icon dependencies;
- all existing working navigation and state transitions.

Create a short audit checklist in your working notes. Identify what can be reused and what must not be broken. If filenames have changed, follow the current canonical implementation rather than recreating old files.

**Never delete/recreate the app shell, service catalog, application store or workflow before understanding its current logic.**

## B. The approved visual design is mandatory

Use `assets/01-approved-dashboard-reference.png` as the primary design reference.
Use `assets/03-expanded-sidebar-user-reference.png` as the exact interaction/layout reminder for the always-expanded sidebar.
Use `assets/02-custom-application-journey-reference.png` for the two application paths and custom browser journey.

Implement the **Indian Civic Identity** direction:
- dark teal/green expanded left sidebar;
- warm cream/ivory canvas;
- deep green/teal actions and headings;
- restrained saffron/orange accents;
- white/ivory cards, subtle warm borders and restrained shadows;
- Manrope headings and Inter body (or compatible already-configured local fonts);
- same temple/government-building + Indian flag + tricolour hero artwork from the approved dashboard visual. Search the repository for the existing matching asset first. If absent, use the supplied hero reference asset as a temporary visual reference and clearly keep the artwork as a replaceable asset. Do not substitute unrelated pastel illustrations.

Translate `design-tokens.json` into the existing Tailwind/CSS token system. Avoid scattered hex values.

### Sidebar — do not miss this

On desktop, the sidebar is **always expanded** and all nine labels are visible at all times:
1. Dashboard
2. New Application
3. Explore Services
4. My Applications
5. Documents
6. Approvals
7. AI Assistant
8. Notifications
9. Settings

Do not collapse it to icons or move the options into a hamburger menu on desktop. On narrow mobile only, a labelled slide-over drawer/overlay is acceptable so all options remain discoverable.

### Topbar

Keep these topbar controls:
- global service/application search;
- `New Application` dropdown containing the six category options;
- `Explore Services` dropdown containing All Services, By Category, By Department, By State, Popular Services and Recently Added;
- notification control;
- profile menu.

The topbar duplicates New Application and Explore Services already in the sidebar. This is intentional and approved.

Dropdown requirements:
- click/tap to open;
- close on outside click, Escape, second click and route navigation;
- correct focus/keyboard navigation and active state;
- no clipping behind hero or content cards;
- hover can be an optional enhancement but cannot be the only way to open.

## C. Dashboard implementation

Route: `/dashboard`

Build the visual hierarchy shown in the approved reference:
1. Shared shell and topbar.
2. Hero welcome section with same temple/flag/tricolour artwork on the right and copy/action on the left.
3. Four metrics: Active Applications, In Review, Documents Pending, Action Required.
4. Your Applications list.
5. Quick Actions: Explore Services, Upload Documents, Ask AI Assistant, Track Application.

Bind metrics and application rows to actual data. Do not hardcode the illustrative numbers or fake names/statuses seen in generated artwork. Handle first-time/empty state gracefully.

## D. New Application — preserve the six-category entry point

Route: `/applications/new`

On initial load show the six categories, with category search:
- Education & Scholarships
- Certificates
- Licenses & Permits
- Benefits & Subsidies
- Government Registrations
- Other Services

Do not replace this page with a dropdown or direct flat service selector. Category selection should lead to `/services?category=...` and show the filtered directory. `Other Services` should make custom discovery easy to reach.

## E. Explore Services — make it state- and department-aware

Route: `/services`

This must be a real service discovery directory, not just a list of cards.

Required:
- Search by service name, synonyms, description, department and keyword.
- All six category tiles.
- State selection, default All India.
- Department selection that reacts to selected state/jurisdiction.
- Category, application mode, official availability and CivicFlow integration filters.
- Sort by relevance/name. Only show Popular/Recently Added if data actually supports it.
- Clear filters and correct URL query parameter behaviour.
- Empty state for no matching service, with primary action `Can't find your service? Create a custom application`.
- Cards clearly distinguish government service availability from CivicFlow integration capability.

Suggested query examples (adapt to current conventions):
- `/services?view=state`
- `/services?view=department`
- `/services?state=bihar`
- `/services?state=bihar&department=...`
- `/services?category=certificates&state=bihar`

Do not make up service counts, popularity, fees, deadlines, eligibility, document lists or official department mappings.

## F. Service details page

Route: `/services/[slug]`

Include:
- title, category, state/jurisdiction and responsible department when verified;
- official source/portal with source attribution;
- verified description/overview;
- eligibility;
- required documents;
- application mode and issuing authority levels when verified;
- application process, important dates and FAQs only when official data exists;
- capability panel explaining what CivicFlow can do.

Primary action depends on capability:
- `native`: Apply Now → existing `createApplication` → unique application workspace.
- `external_assisted`: Open in CivicFlow browser workspace, if the Browser Agent supports the origin and workflow.
- `guided_only`: View official portal / guided steps. Do not promise automation.
- `needs_verification`: do not present an unverified portal as official.

## G. Custom service journey — core product requirement

A custom service request is **not merely a ticket asking the CivicFlow team to add a service**. It creates a custom application session when the citizen chooses to proceed.

Entry points:
- service directory no-results state;
- `/applications/new` → Other Services;
- Explore Services dropdown / dashboard action;
- AI Assistant.

Build the UI flow described in `SERVICE_DISCOVERY_AND_CUSTOM_APPLICATION.md`:
1. Citizen describes request naturally (example: `I need a caste certificate in Bihar`).
2. Ask for missing state/jurisdiction; district/department/issuing level only where relevant. Do not ask for personal sensitive information at discovery stage.
3. AI interprets request and returns typed service candidates with official source references and unresolved ambiguities.
4. CivicFlow verifies official portal/source and displays state, department, issuing authority level and actual capability.
5. If a service has a supported browser workflow, create a custom application and open the official portal inside the CivicFlow workspace.
6. If only guided instructions are supported, retain the custom application context but do not fake browser automation.
7. When user selects a candidate, create a unique application with `applicationMode: custom` or extend the existing Application model. Navigate to `/applications/[id]/workspace`.

Example scenario to test: `I need a caste certificate in Bihar`. The UI must not hardcode this one example. Verify exact Bihar service details and official URL before treating them as factual; if unverified, show a candidate/needs-verification state.

## H. Embedded browser workspace — the differentiator

Route: `/applications/[id]/workspace`

Keep the desktop three-part workspace:
1. Left: application/service context and progress steps.
2. Center: actual embedded Browser Agent session with portal tab and browser controls.
3. Right: AI companion with progress, inspected fields, missing information, field mapping proposals and safe help.

Use `BROWSER_WORKSPACE_SPEC.md` exactly for session states, takeover, pause/resume, field grounding, consent, security and evidence.

Important:
- The central panel must show the real Browser Agent session when connected; do not invent a screenshot of an official portal or present a local fake as live.
- When not connected, clearly state `Demo preview — not connected to a live government portal` or `Browser assistance unavailable for this service`.
- Browser controls must either work or be disabled with a reason. No dead refresh/back/forward/expand buttons.
- Browser Agent returns grounded, current DOM/accessibility field handles. AI may propose mappings; Core authorizes; Browser executes only approved actions.
- Citizen can Take Control, Pause AI, Resume AI and Stop Session.
- Final submission, payment, declarations and other irreversible actions require explicit user confirmation at the time of action.
- A submission click alone is not proof of submission. Use confirmed evidence or `submission_unconfirmed`.

## I. Existing workflow pages — preserve real state

Keep these routes and existing app-specific data:
- `/applications`
- `/applications/[id]/form`
- `/applications/[id]/review`
- `/applications/[id]/tracking`
- `/approvals`
- `/assistant`
- `/documents`
- `/settings`

Use the same unique application ID across the workflow. Each application has independent form, document, review, approval, browser-session and tracking state. Do not create shared mutable global fields that cause one application to overwrite another.

Review gate:
- every required checklist item must pass;
- declaration consent is explicit and per application;
- unchecking any required item revokes review readiness;
- approval must not bypass review;
- server/Core must enforce these rules, not only the UI.

Documents:
- selecting a local file does not mean it was securely uploaded or verified;
- preserve demo labels until real object storage and verification are connected;
- show actual verification status only when backend evidence exists.

Tracking:
- source and verification date of statuses must be visible;
- distinguish portal confirmed from user-entered/demo state;
- no invented receipt/reference number.

## J. Integration architecture

Follow `TEAM_ARCHITECTURE_AND_CONTRACTS.md`.

- Member 1/Core owns authoritative data and policy.
- Member 2/AI is a separate service, returns structured reasoning/proposals/citations, does not run Playwright or write Core DB.
- Member 3/Browser is a separate service, runs Playwright and returns grounded page/session events, does not import LangGraph or write Core DB.
- Use versioned Pydantic/JSON Schema/OpenAPI contracts and mocks.
- Core orchestrates, validates permissions, redacts sensitive information and manages application state.
- Build Core against mock AI/Browser clients so frontend work continues independently.
- Use correlation IDs, idempotency keys, bounded timeouts and contract tests.

Do not merge all agents into one untestable module. Do not introduce direct internal imports between AI and Browser services.

## K. Responsive and accessibility requirements

- Desktop at 1536×1024 is primary visual target.
- Tablet at 1080px and mobile at 760px must have deliberate layouts.
- All essential sidebar links must remain available on mobile.
- Labels must be visible; placeholders are not labels.
- Keyboard access for nav/dropdown, clear focus indicators and reduced-motion support.
- Contrast must be sufficient; state is not communicated by color alone.
- Minimum touch target around 44px.
- Use semantic headings, buttons, links, inputs and live announcements for validation/status changes.

## L. Implementation order

1. Audit repository and report what will be reused/preserved.
2. Add/align design tokens and fonts.
3. Implement shared app shell, full expanded sidebar, topbar and dropdowns.
4. Redesign Dashboard.
5. Redesign New Application preserving six categories.
6. Implement Explore Services: state, department, category and integration filters.
7. Implement Service Details and capability-specific CTAs.
8. Implement custom service discovery and custom application creation.
9. Implement the three-panel workspace with proper demo/live integration states.
10. Redesign My Applications, Form, Review, Approvals, Tracking, Assistant, Documents and Settings.
11. Integrate typed Core/AI/Browser clients and mocks without breaking independent development.
12. Run lint, typecheck, tests and production build. Test responsive routes and primary workflows.

Do not stop after the dashboard. This request is for the whole website redesign.

## M. Final report

When finished, report:
- files/components changed;
- route-by-route status;
- logic/state behaviour preserved;
- new interaction behaviours;
- API/service integrations completed vs mocked;
- known limitations;
- tests, typecheck, lint and production build results.

Never claim tests passed unless you ran them and saw successful output. Never claim a portal is live or automated unless a real Browser Agent session proved it.
