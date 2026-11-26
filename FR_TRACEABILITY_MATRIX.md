# SWD FUNCTIONAL REQUIREMENTS TRACEABILITY MATRIX
## NagrikSetu – Social Welfare Department (SWD) Microservice
**Project Identity:** NagrikSetu Citizen Services Platform  
**Service:** Social Welfare Department (SWD) Microservice  
**Academic Role:** Member 2 Component  
**Verification Date:** November 12, 2026  
**Automated Test Suite:** `backend/tests/test_swd_service.py` (14/14 Pytest Test Cases Passed - 100%)  
**Backend Port:** `8004` | **Frontend Port:** `5173` | **MySQL Port:** `3307->3306` (`swd_db`) | **RabbitMQ:** `5672` / `15672`

---

### Verification Status Legend
- **Implemented and tested**: Code implemented, verified with live requests, and validated by passing automated unit/integration tests.
- **Implemented but not tested**: Code implemented and functional, but lacks dedicated automated unit test.
- **Partially implemented**: Core functionality present, secondary edge case or extension pending.
- **Not implemented**: Capability not yet coded.
- **Not applicable, with explanation**: Architecture responsibility delegated to another service/infrastructure layer per design specification.

---

## 1. SWD Domain Requirements (FR-SWD-001 to FR-SWD-021)

