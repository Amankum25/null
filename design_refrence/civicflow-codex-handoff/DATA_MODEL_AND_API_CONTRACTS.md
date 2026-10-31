# CivicFlow — Suggested Data Model and API Contracts

These structures are a design guide. Codex must first inspect the actual application store, service catalog, backend and types. Reuse/extend existing models where possible; do not create duplicate tables or incompatible parallel types.

## 1. Key entities

### Service catalog

```ts
export type Service = {
  id: string;
  slug: string;
  canonicalName: string;
  description: string;
  primaryCategoryId: string;
  aliases: string[];
  createdAt: string;
  updatedAt: string;
};

export type ServiceAvailability = {
  id: string;
  serviceId: string;
  stateId: string | null; // null can represent a central/all-India scope
  departmentId: string | null;
  availability: "available" | "not_available" | "unknown";
  integrationMode:
    | "native"
    | "external_assisted"
    | "guided_only"
    | "not_integrated"
    | "needs_verification";
  applicationMode: "online" | "offline" | "both" | "unknown";
  officialPortalUrl?: string;
  officialServiceUrl?: string;
  issuingLevels?: string[];
  verifiedAt?: string;
  sourceIds: string[];
};
```

### Custom application session

```ts
export type CustomApplication = {
  id: string;
  userId: string;
  mode: "custom";
  originalRequest: string;
  normalizedIntent?: string;
  stateId?: string;
  district?: string;
  departmentId?: string;
  selectedServiceId?: string;
  selectedAvailabilityId?: string;
  integrationMode:
    | "native"
    | "external_assisted"
    | "guided_only"
    | "not_integrated"
    | "needs_verification";
  officialSourceIds: string[];
  browserSessionId?: string;
  status:
    | "request_received"
    | "interpreting_request"
    | "needs_clarification"
    | "service_candidates_found"
    | "awaiting_service_selection"
    | "service_verified"
    | "ready_to_open_portal"
    | "portal_open"
    | "form_inspected"
    | "filling"
    | "needs_user_input"
    | "ready_for_review"
    | "awaiting_user_confirmation"
    | "submitting"
    | "submitted_confirmed"
    | "submission_unconfirmed"
    | "completed"
    | "blocked"
    | "failed";
  createdAt: string;
  updatedAt: string;
};
```

The actual implementation may use an existing `Application` entity with `applicationMode: "custom"`. Prefer that if it already supports per-application state and unique IDs.

## 2. State and department model

- `State`: stable ID/code, name, kind (`state`/`union_territory`).
- `Department`: stable ID, government level, jurisdiction, official name, display name, aliases, official source.
- `ServiceAvailability`: join between a service, state/jurisdiction and department with its own source, issuing levels, application mode and integration capability.
- Do not store a single static department list in React. Query/filter the department data according to selected state and scope.

## 3. API boundary examples

Names below are illustrative contracts. Preserve existing naming conventions if the backend already has an API standard.

### Core — service directory

`GET /api/services?state=bihar&department=general-administration&category=certificates&sort=relevance`

Returns service cards with separate `availability` and `integrationMode` fields and official source references.

### Core — custom application creation

`POST /api/applications/custom`

Request:

```json
{
  "requestText": "I need a caste certificate in Bihar",
  "stateCode": "IN-BR",
  "district": null,
  "departmentId": null,
  "additionalContext": null
}
```

Response (example only):

```json
{
  "applicationId": "app_opaque_id",
  "status": "interpreting_request",
  "applicationMode": "custom",
  "correlationId": "corr_opaque_id"
}
```

### AI — intent interpretation

`POST /v1/discovery/interpret`

Request includes `correlationId`, contract version, request text, state/district hints and safe catalog context. Response includes normalized intent, needed clarifying questions and service candidate records. Candidate records must include source evidence and unresolved items. AI must not return an unreferenced fabricated official URL.

### AI — form mapping proposal

`POST /v1/forms/propose-mappings`

Input: safe form inspection metadata from Browser plus approved, non-secret user/profile fields.

Output: proposals with `elementHandle`, `fieldLabel`, `valueReference`, `reason`, `riskLevel`, `requiresUserConfirmation`, and optional source reference. Do not include passwords/OTP/CAPTCHA/auth secrets.

### Browser — create session

`POST /v1/sessions`

Request:

```json
{
  "correlationId": "corr_opaque_id",
  "applicationId": "app_opaque_id",
  "approvedOrigin": "https://verified-government-host.example",
  "startUrl": "https://verified-government-host.example/service-path"
}
```

Response includes `browserSessionId`, `sessionState`, safe origin information and supported controls. Core must validate `approvedOrigin` from verified service/source data; never accept arbitrary LLM-supplied URL.

### Browser — inspect and execute

- `POST /v1/sessions/{id}/inspect`
- `POST /v1/sessions/{id}/actions`
- `POST /v1/sessions/{id}/take-control`
- `POST /v1/sessions/{id}/pause`
- `POST /v1/sessions/{id}/resume`
- `POST /v1/sessions/{id}/stop`
- `GET /v1/sessions/{id}/evidence`

Browser actions must use a current grounded element handle and expire when the page changes. Core authorizes actions and carries user-approval information.

## 4. Event envelope

All service events should carry:

```json
{
  "eventId": "evt_opaque_id",
  "eventType": "browser.field_inspected",
  "contractVersion": "1.0.0",
  "correlationId": "corr_opaque_id",
  "applicationId": "app_opaque_id",
  "occurredAt": "2026-10-31T10:00:00+05:30",
  "sourceService": "browser-agent",
  "payload": {}
}
```

Do not put secrets, raw cookies, OTPs or unrestricted page contents into event payloads.

## 5. Idempotency, retries and errors

- Use idempotency keys for application/session creation and consequential actions.
- Use bounded timeouts and safe retries only for idempotent calls.
- Propagate correlation IDs.
- Return typed errors: invalid contract version, unauthorized origin, stale element, browser unavailable, AI unavailable, needs clarification, source unverified, user confirmation required.
- Do not retry non-idempotent submit clicks blindly.
