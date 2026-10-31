# Service boundaries

| Service | Owns | Must not own |
| --- | --- | --- |
| Core API | Identity, authoritative applications/status, approvals, reviews, documents, audit/tracking | AI reasoning internals or browser runtime |
| AI Agent | Intent, discovery, rule evaluation, cited guidance, action proposals | Application database, browser actions, final approvals |
| Browser Agent | Isolated browser sessions, page inspection, user control, evidence capture | Eligibility, application database/status, final submission approval |
| Contracts | Versioned wire payloads and schemas | Service behavior or persistence |

Only `backend/contracts/civicflow_contracts` is a shared Python import. A service must not import another service's `app` package.
