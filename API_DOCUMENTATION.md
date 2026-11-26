# NagrikSetu SWD Microservice — REST API Documentation

Base URL: `http://127.0.0.1:8004/api/v1/swd` (also available under `/api/swd`)
Interactive Swagger Documentation: `http://127.0.0.1:8004/docs`

---

## 1. Authentication & User Management

### `POST /auth/register`
Registers a new citizen user.
- **Request Body:**
```json
{
  "citizen_id": "CIT-KA-9905",
  "email": "new.citizen@example.com",
  "password": "StrongPassword@2026",
  "full_name": "Anand R. Naik",
  "phone": "9876543210",
  "district": "Bengaluru Urban",
  "annual_income": 120000.0,
  "caste_category": "SC"
}
```
- **Response (200 OK):**
```json
{
  "id": 5,
  "citizen_id": "CIT-KA-9905",
  "email": "new.citizen@example.com",
  "full_name": "Anand R. Naik",
  "role": "CITIZEN",
  "is_active": true
}
```

### `POST /auth/login`
Authenticates a user and issues a JWT token.
- **Request Body:**
```json
{
  "email": "admin@nagriksetu.local",
  "password": "AdminPass@2026"
}
```
- **Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "ADMINISTRATOR",
  "citizen_id": "ADM-SWD-001",
  "email": "admin@nagriksetu.local",
  "name": "SWD Welfare Administrator"
}
```

---

## 2. Scheme Catalogue & Eligibility Engine

### `GET /schemes`
Returns all published social welfare schemes.
- **Query Parameters:** `category_id` (optional), `search` (optional)
- **Response (200 OK):** Array of Scheme objects.

### `POST /schemes/{id}/eligibility-check`
Runs deterministic preliminary criteria assessment.
- **Request Body:**
```json
{
  "citizen_attributes": {
    "annual_income": 180000,
    "caste_category": "SC",
    "residence_state": "Karnataka",
    "education_level": "Undergraduate",
    "age": 21
  }
}
```
- **Response (200 OK):**
```json
{
  "scheme_id": 1,
  "scheme_name": "Post-Matric Scholarship for SC/ST and Backward Classes Students",
  "preliminary_status": "LIKELY_ELIGIBLE",
  "summary_explanation": "You appear to meet the preliminary eligibility criteria based on the information provided.",
  "disclaimer": "Final eligibility and approval are subject to verification by the authorized department.",
  "satisfied_criteria": [...],
  "unmet_criteria": []
}
```

---

## 3. Applications & Dossier Tracking

### `POST /schemes/{id}/applications`
Submits an application for a welfare scheme.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
```json
{
  "citizen_id": "CIT-KA-9901",
  "citizen_name": "Ramesh Kumar Nayak",
  "citizen_phone": "9845012345",
  "annual_income": 180000.0,
  "caste_category": "SC",
  "residence_district": "Bengaluru Urban",
  "disability_percentage": 0.0,
  "bank_account_number": "SBIN0040123991",
  "bank_ifsc": "SBIN0040123"
}
```
- **Response (200 OK):**
```json
{
  "id": 12,
  "application_number": "SWD-APP-2026-A1B2C3",
  "scheme_id": 1,
  "citizen_name": "Ramesh Kumar Nayak",
  "status": "SUBMITTED",
  "is_duplicate_suspect": false
}
```

### `GET /public/track-status/{application_number}`
Public minimal non-login tracking lookup.
- **Response (200 OK):**
```json
{
  "application_number": "SWD-APP-2026-A1B2C3",
  "scheme_name": "Post-Matric Scholarship",
  "masked_citizen_name": "R***** K**** N****",
  "district": "Bengaluru Urban",
  "current_status": "SUBMITTED",
  "submission_date": "2026-11-18",
  "notice": "DEMO MODE — Preliminary Public Status Lookup"
}
```

---

## 4. Simulated Direct Benefit Transfer (DBT)

### `GET /dbt/dashboard-stats`
Returns aggregated DBT metrics.
- **Headers:** `Authorization: Bearer <admin_token>`
- **Response (200 OK):**
```json
{
  "total_approved_beneficiaries": 3,
  "total_payments_processed": 3,
  "successful_transactions": 2,
  "failed_transactions": 1,
  "pending_transactions": 0,
  "total_simulated_disbursed": 37000.0,
  "allocated_budget": 10000000.0,
  "remaining_budget": 9963000.0,
  "notice": "DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED."
}
```

### `POST /dbt/batch-process`
Executes atomic simulated batch disbursement.
- **Headers:** `Authorization: Bearer <admin_token>`
- **Request Body:**
```json
{
  "beneficiary_ids": [1, 2],
  "remarks": "Monthly Stipend Batch Disbursal",
  "fail_beneficiary_ids": []
}
```
- **Response (200 OK):**
```json
{
  "batch_reference": "BATCH-DBT-2026-4F2A1",
  "total_processed": 2,
  "successful_count": 2,
  "failed_count": 0,
  "total_amount_disbursed": 37000.0,
  "notice": "DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED.",
  "results": [...]
}
```

### `GET /dbt/batch-report`
Downloads simulated DBT audit ledger in CSV format.
- **Response:** CSV attachment with transaction references and demo notice.