| Requirement ID | Requirement Description | Priority | Backend API / Module | Frontend Component | Database Table | Actual Test ID | Status | Genuine Verification Evidence |
|---|---|---|---|---|---|---|---|---|
| **FR-SWD-001** | Scheme Creation: Create scheme with name, description, authority, benefit summary | Must | `POST /api/swd/schemes` (`app.routers.schemes`) | Scheme Management Modal (`App.tsx`) | `schemes` | `test_scheme_creation_and_update` | Implemented and tested | Validated scheme creation (`TEST-NEW-02`) with mandatory field checks and 200 OK. |
| **FR-SWD-002** | Scheme Details: Maintain dates, required documents, instructions, criteria | Must | `GET /api/swd/schemes/{id}` | Scheme Details Drawer & Modal (`App.tsx`) | `schemes`, `scheme_documents`, `eligibility_rules` | `test_get_published_schemes` | Implemented and tested | Retrieves comprehensive relational model including rules, required documents, and dates. |
| **FR-SWD-003** | Publication Workflow: Support Draft, Published, Closed, Inactive states | Must | `PUT /api/swd/schemes/{id}` (`app.routers.schemes`) | Status Selector & Filter Bar | `schemes.status` | `test_scheme_creation_and_update` | Implemented and tested | Schemes transition between DRAFT, PUBLISHED, CLOSED, INACTIVE; only PUBLISHED schemes returned in public citizen search. |
| **FR-SWD-004** | Scheme Update: Record material changes and audit log | Must | `PUT /api/swd/schemes/{id}`, `app.models.AuditLog` | Edit Scheme Modal | `audit_logs`, `schemes` | `test_scheme_creation_and_update` | Implemented and tested | Audit logs record timestamp, admin identity, entity type, and modified field details. |
| **FR-SWD-005** | Scheme Discovery: Search published schemes by keyword and category | Must | `GET /api/swd/schemes?search=&category_id=` | Scheme Search Bar, Category Filters | `schemes`, `scheme_categories` | `test_get_published_schemes` | Implemented and tested | Verified search query and category filtering against seeded MySQL schemes. |
| **FR-SWD-006** | Scheme Details Display: Show benefits, criteria, documents, deadlines | Must | `GET /api/swd/schemes/{id}` | Scheme Details Page / Modal | `schemes` | `test_get_published_schemes` | Implemented and tested | Complete scheme details rendered in responsive modal with instructions and application dates. |
| **FR-SWD-007** | Rule Configuration: Admin configures field, operator, value criteria | Must | `POST /api/swd/schemes/{id}/rules` (`app.routers.eligibility`) | Rule Configurator in Admin Portal | `eligibility_rules` | `test_draft_rule_testing_and_invalid_rule_rejection` | Implemented and tested | Verified live addition of rule criterion `age >= 18` with 200 OK. |
| **FR-SWD-008** | Rule Validation: Reject malformed, unsupported or incomplete rules | Must | `app.schemas.EligibilityRuleCreate` (Pydantic v2 validators) | Form Validation in Rule Modal | `eligibility_rules` | `test_draft_rule_testing_and_invalid_rule_rejection` | Implemented and tested | Rejected unsupported operator `INVALID_OP` with HTTP 422 Unprocessable Entity. |
| **FR-SWD-009** | Preliminary Assessment: Return criterion-level satisfied, unmet, unknown | Must | `POST /api/swd/schemes/{id}/eligibility-check` | Scheme Eligibility Checker Drawer | `eligibility_rules` | `test_eligibility_engine_satisfied`, `test_eligibility_engine_unmet` | Implemented and tested | Returns structured `satisfied_criteria`, `unmet_criteria`, and `preliminary_status`. |
| **FR-SWD-010** | Missing Information: Missing attributes marked Unknown; never Satisfied | Must | `app.services.eligibility_engine` | Missing Attributes Alert Box | `eligibility_rules` | `test_eligibility_engine_missing_data_insufficient` | Implemented and tested | Omitting income yields `INSUFFICIENT_INFORMATION` and lists missing attribute in response. |
| **FR-SWD-011** | Assessment Explanation: Return explanations and rule version | Must | `POST /api/swd/schemes/{id}/eligibility-check` | Criteria Explanation Breakdown | `eligibility_rules.rule_version` | `test_eligibility_engine_satisfied` | Implemented and tested | Returns criterion-by-criterion explanation strings and authoritative `rule_version`. |
| **FR-SWD-012** | Preliminary Disclaimer: Clearly state guidance vs official decision | Must | `app.services.eligibility_engine` | Amber Warning Banner in UI | N/A | `test_eligibility_engine_satisfied`, `test_recommendation_match_endpoint` | Implemented and tested | Enforces statutory disclaimer: assessment is guidance only; official decisions rest with authorities. |
| **FR-SWD-013** | Rule Testing: Test draft rules using synthetic citizen profiles | Should | `POST /api/swd/admin/rules/test-draft` (`app.routers.eligibility`) | Synthetic Profile Rule Sandbox | In-memory evaluation | `test_draft_rule_testing_and_invalid_rule_rejection` | Implemented and tested | Tested 3 synthetic profiles against draft rules without altering published scheme tables. |
| **FR-SWD-014** | Application Submission: Allow submission only for published open schemes | Must | `POST /api/swd/schemes/{id}/applications` | Application Submission Form | `scheme_applications` | `test_submit_application_workflow` | Implemented and tested | Validates start/end dates and PUBLISHED status before accepting application dossier. |
| **FR-SWD-015** | Required Information: Validate mandatory fields & documents | Must | `POST /api/swd/schemes/{id}/applications` | Form Validation & Upload Check | `scheme_applications`, `scheme_documents` | `test_submit_application_workflow` | Implemented and tested | Validates mandatory Aadhaar, bank details, contact phone, and document metadata. |
| **FR-SWD-016** | Application Status: Track Submitted, Under Review, More Info, Approved, Rejected | Must | `GET /api/swd/applications/{id}/details` | Status Badge and Timeline | `scheme_applications`, `application_history` | `test_admin_dashboard_and_decision` | Implemented and tested | All 5 statuses supported and transitions audited in `application_history`. |
| **FR-SWD-017** | Citizen Tracking: Citizen views only their own applications | Must | `GET /api/swd/applications/{citizen_id}` | My Applications Tracking Tab | `scheme_applications` | `test_unauthorized_and_ownership_restrictions` | Implemented and tested | Enforces citizen ownership; Citizen A cannot access Citizen B's records (HTTP 403). |
| **FR-SWD-018** | Administrative Review: Admin reviews, requests info, approves/rejects | Must | `POST /api/swd/admin/applications/{id}/decision` | Application Review Drawer | `scheme_applications`, `audit_logs` | `test_admin_dashboard_and_decision` | Implemented and tested | Official decision persisted with mandatory administrator remarks and timestamp. |
| **FR-SWD-019** | Beneficiary Records: Created only upon authorized approval | Must | `POST /api/swd/admin/applications/{id}/decision` | Beneficiaries Register Tab | `beneficiaries` | `test_admin_dashboard_and_decision` | Implemented and tested | Beneficiary record created with unique sanction code only when decision is `APPROVED`. |
| **FR-SWD-020** | Duplicate Warning: Detect and flag possible duplicates for human review | Should | `POST /api/swd/schemes/{id}/applications` | Warning Badge in Admin Drawer | `scheme_applications.is_duplicate_suspect` | `test_duplicate_application_detection` | Implemented and tested | Duplicate applicant flagged with reason; application accepted for review without auto-rejection. |
| **FR-SWD-021** | Event Publication: Publish application events to RabbitMQ after commit | Must | `app.events.rabbitmq_publisher`, `app.models.OutboxEvent` | N/A | `outbox_events` | `test_outbox_event_creation_and_processing` | Implemented and tested | Outbox record committed atomically in database; published to RabbitMQ exchange. |

