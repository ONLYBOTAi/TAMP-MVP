# Sprint 6: Telematics Ingestion Pipeline

## Sprint Goal
Build and integrate a fully functional data ingestion system for telemetry data, including real-time API endpoints, asynchronous background processing, structured logging, and metadata integration.

## Team Assignments

### 👨‍💻 Tech Lead Evens – Ingestion Pipeline Core + Oversight
**Responsibilities:**
- Oversee Sprint 6 execution and ensure all technical standards are met
- Design and implement core ingestion routes and worker logic
- Supervise cross-service integration points with vehicle-service
- Approve all architecture, commits, PRs

**Assigned Deliverables:**
| Area | Description | Path | Priority |
|------|-------------|------|----------|
| ✅ API Endpoints | Implement POST /ingest and GET /status | routers/telemetry_routes.py | HIGH |
| ✅ Background Worker | Build ingestion_worker.py to consume async telemetry data | workers/ingestion_worker.py | HIGH |
| 🔄 Queue Simulation | Use asyncio.Queue or background_tasks from FastAPI | Within service logic | HIGH |
| 🔁 Vehicle Integration | Fetch/validate vehicle metadata via vehicle-service | services/telematics/core/vehicle_client.py | MED |
| 🧪 Integration Tests | Write tests to validate ingestion flow | tests/integration/test_ingestion.py | HIGH |
| 📑 Review & QA | Final reviewer for all PRs + demo host | N/A | HIGH |

### 👨‍💻 Co-Tech Lead Kenny – Logging, Testing, Support Services
**Responsibilities:**
- Architect and implement logging and telemetry auditing
- Develop supportive test coverage (unit & functional)
- Ensure observability and error traceability in ingestion

**Assigned Deliverables:**
| Area | Description | Path | Priority |
|------|-------------|------|----------|
| 🛠 Structured Logging | Create a custom JSON log formatter for telemetry events | core/logging.py | HIGH |
| 🧪 Unit Tests | Build tests for ingestion_worker.py logic | tests/unit/test_worker.py | HIGH |
| 🔔 Alert Hooks | Create log-level based alert stubs | core/alerts.py | MED |
| 🔐 Security Logging | Ensure failed ingestions, auth failures are logged | Logging middleware | MED |
| 🤝 Sync with Evens | Pair on vehicle-service integration tests | Shared integration endpoints | MED |
| 📦 .env/.sample | Review and finalize .env.sample for Sprint 6 | Root & service folders | LOW |

## Success Criteria
- ✅ Endpoints ingest telemetry and return status
- ✅ Background task processes data from queue
- ✅ All telemetry logs are structured (JSON, traceable)
- ✅ Error cases logged and surfaced
- ✅ Unit + integration tests passing in CI
- ✅ Vehicle-service integration verified
- ✅ All commits merged via PR with reviews

## Coordination Plan
| Task | Owner | Sync Point |
|------|-------|------------|
| API Contract Finalization | Evens ↔ Kenny | Pair programming or async review |
| Test Plan Confirmation | Kenny | Share draft by Day 3 |
| Logging Level Standards | Kenny | Confirm levels/info to log with Evens |
| Metadata Enrichment | Evens | Share schema with Kenny for log context |
| Git PR Reviews | Evens | Approve all merges to dev |
| Sprint Demo Prep | Both | Run live walkthrough on Demo Day |

## Next Steps
1. Pull latest dev & rebase
2. Create Sprint 6 feature branches
3. Confirm logging specifications
4. Start ingestion logic implementation
5. Confirm vehicle schema fields

## Timeline
- Sprint Start: 2025-06-01
- Mid-Sprint Review: 2025-06-07
- Sprint End: 2025-06-14 