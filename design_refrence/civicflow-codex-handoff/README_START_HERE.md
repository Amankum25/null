# CivicFlow — Codex Redesign Handoff

This is the current, approved design and product handoff for redesigning the existing CivicFlow website. It supersedes the earlier blue/pastel concept pack. Use the included references and specifications as the source of truth.

## Start here

1. Open the existing CivicFlow repository in Codex. **Do not create a new project or replace the repo.**
2. Add this complete handoff folder to Codex context (or extract it beside the repository).
3. Start with `CODEX_IMPLEMENTATION_PROMPT.md`.
4. Use `assets/01-approved-dashboard-reference.png` as the visual source of truth for the dashboard shell, `assets/02-custom-application-journey-reference.png` for the custom-service journey, and `assets/03-expanded-sidebar-user-reference.png` for the always-expanded sidebar requirement.
5. Open `prototype/index.html` in a browser for a lightweight, clickable interaction reference. It is a static front-end prototype; it is not connected to the CivicFlow backend, AI service or Playwright worker.

## What this package contains

- `CODEX_IMPLEMENTATION_PROMPT.md` — complete step-by-step implementation prompt.
- `PRODUCT_VISION_AND_CONTEXT.md` — what CivicFlow is, what it is not, and the agreed product behaviour.
- `DESIGN_SYSTEM.md` — approved Indian Civic Identity visual language and responsive shell.
- `design-tokens.json` — canonical design token values.
- `ROUTE_AND_SCREEN_MAP.json` — the existing Next.js routes and screen requirements.
- `SERVICE_DISCOVERY_AND_CUSTOM_APPLICATION.md` — By State, By Department, service catalog, custom request, service discovery and capability states.
- `BROWSER_WORKSPACE_SPEC.md` — embedded government-portal browser, AI assistant panel, field grounding, user takeover and safe submission.
- `TEAM_ARCHITECTURE_AND_CONTRACTS.md` — Member 1/2/3 boundaries and integration contracts.
- `DATA_MODEL_AND_API_CONTRACTS.md` — proposed entities, state machines and API examples. These are design contracts to reconcile with current code, not a mandate to duplicate existing models.
- `ACCEPTANCE_CHECKLIST.md` — functional, UX, accessibility, security and integration acceptance criteria.
- `assets/` — approved visual references, logo and the cropped temple/flag hero reference.
- `prototype/` — a clickable, offline-friendly UI concept to demonstrate the navigation and key journeys.

## Product and design decisions already made

- CivicFlow is a general-purpose AI public-service application assistant, not a scholarship-only site.
- It supports both existing catalog services and custom, natural-language service requests.
- Custom service means: discover a government service, verify its official portal, open it inside CivicFlow's browser workspace, and assist with the real portal form. It is **not merely a ticket asking the CivicFlow team to add the service**.
- The dashboard uses the Indian Civic Identity theme: dark teal expanded sidebar, cream/ivory canvas, green actions, restrained saffron accents, and the same temple + Indian flag + tricolour hero artwork from the approved reference.
- All nine sidebar destinations remain visible. The sidebar does not collapse into a hidden menu on desktop.
- `New Application` and `Explore Services` also appear in the horizontal top bar as dropdown actions.
- The existing six New Application categories remain the first step.
- The workspace remains a three-part experience: application progress/context, embedded browser, and AI companion. On desktop all three should be visible together.
- Member 2 (AI) and Member 3 (Browser) develop independently behind versioned contracts. Member 1/Core orchestrates and owns authoritative application state.

## Important interpretation

A government service may exist on an official portal even when CivicFlow has not integrated its browser automation. The UI must distinguish:

1. **Native in CivicFlow** — CivicFlow's own workflow is implemented and available.
2. **External portal with guided browser assistance** — the official service exists; CivicFlow can open/inspect it and assist where the browser agent supports the portal.
3. **Official information only** — verified service information is available, but the portal workflow is not supported.
4. **Needs verification** — CivicFlow cannot yet verify a trustworthy official service/source.

Never imply that a government service is fully automated merely because AI found its website.

## Prototype limitations

The prototype uses illustrative sample records and a simulated browser view. It does not make official government claims, connect to live portals, store files, call AI, run Playwright, or submit applications. Codex must connect the production UI to the existing repository's real state/services, not copy sample data as authoritative facts.
