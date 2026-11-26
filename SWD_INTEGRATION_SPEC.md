# NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
## Integration Specification & API Architecture Contract

**Service Name:** `swd-service`  
**Identity:** NagrikSetu – Social Welfare Department (SWD) Microservice  
**Academic Role:** Member 2 Component  
**Version:** 2.0.0  
**API Prefix:** `/api/swd/`  
**Base URL:** `http://localhost:8004` (Direct) / `http://localhost:8000/api/swd/` (via API Gateway)  
**Database:** `swd_db` (MySQL 8.0 on port 3307/3306)  
**Event Bus:** RabbitMQ (`nagriksetu.events` exchange)

---

## 1. System Overview & Boundaries

The Social Welfare Department (SWD) microservice manages the full lifecycle of government welfare schemes, configurable rule-based eligibility evaluation, citizen scheme applications, document verification, and beneficiary entitlement records.

### Boundaries:
- **SWD Owns:** Schemes, eligibility rule criteria, required document definitions, citizen welfare applications, review decision records, and beneficiary sanction mandates.
- **Administrative Service Owns:** Core citizen master profiles, household associations, administrative geography.
- **Recommendation Service Owns:** Multi-domain scoring, ranking, and machine-learning matching. SWD provides pre-filtered criteria and preliminary matching evaluation endpoints.
- **Agentic AI Service Owns:** Natural language intent processing and cross-domain tool orchestration.

---

## 2. Authentication & Authorization

All protected endpoints require a JWT Bearer token in the `Authorization` header:
```http
Authorization: Bearer <jwt_access_token>
```

### Roles:
- `CITIZEN`: Can view published schemes, evaluate eligibility, submit applications for their own profile, upload documents, and track application status.
- `SWD_ADMIN`: Full administrative control over schemes, rule configurations, application review decisions, duplicate resolution, and beneficiary registers.

---

## 3. Authoritative REST API Endpoints

### 3.1 Service Health
- `GET /health`
  - Returns service status and database connectivity.
  - Response:
    ```json
    {
      "service": "swd-service",
      "status": "healthy",
      "database": "mysql_8.0",
      "version": "2.0.0",
      "environment": "development"
    }
    ```

### 3.2 Scheme Catalogue & Discovery
- `GET /api/swd/categories`: List all welfare categories (Scholarships, Disability, Pensions, etc.).
- `GET /api/swd/schemes`: Search and list published schemes.
  - Query params: `category_id` (optional integer), `search` (optional string), `status_filter` (optional string).
- `GET /api/swd/schemes/{id}`: Detailed scheme specification, including required documents and eligibility criteria.
- `POST /api/swd/schemes` *(SWD_ADMIN only)*: Create a new scheme.
- `PUT /api/swd/schemes/{id}` *(SWD_ADMIN only)*: Update scheme details, dates, or publication status (`DRAFT`, `PUBLISHED`, `CLOSED`, `INACTIVE`).
- `DELETE /api/swd/schemes/{id}` *(SWD_ADMIN only)*: Deactivate scheme.

### 3.3 Eligibility Rules & Preliminary Assessment Engine
- `POST /api/swd/schemes/{id}/rules` *(SWD_ADMIN only)*: Configure criteria (fields, operators, values).
- `POST /api/swd/schemes/{id}/eligibility-check`: Evaluate citizen attributes against rules.
  - Request:
    ```json
    {
      "citizen_attributes": {
        "annual_income": 180000,
        "residence_state": "Karnataka",
        "caste_category": "SC",
        "education_level": "Undergraduate"
      }
    }
    ```
  - Response:
    ```json
    {
      "scheme_id": 1,
      "scheme_name": "State Scholarship Portal (SSP) Post-Matric Scholarship",
      "preliminary_status": "LIKELY_ELIGIBLE",
      "is_preliminary_guidance": true,
      "satisfied_criteria": [
        {"field": "annual_income", "operator": "LESS_THAN_OR_EQUAL", "expected": "250000", "actual": 180000, "status": "SATISFIED"},
        {"field": "residence_state", "operator": "EQUALS", "expected": "Karnataka", "actual": "Karnataka", "status": "SATISFIED"}
      ],
      "unmet_criteria": [],
      "unknown_criteria": [],
      "missing_fields": [],
      "disclaimer": "This assessment provides preliminary guidance only and does not constitute an official award."
    }
    ```

