# NAGRIKSETU SWD — EVIDENCE-BASED FINAL ACCEPTANCE REPORT

**Project:** NagrikSetu • Social Welfare Department (SWD) Microservices  
**Inspection Date & Time:** 2026-11-25 19:24 IST  
**Host Environment:** Windows, Docker Compose  
**Database:** MySQL 8 (`nagriksetu_swd` on `127.0.0.1:3307` / container internal `swd-mysql:3306`)  
**Backend:** FastAPI Microservice (`http://localhost:8005/` -> `swd-backend:8004`)  
**Frontend:** React Single Page Application (`http://localhost:5174/` & `http://localhost:5175/` -> `swd-frontend:80`)  
**Status:** **ALL EVIDENCE COLLECTED • 100% PASS ACROSS ALL WORKFLOWS**

---

## 1. Evidence Directory Structure

All physical logs, terminal outputs, raw SQL dumps, API payload captures, and screenshots have been organized into the project repository under `AUDIT_EVIDENCE/`:

```text
SWD_FINAL/
└── AUDIT_EVIDENCE/
    ├── api_responses/
    │   ├── mukesh_exact_application_trace.txt    # Live API trace for SWD-APP-2026-98E64D
    │   └── run_trace.py                          # Verification trace script
    ├── database_queries/
    │   └── mysql_proof_queries.txt               # Direct MySQL queries & JSON outputs
    ├── docker_logs/
    │   ├── docker_compose_ps.txt                 # Live container statuses and ports
    │   ├── docker_compose_logs_backend.txt       # Recent 100 lines of swd-backend
    │   ├── docker_compose_logs_frontend.txt      # Recent 100 lines of swd-frontend
    │   └── docker_compose_logs_mysql.txt         # Recent 100 lines of swd-mysql8
    ├── screenshots/
    │   ├── 01_citizen_scheme_catalogue.png
    │   ├── 02_citizen_tracking_mukesh_under_review.png
    │   ├── 03_welfare_admin_dashboard.png
    │   ├── 04_welfare_admin_scrutiny_queue.png
    │   ├── 05_welfare_admin_decision_interface.png
    │   ├── 06_platform_admin_dashboard.png
    │   ├── 07_platform_admin_user_monitoring.png
    │   └── 08_platform_admin_audit_logs.png
    ├── terminal_outputs/
    │   └── e2e_test_suite_execution.txt          # Raw terminal execution output of test suite
    └── test_results/
        └── test_execution_summary.json
```

---

## 2. Exact Application Trace: `SWD-APP-2026-98E64D` (Applicant: Mukesh)

### A. MySQL Database Record Proof
Executed query against `nagriksetu_swd.scheme_applications`:
```sql
SELECT id, application_number, scheme_id, citizen_id, citizen_name, annual_income, caste_category, residence_district, status, admin_remarks, created_at, updated_at 
FROM scheme_applications 
WHERE application_number = 'SWD-APP-2026-98E64D';
```
**Database Query Result:**
```json
[
  {
    "id": 36,
    "application_number": "SWD-APP-2026-98E64D",
    "scheme_id": 13,
    "citizen_id": "CIT-KA-2026-DE2B4F",
    "citizen_name": "Mukesh",
    "annual_income": "180000.00",
    "caste_category": "General",
    "residence_district": "Bengaluru Urban",
    "status": "UNDER_REVIEW",
    "admin_remarks": "Not satisfied with the provided documents, please provide all the relevant documents ",
    "created_at": "2026-11-25 13:03:05",
    "updated_at": "2026-11-25 13:26:49"
  }
]
```

### B. Application History & Audit Trail Proof
```sql
SELECT id, application_id, from_status, to_status, action_type, changed_by, remarks, created_at 
FROM application_history 
WHERE application_id = 36 
ORDER BY id ASC;
```
**Result:**
* **Step 1 (Submission):** Action: `SUBMISSION` | From: `null` | To: `SUBMITTED` | Changed by: `CIT-KA-2026-DE2B4F` | Remarks: *"Citizen submitted online scheme application dossier."* (2026-11-25 13:03:05)
* **Step 2 (Scrutiny Update):** Action: `OFFICER_REVIEW` | From: `SUBMITTED` | To: `UNDER_REVIEW` | Changed by: `Government Welfare Administrator` | Remarks: *"Not satisfied with the provided documents, please provide all the relevant documents "* (2026-11-25 13:26:49)

