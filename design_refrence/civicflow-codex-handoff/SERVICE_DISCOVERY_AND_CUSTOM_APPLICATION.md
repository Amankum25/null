# Explore Services, By State, By Department and Custom Application

## 1. Purpose

Explore Services must support normal catalog discovery and a flexible custom-service journey. A citizen may ask for a service in any state, including a service not yet natively integrated into CivicFlow.

Example: `I need a caste certificate in Bihar`.

The goal is not only to add a catalog record. The citizen must be able to start a custom application session, identify the official portal, and—where technically and safely supported—complete the portal form inside CivicFlow's embedded browser workspace with AI assistance.

## 2. Explore Services directory layout

Recommended desktop layout:

- Page heading: `Explore Government Services` with a short explanation.
- Global search: service name, synonyms, department or keyword.
- A state picker with an explicit `All India` default and selected-state chip.
- Six category tiles using the permanent category taxonomy.
- Filter column: State, Department, Category, Application Mode, Integration Capability, Availability.
- Results area with sort by Most Relevant, Popular (only when backed by analytics), Recently Added (only when backed by verified `createdAt`), Name.
- Service cards show title, state/jurisdiction, department, concise verified description, application mode, availability and CivicFlow integration mode.
- `Can't find your service? Create a custom application` call to action remains prominent even when results are non-empty.

Do not use fictional result counts or popularity rankings. If analytics are absent, hide Popular or label it as a future option rather than fabricating a ranking.

## 3. By State

`By State` should open a state-selection view/picker and then filter `/services` using query parameters, e.g.:

- `/services?state=bihar`
- `/services?state=maharashtra`

Requirements:
- Support India-wide services as well as state-specific services.
- Use a normalized `stateId`/code rather than free-text labels as the primary join key.
- The service list updates after state selection; department choices are constrained to that state and any applicable central departments.
- Provide `All India` and clear-filter behavior.
- Do not persist a selected state as a global user preference unless the user explicitly chooses that preference. A route filter can be remembered per view, not used to silently exclude services everywhere.
- Use a maintained state/UT reference list in data. Avoid hardcoded state lists repeated in UI components.

## 4. By Department

Department selection is state-aware and should be data-driven.

Requirements:
- A department belongs to one government level/jurisdiction and can be associated with many services.
- Departments can have official display names and aliases. Do not assume names are uniform across states.
- Allow a `Central / All India` scope and a selected state scope.
- Display department name, jurisdiction and relevant service count only when count is computed from actual results.
- Department is not the same as issuing authority level. Keep separate fields such as `issuingLevels`: Circle/Block, Sub-Division, District, etc., when confirmed by an official source.
- Do not invent department-to-service mappings.

## 5. By Category

Reuse the six approved categories. Categories are CivicFlow's discovery taxonomy; they are not necessarily the exact wording used by government departments. Each service may have one primary category and optional secondary tags.

## 6. Service record and state-specific availability are separate

A service can have different official sources, departments, required documents, application modes and authority levels across states. Do not model one generic service record as though it is universally identical.

Recommended normalized data model (adapt to current database):

### `services`
- `id`, `slug`, `canonicalName`, `description`, `primaryCategoryId`, `synonyms[]`, `createdAt`, `updatedAt`.

### `states`
- `id`, `code`, `name`, `kind` (state / union_territory), `isActive`.

### `departments`
- `id`, `stateId` nullable for central, `level` (central / state / district / local), `officialName`, `displayName`, `aliases[]`, `officialSourceUrl`.

### `service_availability`
- `id`, `serviceId`, `stateId` nullable for India-wide, `departmentId`, `availabilityStatus`, `integrationMode`, `applicationMode`, `officialPortalUrl`, `officialServiceUrl`, `issuingLevels[]`, `verifiedAt`, `verifiedBy`, `sourceRecordId`.

### `service_sources`
- `id`, `serviceAvailabilityId`, `sourceType`, `url`, `title`, `retrievedAt`, `verificationStatus`, `notes`, `contentHash` (if appropriate).

### `service_requests` (catalog/product feedback, optional distinct capability)
- Citizen suggestions to expand the catalog. This is not the active custom application session. Keep this table distinct from `applications`.

## 7. Custom application journey — required UX

### Entry points