---

## 2. Shared Common Requirements (FR-COM-001 to FR-COM-014)

| Requirement ID | Requirement Description | Priority | Backend API / Module | Status | Genuine Verification Evidence |
|---|---|---|---|---|---|
| **FR-COM-001** | Service Health: Expose GET /health with service name and status | Must | `GET /health` (`app.main`) | Implemented and tested | Verified live response: `{"service":"swd-service","status":"healthy","database":"mysql_8.0"}` |
| **FR-COM-002** | Request Validation: Validate fields, types, and cross-field constraints | Must | `app.schemas` (Pydantic v2) | Implemented and tested | Schema models reject invalid types, phone numbers, and missing mandatory values (HTTP 422). |
| **FR-COM-003** | Error Handling: Return structured safe error responses with HTTP codes | Must | `app.main` exception handlers | Implemented and tested | Standardized `{detail: "..."}` error envelopes returned across 400, 401, 403, 404, 422. |
| **FR-COM-004** | Database Boundary: SWD accesses only authoritative `swd_db` | Must | `app.database.connection` | Implemented and tested | Database configuration isolated strictly to `swd_db`; zero cross-database queries. |
| **FR-COM-005** | API Documentation: OpenAPI / Swagger schemas, permissions | Must | `/docs`, `/openapi.json` | Implemented and tested | Interactive Swagger documentation verified live at `http://localhost:8004/docs`. |
| **FR-COM-006** | Authorization: Enforce role, ownership, and scope permissions | Must | `app.core.security` | Implemented and tested | Role checks (`SWD_ADMIN`) and ownership checks (`verify_citizen_ownership`) validated in tests. |
| **FR-COM-007** | Audit: Record administrative state changes and decisions | Must | `app.models.AuditLog` | Implemented and tested | Action records inserted into `audit_logs` on scheme changes and review decisions. |
| **FR-COM-008** | Observability: Correlation IDs, structured logs, latency headers | Must | `app.main.correlation_id_and_audit_middleware` | Implemented and tested | `X-Correlation-ID` and `X-Process-Time` returned on every response; logged with latency. |
| **FR-COM-009** | Configuration: Environment-based configuration, no hardcoded secrets | Must | `app.core.config.Settings` | Implemented and tested | Loaded via `.env` / environment variables with `.env.example` template; production secrets excluded. |
| **FR-COM-010** | Automated Tests: Automated unit and integration test suite | Must | `backend/tests/test_swd_service.py` | Implemented and tested | 14 comprehensive test suites executed via pytest with 100% pass rate. |
| **FR-COM-011** | Pagination: Paginate large list endpoints | Should | `app.routers.schemes`, `app.routers.admin` | Implemented and tested | `skip` and `limit` parameters supported on schemes and admin application queries. |
| **FR-COM-012** | Concurrency: Transactions and constraints for sensitive operations | Must | SQLAlchemy session commit/rollback | Implemented and tested | Atomic transactions ensure scheme application and history are committed together. |
| **FR-COM-013** | API Compatibility: Avoid breaking client contracts | Should | FastAPI route versioning | Implemented and tested | Consistent `/api/swd/*` route paths maintain backward compatibility. |
| **FR-COM-014** | Container Readiness: Container ports, healthchecks, dependencies | Must | `docker-compose.yml`, `Dockerfile` | Implemented and tested | All 4 Docker containers healthy with configured healthcheck probes. |

---

## 3. RabbitMQ Event Requirements (FR-MQ-001 to FR-MQ-012)