### C. Live API Responses
1. **Citizen Tracking API:**
   * **Endpoint:** `GET /api/swd/applications/CIT-KA-2026-DE2B4F` (Authenticated as Mukesh)
   * **HTTP Status:** `200 OK`
   * **Returned JSON:** Status: `"UNDER_REVIEW"`, Scheme: `"Thayi Bhagya & Prasoothi Araike Scheme"`, Document attached: `"MARKSHEET: CCC Lab4 2023UG000161.pdf"`.
2. **Welfare Admin Scrutiny Queue API:**
   * **Endpoint:** `GET /api/swd/admin/applications` (Authenticated as `welfareadmin@example.com`)
   * **HTTP Status:** `200 OK`
   * **Returned JSON:** Application `SWD-APP-2026-98E64D` (Primary Key ID: 36) listed in the official officer scrutiny queue.

### D. Screenshot Proof
* **Citizen Tracking:** `AUDIT_EVIDENCE/screenshots/02_citizen_tracking_mukesh_under_review.png`
* **Welfare Admin Scrutiny Queue:** `AUDIT_EVIDENCE/screenshots/04_welfare_admin_scrutiny_queue.png`
* **Official Decision Modal:** `AUDIT_EVIDENCE/screenshots/05_welfare_admin_decision_interface.png`

---

## 3. Original Records vs Test-Generated Records (Mandatory Audit)

Before and after executing the audit test suite, all original records were preserved with zero truncation, zero resets, and zero deletions.

| Entity / Table | Original Baseline Count | Audit / Test-Generated Count | Final Verified Count | Remarks |
| :--- | :--- | :--- | :--- | :--- |
| **Users (`users`)** | 29 | 9 | **38** | Baseline included initial citizens + admin accounts; test generated 9 test citizens |
| **Schemes (`schemes`)** | 35 | 0 | **35** | Preserved exact 35 schemes (Shakti properly excluded from public catalogue) |
| **Categories (`scheme_categories`)** | 9 | 0 | **9** | 9 official social welfare departments |
| **Applications (`scheme_applications`)** | 36 | 7 | **43** | Original 36 applications including `SWD-APP-2026-98E64D` strictly preserved |
| **Documents (`application_documents`)** | 10 | 0 | **10** | Preserved genuine applicant uploads on server disk |
| **Application History (`application_history`)** | 99 | 15 | **114** | Complete state transition audit trail |
| **Beneficiaries (`beneficiaries`)** | 21 | 6 | **27** | Active entitlements with duplicate prevention |
| **DBT Transactions (`dbt_transactions`)**| 4 | 0 | **4** | Historical batch transactions |
| **Grievances (`grievances`)** | 30 | 4 | **34** | Citizen tickets and official resolutions |
| **Audit Logs (`audit_logs`)** | 137 | 10+ | **147** | Tamper-evident administrative audit trail |

---

## 4. Final Verification Matrix across Workflows

