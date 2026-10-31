# Member 2 — AI Agent Handoff Specification

## 1. Executive Summary & Ownership Boundaries
Member 2 owns the **AI Agent Service** located in `backend/services/ai_agent/`.
- **Member 2 Scope**: Intent recognition, service discovery reasoning, RAG & source interpretation, eligibility rule evaluation, document requirements analysis, and structured form field guidance.
- **Member 1 (Core API) Scope**: Sole authority for application persistence, user identity, policy decisions, review gates, and state machine transitions.
- **Member 3 (Browser Agent) Scope**: Isolated Playwright browser contexts, live portal inspection, DOM grounding, and authorized form execution.

**Crucial Safety Rule**: Member 2 and Member 3 do **not** communicate directly and do **not** share internal database connections. All inter-service communication flows through versioned HTTP contracts defined in `civicflow-contracts`.

---

## 2. Service Contract & Endpoints to Implement in `backend/services/ai_agent`

The AI Agent runs independently on port **8001**. Member 2 must implement or complete the following endpoints:

### 2.1 Health & Capabilities
- `GET /health/live` -> `{"status": "alive", "service": "ai_agent"}`
- `GET /health/ready` -> `{"status": "ready", "service": "ai_agent", "contract_version": "1.0.0", "mode": "langgraph"}`
- `GET /internal/v1/agent/capabilities` -> List of active models, tools, and reasoning capabilities.

### 2.2 Intent & Service Discovery
- `POST /internal/v1/agent/services/discover`
  - **Input (`ServiceDiscoveryRequest`)**:
    ```json
    {
      "query": "I need a caste certificate in Bihar",
      "state_code": "BR",
      "district": "Patna",
      "user_context": {}
    }
    ```
  - **Output**: Ranked candidate services with confidence score, source URL citation, and jurisdiction verification.

### 2.3 Eligibility Reasoning
- `POST /internal/v1/agent/eligibility/evaluate`
  - **Input (`EligibilityRequest`)**:
    ```json
    {
      "service_id": "caste-certificate-bihar",
      "applicant_attributes": {
        "residence_state": "Bihar",
        "category": "EBC",
        "annual_income": 180000
      }
    }
    ```
  - **Output (`EligibilityResult`)**: Structured eligibility status (`eligible`, `ineligible`, `needs_more_info`), cited legal rules, and specific follow-up questions for the citizen.

### 2.4 Document Requirements
- `POST /internal/v1/agent/documents/requirements`
  - **Input (`DocumentRequirementsRequest`)**:
    ```json
    {
      "service_id": "income-certificate-mh",
      "applicant_category": "OBC",
      "salaried": false
    }
    ```
  - **Output**: Mandatory vs. optional document checklist with valid alternative proofs and accepted formats.

### 2.5 Multi-turn Assistant & Form Guidance
- `POST /internal/v1/agent/turn`
  - **Input (`AgentTurnRequest`)**:
    ```json
    {
      "conversation_id": "conv-uuid",
      "message": "What should I enter under family income?",
      "application_context": {
        "application_id": "app-uuid",
        "service_id": "mock-citizen-certificate",
        "status": "draft",
        "sanitized_data": { "applicantName": "Aarav Patil" }
      }
    }
    ```
  - **Output (`AgentTurnResponse`)**:
    ```json
    {
      "reply_text": "Enter the gross annual income of all earning family members as certified by your Tahsildar or salary slip.",
      "proposed_actions": [
        {
          "field_name": "income",
          "proposed_value": "250000",
          "rationale": "Extracted from uploaded income certificate",
          "requires_citizen_confirmation": true
        }
      ]
    }
    ```

---

## 3. Strict Security & Data Privacy Boundaries

1. **Zero Secret Handling**:
   - **Passwords, OTPs, CAPTCHAs, Payment PINs/Cards, and e-Sign secrets must NEVER be passed to Member 2**.
   - If an input appears to be an authentication credential, Member 2's preflight filter must reject it.
2. **Advisory Authority Only**:
   - AI outputs are untrusted proposals. The AI cannot approve an application, cannot change application status to `submitted`, and cannot initiate payment.
   - Core API acts as the gatekeeper; the citizen must explicitly approve actions.
3. **No Direct Database Access**:
   - Do not connect to Core PostgreSQL or Redis directly from `ai_agent`. Core API will pass all necessary sanitized application context in the request payload.

---

## 4. How to Run & Develop Independently

```powershell
# In repository root:
$env:PYTHONPATH = "backend/contracts/civicflow_contracts;backend/services/ai_agent"
uv run --project backend/services/ai_agent uvicorn app.main:app --port 8001 --reload
```

### Required Environment Variables (`backend/services/ai_agent/.env`)
```env
OPENAI_API_KEY=your-api-key       # or GOOGLE_API_KEY / ANTHROPIC_API_KEY
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o
REDIS_URL=redis://localhost:6379/0  # For LangGraph checkpointing only
```

---

## 5. Contract Verification Commands
To test contract adherence:
```powershell
uv run --project backend/services/ai_agent pytest backend/services/ai_agent/tests -q
```
