# CivicFlow backend

Three separately packaged FastAPI services share the versioned `civicflow-contracts` package. Frontend routes and the six-category service catalogue remain in the existing Next.js application.

## Independent startup

Install `uv`, then follow each guide under `docs/`. Each service listens on its assigned port: Core 8000, AI 8001, Browser 8002. Health checks are `/health/live` and `/health/ready`.

## Full local infrastructure

From the repository root:

```powershell
docker compose -f backend/infrastructure/docker-compose.yml up --build
```

The current Core data stores and browser sessions are scaffolds in process memory. Compose provisions PostgreSQL, Redis and MinIO, but these services are not yet wired to durable Core models, browser workers or object uploads. See [architecture.md](docs/architecture.md) for the exact remaining scope.

## Ownership and integration

See `docs/member-1-guide.md`, `docs/member-2-guide.md`, `docs/member-3-guide.md`, `docs/contract-versioning.md`, and `docs/integration-guide.md`. Create the three feature branches and `integration/backend-main` from the agreed repository base; branch creation is intentionally a team-level operation so existing local work is not switched unexpectedly.