### 3.4 Applications & Tracking
- `POST /api/swd/schemes/{id}/applications` *(CITIZEN)*: Submit scheme application.
- `GET /api/swd/applications/{citizen_id}`: Citizen lists their own submitted applications.
- `GET /api/swd/applications/{id}/details`: Application timeline, status history, and reviewer notes.
- `POST /api/swd/applications/{id}/documents`: Upload supporting document (PDF/JPG/PNG <= 5MB).

### 3.5 Administrative Review & Beneficiaries
- `GET /api/swd/admin/dashboard` *(SWD_ADMIN)*: Real-time dashboard statistics.
- `GET /api/swd/admin/applications` *(SWD_ADMIN)*: List all applications with duplicate detection flags.
- `POST /api/swd/admin/applications/{id}/decision` *(SWD_ADMIN)*: Record official decision (`APPROVED`, `REJECTED`, `REQUEST_INFO`).
  - Upon `APPROVED`, the system automatically commits a record to `beneficiaries` and publishes RabbitMQ events.
- `GET /api/swd/beneficiaries` *(SWD_ADMIN)*: Retrieve authoritative beneficiary register with Direct Benefit Transfer (DBT) details.

### 3.6 Recommendation Service Integration
- `POST /api/swd/recommendations/match`: Pre-filter schemes for a citizen profile and return ranked matches.
  - Request:
    ```json
    {
      "citizen_attributes": {
        "annual_income": 120000,
        "caste_category": "SC",
        "residence_state": "Karnataka",
        "age": 21
      }
    }
    ```
  - Response:
    ```json
    [
      {
        "scheme_id": 1,
        "scheme_code": "KAR-SSP-POSTMATRIC",
        "scheme_name": "SSP Post-Matric Scholarship",
        "match_category": "LIKELY_MATCH",
        "score": 90,
        "benefit_summary": "100% Course fee reimbursement + monthly stipend",
        "disclaimer": "Preliminary guidance only."
      }
    ]
    ```

---

## 4. RabbitMQ Event Contracts

**Exchange Name:** `nagriksetu.events`  
**Exchange Type:** `topic`  
**Durable:** `true`

### 4.1 Event Envelope Format
```json
{
  "event_id": "evt_swd_1731405000000_a1b2c3d4",
  "event_type": "SCHEME_APPLICATION_CREATED",
  "schema_version": "1.0",
  "timestamp": "2026-11-12T07:15:00.000Z",
  "correlation_id": "SWD-APP-20261112-9901",
  "publisher": "swd-service",
  "payload": {
    "application_id": 12,
    "application_number": "SWD-APP-20261112-9901",
    "scheme_id": 1,
    "scheme_code": "KAR-SSP-POSTMATRIC",
    "citizen_id": "CIT-KA-9901",
    "status": "SUBMITTED",
    "is_duplicate_suspect": false
  }
}
```

### 4.2 Published Events
1. **`SCHEME_APPLICATION_CREATED`**
   - Routing Key: `swd.scheme_application_created`
   - Trigger: Committed when citizen successfully submits an application.
2. **`SCHEME_APPLICATION_UPDATED`**
   - Routing Key: `swd.scheme_application_updated`
   - Trigger: Committed when administrator reviews, updates status, requests info, approves, or rejects.

---

## 5. MySQL Database Architecture (`swd_db`)

The service exclusively interacts with its isolated database `swd_db`:
1. `scheme_categories`: Welfare sectors and themes.
2. `schemes`: Authoritative scheme records and lifecycle statuses.
3. `eligibility_rules`: Configurable validation rules with versioning.
4. `scheme_documents`: Required verification documents per scheme.
5. `scheme_applications`: Citizen applications with duplicate detection flags.
6. `application_documents`: Uploaded document metadata and secure file paths.
7. `application_history`: Complete audit trail of application status changes and remarks.
8. `beneficiaries`: Official sanction and DBT payment records created only on administrative approval.
9. `audit_logs`: Administrative actions log.
10. `outbox_events`: Reliable event outbox for RabbitMQ event durability.
