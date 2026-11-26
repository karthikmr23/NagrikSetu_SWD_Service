# NAGRIKSETU — SWD REST API SPECIFICATION
## Comprehensive Endpoints & Schemas Reference

All routes are prefixed with `/api/swd` (or available directly via Swagger docs at `http://localhost:8004/docs`).

### 1. Health Endpoint (FR-COM-001)
* **`GET /health`**
  * Description: Service status, database type, and microservice version.
  * Response: `{"service": "swd-service", "status": "healthy", "database": "mysql_8.0", "version": "2.0.0"}`

### 2. Schemes & Categories (FR-SWD-001 to FR-SWD-006)
* **`GET /api/swd/categories`**: List all active welfare categories.
* **`POST /api/swd/categories`**: Create category (`SWD_ADMIN` role required).
* **`GET /api/swd/schemes`**: Public catalogue of published schemes. Supports query params: `category_id`, `search`, `status_filter`, `skip`, `limit`.
* **`GET /api/swd/schemes/{scheme_id}`**: Full scheme detail including criteria and required documents.
* **`POST /api/swd/schemes`**: Create new scheme with nested rules and documents (`SWD_ADMIN`).
* **`PUT /api/swd/schemes/{scheme_id}`**: Update scheme particulars (`SWD_ADMIN`).
* **`DELETE /api/swd/schemes/{scheme_id}`**: Deactivate scheme (`status = INACTIVE`).

### 3. Eligibility Engine (FR-SWD-007 to FR-SWD-013)
* **`POST /api/swd/schemes/{scheme_id}/eligibility-check`**:
  * Body: `{"citizen_attributes": {"annual_income": 180000, "caste_category": "SC", "residence_state": "Karnataka"}}`
  * Response: Evaluates each rule, returns `preliminary_status` (`LIKELY_ELIGIBLE`, `NOT_ELIGIBLE`, `INSUFFICIENT_INFORMATION`), lists of satisfied/unmet/unknown criteria, missing fields, and mandatory disclaimer.
* **`GET /api/swd/citizens/{citizen_id}/eligibility`**: Batch assessment of all active published schemes against citizen profile.

### 4. Application Workflow (FR-SWD-014 to FR-SWD-021)
* **`POST /api/swd/schemes/{scheme_id}/applications`**:
  * Submits citizen application dossier. Checks open date window, flags potential duplicates for human review, commits transaction, and publishes `SCHEME_APPLICATION_CREATED`.
* **`GET /api/swd/applications/{citizen_id}`**: Retrieve citizen's own application portfolio (ownership enforced).
* **`GET /api/swd/applications/{application_id}/details`**: Get full dossier details, uploaded documents, and history timeline.
* **`POST /api/swd/applications/{application_id}/documents`**: Upload supplementary PDF/Image documents.

### 5. Administration & Review (FR-SWD-018 to FR-SWD-019)
* **`GET /api/swd/admin/dashboard`**: Real database counts: schemes, status breakdown, beneficiaries, sanctioned total, and recent queue.
* **`GET /api/swd/admin/applications`**: Admin queue with filtering by status and duplicate suspect flag.
* **`POST /api/swd/admin/applications/{application_id}/request-information`**: Request citizen clarification or documents.
* **`POST /api/swd/admin/applications/{application_id}/decision`**: Record official approval or rejection with mandatory remarks. Automatically creates `beneficiaries` record upon approval.

### 6. Beneficiaries & Recommendations
* **`GET /api/swd/beneficiaries`**: Beneficiary ledger and sanctioned DBT totals.
* **`POST /api/swd/recommendations/match`**: Integration endpoint for Member 3's Recommendation Engine and Agentic AI.
