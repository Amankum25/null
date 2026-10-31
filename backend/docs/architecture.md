# CivicFlow backend architecture

The backend is split into three independently packaged FastAPI services. They share only `civicflow-contracts`; service implementations communicate over HTTP. Core is the sole authority for application status. AI output is a proposal, and browser events are evidence for Core to evaluate.

```mermaid
flowchart LR
  UI[Next.js frontend] -->|REST| Core[Core API :8000]
  Core -->|versioned REST| AI[AI Agent :8001]
  Core -->|versioned REST| Browser[Browser Agent :8002]
  Core --> PG[(PostgreSQL :5432)]
  Core --> MinIO[(MinIO :9000)]
  AI -. optional checkpoints .-> Redis[(Redis :6379)]
  Browser -. ephemeral sessions .-> Redis
  Contracts[[civicflow-contracts 1.0.0]] -. shared package .-> Core
  Contracts -. shared package .-> AI
  Contracts -. shared package .-> Browser
```

Current implementation status: Core API application, auth and document records are in-memory development scaffolds. PostgreSQL, Alembic, durable session/event processing, signed browser callbacks, real LangGraph nodes, and the Playwright worker lifecycle still need implementation before production or multi-user use. The AI and browser endpoints label their current mock mode explicitly.