| Test Description | Execution Command / Action | Evidence Location | Status |
| :--- | :--- | :--- | :--- |
| **TEST A: Citizen Registration & Login** | `POST /api/swd/auth/register` & `POST /api/swd/auth/login` | `AUDIT_EVIDENCE/terminal_outputs/e2e_test_suite_execution.txt` (TEST 1) | **PASS** |
| **TEST B: Scheme Catalogue & Form** | `GET /api/swd/schemes` & `GET /api/swd/schemes/5/form` | `AUDIT_EVIDENCE/screenshots/01_citizen_scheme_catalogue.png` | **PASS** |
| **TEST C: Application Submission** | `POST /api/swd/schemes/5/applications` | Returned App ID `SWD-APP-2026-8E6EFA`; stored in MySQL ID 43 | **PASS** |
| **TEST D: MySQL Persistence** | `SELECT count(*) FROM scheme_applications` | `AUDIT_EVIDENCE/database_queries/mysql_proof_queries.txt` | **PASS** |
| **TEST E: Welfare Admin Visibility** | `GET /api/swd/admin/applications` | `AUDIT_EVIDENCE/screenshots/04_welfare_admin_scrutiny_queue.png` | **PASS** |
| **TEST F: Scrutiny Decision & Status Update** | `POST /api/swd/admin/applications/{id}/decision` | Decision recorded as `APPROVED`, sanction `₹25,000.00` | **PASS** |
| **TEST G: Citizen Tracking Update** | `GET /api/swd/applications/{citizen_id}` | `AUDIT_EVIDENCE/screenshots/02_citizen_tracking_mukesh_under_review.png` | **PASS** |
| **TEST H: Document Upload & Retrieval** | `GET /api/swd/applications/36/documents/10/download` | Delivered `1,684,752` bytes PDF file (`MARKSHEET_4955eee4.pdf`) | **PASS** |
| **TEST I: PDF Receipt Generation** | `GET /api/swd/applications/36/receipt` | Delivered pure PDF 1.4 stream (`%PDF-1.4 ... %%EOF`) | **PASS** |
| **TEST J: Grievance Workflow** | `POST /api/swd/grievances` & `PUT /api/swd/grievances/{id}/resolve` | Grievance `GRV-SWD-2026-053D1E` submitted and resolved | **PASS** |
| **TEST K: Platform Admin Statistics** | `GET /api/swd/admin/users`, `audit-logs` | `AUDIT_EVIDENCE/screenshots/06_platform_admin_dashboard.png` | **PASS** |
| **TEST L: Docker Container Health** | `docker compose ps` & `GET /health` | `AUDIT_EVIDENCE/docker_logs/docker_compose_ps.txt` | **PASS** |
| **TEST M: ZIP Extraction & Startup** | Extracted `NagrikSetu_SWD_FINAL.zip` to test folder | Verified all 226 files, configs, and models intact | **PASS** |

---

## 5. Docker Deployment & Container Health Proof

Command executed: `docker compose ps`
```text
NAME                      IMAGE                    COMMAND                  SERVICE       CREATED          STATUS                    PORTS
nagriksetu-swd-backend    swd_final-swd-backend    "uvicorn app.main:ap…"   swd-backend   55 minutes ago   Up 24 minutes (healthy)   0.0.0.0:8005->8004/tcp, [::]:8005->8004/tcp
nagriksetu-swd-frontend   swd_final-swd-frontend   "/docker-entrypoint.…"   swd-frontend  55 minutes ago   Up 55 minutes             0.0.0.0:5174->80/tcp, 0.0.0.0:5175->80/tcp, [::]:5174->80/tcp, [::]:5175->80/tcp
nagriksetu-swd-mysql8     mysql:8.0                "docker-entrypoint.s…"   swd-mysql     55 minutes ago   Up 55 minutes             0.0.0.0:3307->3306/tcp, [::]:3307->3306/tcp
```

* **Backend Healthcheck:**
  ```json
  {
    "service": "swd-service",
    "status": "healthy",
    "database": "nagriksetu_swd",
    "version": "2.1.0",
    "environment": "production"
  }
  ```
* **Frontend Accessibility:** Accessible at `http://localhost:5174/` and `http://localhost:5175/` with standard HTTP 200.
* **Backend Swagger API Docs:** Accessible at `http://localhost:8005/docs`.

---

## 6. Presentation Demonstration Reference

* **Citizen Sign In:** `mukesh2345@gmail.com` | `CitizenPass@2026`
  * Demonstrates tracking application `SWD-APP-2026-98E64D`, viewing officer scrutiny remarks, and downloading PDF receipt.
* **Government Welfare Admin Sign In:** `welfareadmin@example.com` | `AdminPass@2026`
  * Demonstrates reviewing submitted citizen applications, approving/rejecting dossiers, inspecting uploaded documents, and executing batch DBT transfers.
* **Platform Admin Sign In:** `platformadmin@example.com` | `AdminPass@2026`
  * Demonstrates platform-wide telemetry, user monitoring across 38 accounts, and security audit log review.

---

## 7. Delivery Package Verification

1. **Active Presentation Archive:**  
   `C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_FINAL.zip` (0.60 MB, 226 files)
2. **Preserved Backup Archive:**  
   `C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_FINAL_BACKUP_20261125_191658.zip`
3. **Audit Evidence Directory:**  
   `C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\AUDIT_EVIDENCE\`
