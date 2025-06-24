#!/usr/bin/env bash
set -euo pipefail

OWNER="ONLYBOTAi"
REPO="TAMP-MVP"
MILESTONE="Sprint 9"

# 1️⃣ Load Persistence
gh issue create \
  --repo "$OWNER/$REPO" \
  --title "Load Persistence (ORM + Alembic)" \
  --assignee ONLYBOTAi \
  --label "backend,enhancement,sprint-9" \
  --milestone "$MILESTONE" \
  --body $'**Context:** We need to wire up SQLAlchemy ORM models for the Load entity, add Alembic migrations, and expose CRUD endpoints in `services/load_matching`.\n\n**Acceptance Criteria:**\n- SQLAlchemy models defined for Load with fields: id, origin, destination, weight, created_at.\n- Alembic migration script generated and applied in CI.\n- CRUD REST endpoints (`POST /loads`, `GET /loads/{id}`, `PUT /loads/{id}`, `DELETE /loads/{id}`) implemented and documented in Swagger.\n- Unit tests covering model integrity and endpoints with pytest.'

# 2️⃣ Matcher Algorithm MVP
gh issue create \
  --repo "$OWNER/$REPO" \
  --title "Matcher Algorithm MVP" \
  --assignee MokwenaMK \
  --label "algorithm,enhancement,sprint-9" \
  --milestone "$MILESTONE" \
  --body $'**Context:** Implement a basic matching rule engine in `services/matcher` using distance and capacity constraints.\n\n**Acceptance Criteria:**\n- Rule engine that scores potential matches based on Euclidean distance and truck capacity.\n- `/match` endpoint accepts Load and Vehicle payloads and returns top N matches.\n- Background task enqueued via Celery for asynchronous matching.\n- Unit tests for scoring logic and endpoint behavior.'

# 3️⃣ Telematics Data Ingestion & Retention
gh issue create \
  --repo "$OWNER/$REPO" \
  --title "Telematics Data Ingestion & Retention" \
  --assignee ONLYBOTAi \
  --label "telematics,enhancement,sprint-9" \
  --milestone "$MILESTONE" \
  --body $'**Context:** Secure the ingestion endpoint in `services/telematics`, validate incoming GPS pings, and implement retention policies.\n\n**Acceptance Criteria:**\n- POST `/telemetry` endpoint requires JWT auth.\n- Input payload validation (lat, lon, timestamp).\n- Store records in Postgres with TTL of 30 days (via cleanup script or DB policy).\n- Unit tests for auth, validation, and retention behavior.'

# 4️⃣ End-to-End Integration Tests
gh issue create \
  --repo "$OWNER/$REPO" \
  --title "End-to-End Integration Tests" \
  --assignee MokwenaMK \
  --label "test,enhancement,sprint-9" \
  --milestone "$MILESTONE" \
  --body $'**Context:** Verify that all services work together as expected using Docker Compose smoke tests.\n\n**Acceptance Criteria:**\n1. New test script `tests/e2e/smoke_test.py` that:\n   - Brings up all services via `docker compose`.\n   - Hits each `/health` endpoint and asserts healthy.\n   - Creates a Load and Vehicle, triggers a match, and asserts a valid match response.\n2. This smoke test runs in CI on the `sprint/9` branch.'
