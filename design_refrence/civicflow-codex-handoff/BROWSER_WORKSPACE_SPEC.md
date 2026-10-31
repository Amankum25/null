# CivicFlow — Embedded Browser and AI-Guided Application Workspace

## 1. Purpose

The workspace is the core differentiator. It should let a citizen interact with an official external government portal without leaving the CivicFlow experience, while AI and browser automation assist the citizen. The UI is a coordinated surface for Core, AI Agent and Browser Agent; it is not an iframe mockup pretending to be connected.

Use `assets/02-custom-application-journey-reference.png` as the visual journey reference. The final workspace should be consistent with `assets/01-approved-dashboard-reference.png`.

## 2. Desktop layout — three visible regions

1. **Left: application context / step rail** (approx. 220–250px)
   - Application/service name and state.
   - Current lifecycle stage: Discover service, Open portal, Fill form, Upload documents, Review, Submit/Track.
   - Application reference and integration capability.
   - Links to native form, documents, review, tracking as relevant.

2. **Center: embedded browser workspace** (flexible, primary region)
   - Browser tab(s) with service/portal label.
   - Address/origin display; clearly identify official domain.
   - Back, forward, refresh only when connected and implemented.
   - Viewport renders the actual Browser Agent session (stream/screenshot/remote view) or honest empty/demo state.
   - Browser security state, connection and session health.
   - Buttons: Take Control, Pause AI, Resume AI, Stop Session. Show only actions that actually work for the current session state.

3. **Right: AI companion / form intelligence** (approx. 300–360px)
   - AI task summary and next step.
   - Detected form fields and field-mapping proposals.
   - Missing information/questions.
   - Suggested values with source/grounding note.
   - Review field values before write.
   - Activity/event log (non-sensitive only).
   - Clear label that AI suggestions are advisory.

## 3. Narrow viewport behaviour

- Tablet: keep browser as primary; move AI/context panels into tabs or drawers without losing access to either.
- Mobile: use a step-based stack or tabs: `Steps`, `Portal`, `AI Help`. Make takeover and consent actions easy to reach.
- Never clip the embedded browser or obscure user control buttons.

## 4. Browser session states

- `not_started`
- `starting`
- `active`
- `inspecting`
- `ready_for_fill`
- `filling`
- `paused_for_user`
- `user_controlled`
- `awaiting_confirmation`
- `submitting`
- `submitted_confirmed`
- `submission_unconfirmed`
- `error`
- `stopped`

The UI must distinguish `submitted_confirmed` from `submission_unconfirmed`. Never mark submitted just because a click was sent.

## 5. Browser controls

- **Take Control:** stops AI actions, leaves browser session visible/usable by the citizen.
- **Pause AI:** blocks new AI-proposed actions; does not necessarily stop page rendering.
- **Resume AI:** only resumes after clear user action and reinspection/re-grounding of the current page.
- **Stop Session:** safely closes/ends the Browser Agent session after confirmation where appropriate.
- **Refresh/Back/Forward:** only enable when the Browser Agent exposes these operations.
- **Open in External Tab:** optional fallback; label that it leaves CivicFlow and that browser assistance may pause.

## 6. Field inspection and grounding

Browser Agent should report grounded information, not generic page guesses:
- DOM/accessibility role/name/label;
- stable element locator or agent-internal element handle;
- element type and required/visible/disabled state;
- surrounding section/group context;
- observed validation message and current value state (redacted where sensitive).

AI returns a proposed field mapping, for example:
- target field identifier/handle;
- source value reference from safe user-provided profile/application data;
- rationale and uncertainty;
- whether user confirmation is required.

Core policy validates permissions and data access. Browser Agent re-checks that the element still exists and the page state is current before acting. Stale element handles must be rejected and re-inspected.

## 7. User control and approval

- Each action is visible as an event: proposed → approved (if needed) → executed → verified/failed.
- Filling ordinary non-sensitive fields can follow user-authorized policy, but any unclear or high-impact field must be confirmed.
- User can pause/take control at any time.
- Final submit, payment, declaration, irreversible action or other consequential portal action requires explicit user confirmation at the point of action.
- Don't silently submit after filling.

## 8. Sensitive data and security

- Passwords, OTPs, CAPTCHA answers, MFA secrets, session cookies and auth tokens never enter LLM prompts, LangGraph state, AI service logs or normal application event logs.
- The citizen enters these directly into the visible browser session.
- Mask sensitive form values in screenshots/streams where feasible and redact any captured evidence before persistence.
- Never bypass CAPTCHA, MFA or portal access restrictions.
- Do not persist browser cookies/session state longer than policy requires; isolate sessions by application/user.
- Browser Agent service must enforce SSRF/URL policy: allowlisted/verified government origins, redirect validation, private-network blocking and safe navigation.
- Do not let AI navigate to arbitrary URLs without Core policy/source validation.

## 9. Evidence and tracking

Capture minimal, privacy-aware evidence:
- verified origin and navigation events;
- page title and timestamp;
- form/section identifiers where safe;
- submission reference/receipt only after it is visibly confirmed by portal;
- sanitized screenshot or text snapshot only when policy permits.

If the portal returns ambiguous state, set `submission_unconfirmed`. Let citizen check the portal/reference manually. Never invent a receipt or status.

## 10. Honest fallback states

If Browser Agent is not integrated or portal cannot be automated:
- show `Browser assistance unavailable for this service`;
- show official portal URL and source metadata;
- offer manual step-by-step guidance;
- keep the custom application session and user notes;
- do not render fake interactive controls or a fabricated official portal page.

If a browser preview is only a static mock/demo, label it prominently as `Demo preview — not connected to a live government portal`.
