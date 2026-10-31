# CivicFlow — Product Flow Diagrams

## 1. Main navigation and application paths

```mermaid
flowchart TD
  D[Dashboard] --> N[New Application]
  D --> E[Explore Services]
  N --> C[Six service categories]
  C --> S[Service directory filtered by category]
  E --> S
  S -->|Existing catalog match| SD[Service details]
  S -->|No match / custom request| CR[Custom service description]
  SD -->|Native CivicFlow service| A[Create unique application]
  SD -->|External assisted| A
  CR --> AI[AI interprets request]
  AI --> SRC[Verify official service and source]
  SRC --> CH{Capability verified?}
  CH -->|Native| A
  CH -->|External portal supported| A
  CH -->|Guided only| G[Official link and manual guidance]
  CH -->|Not verified| Q[Ask clarification / needs verification]
  A --> W[Application workspace]
  W --> F[Fill / inspect portal]
  F --> R[Review and user confirmation]
  R --> T[Submit only with explicit consent]
  T --> TR[Track with evidence or submission_unconfirmed]
```

## 2. By State and By Department

```mermaid
flowchart TD
  S[Explore Services] --> V{Browse view}
  V --> BS[By State]
  V --> BD[By Department]
  BS --> ST[Select state / All India]
  ST --> DE[Load applicable departments for jurisdiction]
  BD --> ST2[Select jurisdiction first if needed]
  ST2 --> DP[Select department]
  DE --> C[Filter service_availability records]
  DP --> C
  C --> R[Show matching service cards and integration capability]
  R -->|No match| CU[Create custom application]
```

## 3. Custom application and three-member orchestration

```mermaid
sequenceDiagram
  participant Citizen
  participant UI as CivicFlow UI
  participant Core as Member 1 / Core
  participant AI as Member 2 / AI Service
  participant Browser as Member 3 / Browser Service

  Citizen->>UI: Describe service + state
  UI->>Core: Create custom application request
  Core->>Core: Persist unique application + correlation ID
  Core->>AI: Interpret request / discover official candidates
  AI-->>Core: Intent, candidates, sources, ambiguities
  Core-->>UI: Candidate service(s) and verified capability
  Citizen->>UI: Select service candidate
  UI->>Core: Confirm selection
  Core->>Core: Validate source and policy
  Core->>Browser: Create isolated session for approved origin
  Browser-->>Core: Session ID + safe portal metadata
  Core-->>UI: Embedded browser session ready
  Browser->>Browser: Inspect accessible DOM/labels
  Browser-->>Core: Grounded fields + page state
  Core->>AI: Safe field metadata + approved user data references
  AI-->>Core: Proposed field mappings / questions
  Core-->>UI: Show proposals for review
  Citizen->>UI: Approve or edit proposed data
  UI->>Core: Confirm allowed fill actions
  Core->>Browser: Execute grounded approved actions
  Browser-->>Core: Action result and verification
  Core-->>UI: Updated progress and evidence
  Citizen->>UI: Explicit final confirmation
  UI->>Core: Authorize final action
  Core->>Browser: Submit action (only when permitted)
  Browser-->>Core: Portal evidence or ambiguous result
  Core-->>UI: submitted_confirmed OR submission_unconfirmed
```

## 4. Key rule

AI does not directly control Playwright. Browser does not decide user authorization. Core coordinates and enforces the contracts/policy. The citizen remains in control.