- `/services` empty/no-result state: `Can't find your service?`
- New Application → Other Services.
- Dashboard quick action, e.g. `Describe a service`.
- AI Assistant: `Start a custom application`.

### Step 1 — Describe the service

Form fields:
- Required: What government service do you need? (natural language textarea)
- Required or inferable: State / jurisdiction.
- Optional: District / city.
- Optional: Department (if known).
- Optional: Issuing level (Circle/Block, Sub-Division, District, etc.) only where relevant.
- Optional: Additional detail.

Do not ask for personal identity numbers, passwords, OTPs, document scans or other sensitive application data during service discovery.

### Step 2 — AI interpretation

AI should return a typed object:
- normalized service intent/name;
- state/jurisdiction;
- department candidates with reasons and source citations;
- service candidates with official URLs and cited evidence;
- missing routing questions;
- confidence/ambiguity for internal decision handling (do not present an uncalibrated numeric confidence to the citizen).

If multiple plausible services or levels exist, show the candidate options and ask the citizen to choose. Never silently choose an authority level that materially changes the service.

### Step 3 — Verify official service and portal

The Core service should retain source URLs and verification metadata. Prefer official government domains and sources. The browser agent may inspect the user-selected official portal but cannot declare a website official solely based on its appearance.

Show to the citizen:
- service name;
- state/jurisdiction;
- responsible department (if verified);
- issuing authority level(s) (if verified);
- official portal/source link;
- when the source was last verified (if stored);
- what CivicFlow can currently do.

### Step 4 — Capability decision

Render one of the following truthful states:

1. **Native CivicFlow application** — native workflow implemented; create application and use the native form.
2. **External portal — guided browser assistance** — open portal inside browser workspace; AI and browser assistance are limited to supported/grounded interactions.
3. **Official information only** — show official link and guided steps; browser form automation is not currently supported.
4. **Needs verification** — no trustworthy official service/source confirmed. Ask for clarifying jurisdiction or explain that the service cannot yet be verified. Do not launch an arbitrary guessed website.

### Step 5 — Create custom application session

When citizen chooses to proceed, create an application with:
- unique `applicationId`;
- `applicationMode: custom`;
- original user request;
- normalized intent;
- jurisdiction/state and optional district;
- selected service match/source;
- integration mode;
- discovery evidence;
- state machine status such as `service_discovered` or `ready_to_open_portal`.

Then navigate to `/applications/[id]/workspace`.

Do not convert an unverified service request into a ready-to-submit application.

## 8. State and department filters in route parameters

Suggested URL patterns (adapt to existing query naming):

- `/services?view=state`
- `/services?view=department`
- `/services?state=bihar`
- `/services?state=bihar&department=general-administration`
- `/services?category=certificates&state=bihar`
- `/services?sort=recent`

Filters must be shareable through URL state and have clear/reset actions. Validate query values against known IDs.

## 9. Example: caste certificate in Bihar

This example is for illustrating the architecture only. The actual responsible department, service labels, portal URLs, rules, issuing authority levels, documents and availability must be checked from official Bihar sources at runtime or from a verified catalog record before showing them as facts.

A possible flow:

1. User describes `I need a caste certificate in Bihar`.
2. AI extracts `service intent = caste certificate`, `state = Bihar`.
3. Catalog checks if there's a Bihar-specific service availability record.
4. If absent, official-source discovery looks for the relevant official portal and authority. It may identify multiple issuing levels; ask the citizen to choose when required.
5. Core stores selected source and evidence.
6. If Browser Agent supports the portal and policy allows it, start an embedded session. Otherwise show the official link and guided/manual path.
7. Do not present the service as a native CivicFlow integration until one has been built and tested.

## 10. Failure and edge cases

- No state supplied and request is state-specific: ask state before searching.
- User asks for service but state not supported in CivicFlow catalog: run discovery, don't drop the request.
- More than one service matches: ask user to choose.
- Service name varies by state: use synonyms and state aliases.
- Official portal unavailable: show last verified source time if available; do not claim live availability.
- Portal has CAPTCHA, OTP or MFA: the user completes it directly; no bypass.
- Browser cannot inspect form: fall back to guided instructions or manual entry.
- Service has multiple office/issuing levels: ask citizen to select appropriate option when needed.
- Portal blocks automation or terms disallow it: show information/manual link and respect restriction.