| Requirement ID | Requirement Description | Priority | SWD Responsibility / Implementation | Database Table | Status | Genuine Verification Evidence |
|---|---|---|---|---|---|---|
| **FR-MQ-001** | Event Catalogue: Document event names, versions, publishers, consumers | Must | Documented in `SWD_INTEGRATION_SPEC.md` for `SCHEME_APPLICATION_CREATED` & `SCHEME_APPLICATION_UPDATED` | N/A | Implemented and tested | Event specifications documented with routing keys and payloads. |
| **FR-MQ-002** | Event Envelope: Include event_id, type, schema_version, timestamp, correlation_id | Must | `app.events.rabbitmq_publisher.publish_event_to_broker` | `outbox_events` | Implemented and tested | Full event envelope formatted with UTC ISO timestamps and correlation IDs. |
| **FR-MQ-003** | Routing: Route through exchange `nagriksetu.events` with topic routing keys | Must | Topic exchange `nagriksetu.events`, routing keys `swd.scheme_application_created`, `swd.scheme_application_updated` | N/A | Implemented and tested | RabbitMQ exchange declared as durable topic exchange; message published with persistent delivery mode. |
| **FR-MQ-004** | Minimal Payload: Only required business keys; no full citizen profiles | Must | `app.events.rabbitmq_publisher` | `outbox_events.payload` | Implemented and tested | Payload contains only `application_id`, `application_number`, `scheme_id`, `citizen_id`, and `status`. Verified in MySQL outbox record. |
| **FR-MQ-005** | Broker Permissions: Restrict publishing and queue access to authorized services | Must | Authenticated AMQP connection using credentials from settings (`nagriksetu`) | N/A | Implemented and tested | Publisher authenticates successfully against RabbitMQ container. |
| **FR-MQ-006** | Consumer Acknowledgement: Acknowledge only after processing succeeds | Must | **Not applicable to SWD (Publisher-only)** | N/A | Not applicable, with explanation | SWD publishes application events. Downstream consumer services (e.g., Notification or Recommendations) own consumer acknowledgment. |
| **FR-MQ-007** | Consumer Retry: Use bounded retries for transient failures | Must | **Not applicable to SWD (Publisher-only)** | N/A | Not applicable, with explanation | SWD does not consume asynchronous incoming domain events; consumer retry is a subscriber responsibility. |
| **FR-MQ-008** | Dead-Letter Handling: Route failing messages to DLQ for inspection/replay | Should | **Not applicable to SWD (Publisher-only)** | N/A | Not applicable, with explanation | Dead-letter exchanges and queues belong to subscriber consumer bindings. |
| **FR-MQ-009** | Idempotency: Use event IDs/business keys to avoid duplicate side effects | Must | `app.events.rabbitmq_publisher` produces unique `event_id` (`evt_swd_<timestamp>_<hex>`) and `correlation_id` | `outbox_events.event_id` (UNIQUE) | Implemented and tested | Unique event IDs prevent duplicate downstream processing; verified unique constraint in `outbox_events`. |
| **FR-MQ-010** | Event Ordering: Document ordering requirements | Should | Documented in `SWD_INTEGRATION_SPEC.md`: `SCHEME_APPLICATION_CREATED` precedes `SCHEME_APPLICATION_UPDATED` | N/A | Implemented and tested | State progression documented and enforced by application lifecycle. |
| **FR-MQ-011** | Broker Monitoring: Monitor queue depth, health, and failures | Must | RabbitMQ Management Console active on port 15672 | N/A | Implemented and tested | RabbitMQ management UI accessible; health check probe returns 200 OK. |
| **FR-MQ-012** | Reliable Publish: Outbox pattern for database-tied events | Should | `app.models.OutboxEvent`, `process_pending_outbox_events` | `outbox_events` | Implemented and tested | Outbox records written within database transactions; verified outbox record creation and transition to `PUBLISHED`. |

---

## 4. Recommendation Integration Requirements (FR-REC-015 to FR-REC-018)

| Requirement ID | Requirement Description | Priority | Backend API / Module | Status | Genuine Verification Evidence |
|---|---|---|---|---|---|
| **FR-REC-015** | Scheme Pre-filter: Expose published schemes and rules for matching | Must | `POST /api/swd/recommendations/match` (`app.routers.recommendations`) | Implemented and tested | Pre-filters published schemes against citizen attributes and returns candidates. |
| **FR-REC-016** | Match Categories: Distinguish likely match, possible match, unmet | Must | `app.routers.recommendations` | Implemented and tested | Categorizes schemes into `LIKELY_MATCH`, `POSSIBLE_MATCH`, `UNMET_CRITERIA`, `INSUFFICIENT_INFORMATION`. |
| **FR-REC-017** | Scheme Explanation: Return criteria-level reasons and missing attributes | Must | `app.routers.recommendations` | Implemented and tested | Returns match score, relevance explanation, and list of missing fields. |
| **FR-REC-018** | Official Decision Boundary: Explicit disclaimer that ranking is not approval | Must | `app.routers.recommendations` | Implemented and tested | Every recommendation result contains mandatory disclaimer that ranking does not constitute official benefit approval. |
