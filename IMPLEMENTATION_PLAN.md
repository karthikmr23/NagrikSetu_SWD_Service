# NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
## MASTER IMPLEMENTATION PLAN

**Target Deliverable:** `NagrikSetu_SWD_Final.zip`  
**Standard Compliance:** FR-SWD-001 to FR-SWD-021, FR-REC-015 to FR-REC-018, FR-COM-001 to FR-COM-014.

---

### Step 1: Database Engineering (`swd_db`)
- Create `database/swd_db_setup.sql` with strict InnoDB constraints, indexes, UTF8MB4 charset, DATETIME auditing.
- 10 Tables:
  1. `scheme_categories`
  2. `schemes`
  3. `eligibility_rules`
  4. `scheme_documents`
  5. `scheme_applications`
  6. `application_documents`
  7. `application_history`
  8. `beneficiaries`
  9. `audit_logs`
  10. `outbox_events`
- Pre-seed with Karnataka Social Welfare Schemes (SSP Post-Matric, Pre-Matric, Vidyasiri, SSLC Prize Money, Inter-caste Marriage Assistance, Disability Pension, Sandhya Suraksha).
- Create `safe_restore.py` with schema-isolation safeguards.

### Step 2: FastAPI Backend Engine
- `backend/app/main.py`: Entrypoint, CORS, lifespan handlers, middleware for audit logs and correlation IDs.
- `backend/app/core/config.py`: Environment settings (Pydantic Settings).
- `backend/app/core/security.py`: JWT decoding/encoding, RBAC dependencies (`CITIZEN`, `SWD_ADMIN`, `PLATFORM_ADMIN`), ownership validation.
- `backend/app/database/connection.py`: SQLAlchemy engine, session maker, get_db dependency.
- `backend/app/models/`: Declarative models matching the 10 tables.
- `backend/app/schemas/`: Pydantic request/response schemas with strict validation.
- `backend/app/services/eligibility_engine.py`: Configurable rules engine evaluating `SATISFIED`, `UNMET`, `UNKNOWN`.
- `backend/app/services/application_workflow.py`: Status transitions, duplicate warning check, history logging.
- `backend/app/services/document_service.py`: Secure upload, MIME validation, unique hashing, private file streaming.
- `backend/app/events/rabbitmq_publisher.py`: Outbox pattern and RabbitMQ AMQP event publisher.
- `backend/app/routers/`:
  - `schemes.py` (CRUD, publish, search, filters)
  - `eligibility.py` (Preliminary check API for single scheme and citizen batch matching)
  - `applications.py` (Citizen application submission, tracking, history)
  - `admin.py` (Admin dashboard stats, review, request info, record decisions)
  - `beneficiaries.py` (Beneficiary ledger)
  - `recommendations.py` (Recommendation engine integration API)

### Step 3: Frontend Implementation (React + TypeScript + Vite)
- Reproduce the exact visual identity from the WhatsApp screenshot (`media_1794456225900_a164bcfb.jpg`).
- All 12 requested views:
  1. `/swd`: SWD Landing Page (Hero banner, 4 welfare pillars, scheme highlights, quick stats, pre-seeded credentials).
  2. `/swd/schemes`: Scheme Catalogue (Filters by category, target group, search bar, active scheme cards).
  3. `/swd/schemes/:id`: Scheme Details (Benefit breakdown, criteria, required documents, deadlines, direct check & apply buttons).
  4. `/swd/eligibility`: Interactive Eligibility Checker (Profile input, instant preliminary rule-by-rule evaluation, disclaimers).
  5. `/swd/apply/:id`: Scheme Application Form (Multi-step form, declaration, document file uploads).
  6. `/swd/applications`: My Applications (Citizen application portfolio, current status badges).
  7. `/swd/applications/:id`: Application Tracking (Detailed timeline, reviewer notes, uploaded docs, response to info requests).
  8. `/swd/admin`: SWD Admin Dashboard (Real database metrics, status charts, recent queue).
  9. `/swd/admin/schemes`: Scheme Management (CRUD, publish/close toggle).
  10. `/swd/admin/rules`: Eligibility Rule Management (Add/edit criteria operators and thresholds).
  11. `/swd/admin/applications`: Application Review (Workflow action modal: approve, reject, request info).
  12. `/swd/admin/beneficiaries`: Beneficiary Management (Approved disbursements and beneficiary registry).

### Step 4: Platform & Event Integration
- RabbitMQ Event integration (`SCHEME_APPLICATION_CREATED`, `SCHEME_APPLICATION_UPDATED`).
- Outbox pattern for guaranteed delivery.
- Recommendation API (`/api/swd/recommendation/match`).
- API Gateway NGINX configuration snippet for `/api/swd/*`.

### Step 5: Testing & Verification
- Unit & integration tests using `pytest` and FastAPI `TestClient`.
- Verification against SQLite (for fast test isolation) and MySQL 8.0 schema syntax.
- Visual inspection of UI components.

### Step 6: Documentation & Final Packaging
- 14 comprehensive markdown documents.
- Clean packaging into `NagrikSetu_SWD_Final.zip` strictly excluding reference files.
