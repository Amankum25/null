# CivicFlow — Product Vision and Agreed Context

## 1. Product definition

CivicFlow is a general-purpose, AI-powered public-service application assistant. It helps a citizen discover a government service, understand the process, and complete an application with AI guidance and controlled browser automation.

The first demo service is Maharashtra Post-Matric Scholarship, but the architecture and user experience must support many Indian central/state/department services. Do not bake Maharashtra or scholarship assumptions into the global app shell.

## 2. Two equally important application paths

### Path A — Existing service in CivicFlow

1. Citizen enters through Dashboard, New Application, or Explore Services.
2. Citizen browses by category, state, department, search, popularity or recency.
3. Citizen opens service details and reviews eligibility, required documents, process and official source.
4. If the service has a native CivicFlow integration, `Apply Now` creates an independent application using the existing `createApplication` flow.
5. If it is available only on an external portal, show the external/guided option rather than pretending it is native.

### Path B — Custom service / custom filling

This is a core product capability, not an afterthought and not merely a service-catalog feedback form.

1. Citizen cannot find the service or deliberately chooses `Custom application` / `Can't find your service?`.
2. Citizen describes the task naturally, for example: `I need a caste certificate in Bihar`.
3. CivicFlow asks for only the missing routing facts (state, optional district, issuing level, department if known). Avoid collecting identity details at service-discovery stage.
4. AI interprets the request and proposes candidate service matches.
5. CivicFlow verifies candidates against official government sources and identifies state, department, issuing authority level, official URL and portal type.
6. CivicFlow creates a custom application session, not a catalog-only service request.
7. The official portal opens inside an embedded browser tab/pane within the CivicFlow workspace.
8. Browser Agent inspects accessible DOM/labels and returns grounded field information.
9. AI reasons about form questions and suggests field mappings/answers using only approved user-provided data and safe context.
10. Browser Agent executes only approved, grounded actions. The citizen can take control, pause AI, resume or stop.
11. Sensitive credentials and challenge responses are entered directly by the citizen; never transmit them to AI, agent state or logs.
12. The citizen reviews the filled form and explicitly confirms before any irreversible submission.
13. CivicFlow records portal evidence. If a submission result cannot be confirmed, the state is `submission_unconfirmed`, not `submitted`.

A custom session should be useful even if a portal is not automatable: show the official source and provide guided/manual steps. Never hide a capability limitation.

## 3. Service capability language

Availability and integration capability are separate dimensions.

- `availability`: whether the government service is officially available for the relevant state/jurisdiction.
- `integrationMode`: what CivicFlow itself can do with that service.

Recommended integration modes:
- `native`: CivicFlow has an implemented, tested service workflow.
- `external_assisted`: the service is external; CivicFlow can open/inspect the official portal and assist within browser-agent capability.
- `guided_only`: official information is verified, but the portal cannot be safely automated; provide instructions and link.
- `not_integrated`: known service but no current supported workflow.
- `needs_verification`: candidate/source could not yet be verified.

Do not use one generic `available` badge to conflate these states.

## 4. Navigation and core routes

Keep the current Next.js App Router and these paths unless the existing repository contains a newer canonical equivalent:

- `/dashboard`
- `/applications/new`
- `/services`
- `/services/[slug]`
- `/applications`
- `/applications/[id]/workspace`
- `/applications/[id]/form`
- `/applications/[id]/review`
- `/applications/[id]/tracking`
- `/approvals`
- `/assistant`
- `/documents`
- `/settings`

The `/applications/new` landing page must show the six established categories first. Do not replace it with a dropdown or an undifferentiated service list.

## 5. Six permanent service categories

1. Education & Scholarships
2. Certificates
3. Licenses & Permits
4. Benefits & Subsidies
5. Government Registrations
6. Other Services

`Other Services` must remain a visible option, with an obvious route to custom service discovery.

## 6. Existing team structure

- Member 1: Core backend, DB, auth, API, app state, integration, UI/route integration and infrastructure.
- Member 2: AI reasoning service (LangGraph), intent understanding, service discovery, official-source retrieval, RAG, eligibility and field-mapping proposals.
- Member 3: Browser service (Playwright/Chromium), session lifecycle, portal navigation, accessible DOM inspection, element grounding, approved field fill, screenshots/stream, user takeover/resume and evidence.

Member 2 and Member 3 must be able to work independently and integrate later. Use versioned contracts. Do not create circular dependencies or shared database ownership.

## 7. Non-negotiable trust principles

- AI is advisory; Core enforces policy and authorization.
- Browser execution must be grounded in inspected page elements, not guessed selectors.
- User consent is required for consequential and irreversible actions.
- No CAPTCHA/MFA bypass.
- No passwords, OTPs, session cookies or authentication secrets in AI prompts/state/logs.
- Do not claim a document is verified merely because it has been uploaded.
- Do not claim an official application was submitted without reliable portal evidence.
- Make demo vs real integration status explicit in UI copy.
