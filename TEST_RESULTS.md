# NagrikSetu SWD — Functional & Eligibility Test Results

**Date of Execution:** 2026-11-25  
**Test Suite:** End-to-End Functional Suite (`run_project_functional_tests.py`) & Multi-Scenario Eligibility Engine Suite (`test_8_schemes_eligibility.py`)  
**Overall Execution Result:** **36 OF 36 TESTS PASSED (100% SUCCESS RATE)**

---

## 1. Core Functional Test Results (12 / 12 PASS)

| Test ID | Test Description | Target / Endpoint | Expected Outcome | Actual Terminal Output | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Backend Health Probe | `GET /health` | HTTP 200, status="healthy" | `HTTP 200, {'service': 'swd-service', 'status': 'healthy'}` | **PASS** |
| **TC-02** | Frontend Web Availability | `http://localhost:5174/` | HTTP 200 OK | `HTTP 200 OK (Nginx Alpine)` | **PASS** |
| **TC-03** | Citizen Authentication | `POST /api/swd/auth/login` (`mukesh2345@gmail.com`) | JWT Token + Citizen ID | `Token issued, citizen_id=CIT-KA-2026-DE2B4F` | **PASS** |
| **TC-04** | Welfare Admin Authentication | `POST /api/swd/auth/login` (`welfareadmin@example.com`) | JWT Token + Welfare Admin Role | `Token issued, role=GOVERNMENT_WELFARE_ADMIN` | **PASS** |
| **TC-05** | Platform Admin Authentication | `POST /api/swd/auth/login` (`platformadmin@example.com`) | JWT Token + Platform Admin Role | `Token issued, role=PLATFORM_ADMIN` | **PASS** |
| **TC-06** | Public Scheme Catalogue | `GET /api/swd/schemes` | 28 schemes, 0 Shakti | `28 published schemes, Shakti included=False` | **PASS** |
| **TC-07** | Application Tracking | `GET /api/swd/applications/CIT-KA-2026-DE2B4F` | App SWD-APP-2026-98E64D found | `App found=True, status=UNDER_REVIEW` | **PASS** |
| **TC-08** | Pure-Python PDF Receipt | `GET /api/swd/applications/36/receipt` | HTTP 200, %PDF-1.4 header | `HTTP 200, size=2148 bytes, %PDF-1.4 header` | **PASS** |
| **TC-09** | Welfare Admin Metrics | `GET /api/swd/admin/dashboard` | Dynamic MySQL counters | `total_applications=44, schemes=28, beneficiaries=28` | **PASS** |
| **TC-10** | Platform Admin Monitoring | `GET /api/swd/admin/users`, `audit-logs` | Active accounts and audit logs | `Users=39, Audit logs=50 (paginated from 142 total)` | **PASS** |
| **TC-11** | Grievance Resolution Workflow | `POST /api/swd/grievances` & `PUT .../resolve` | Transition to RESOLVED | `Ticket created, resolved by officer, status=RESOLVED` | **PASS** |
| **TC-12** | RBAC Security Enforcement | `GET /api/swd/admin/dashboard` with Citizen Token | HTTP 403 Forbidden | `HTTP 403 Forbidden (RBAC Access Denied)` | **PASS** |

---

## 2. Scheme-Specific Eligibility Matrix (8 Schemes x 3 Scenarios = 24 / 24 PASS)

| Scheme ID & Name | Scenario 1: Satisfied | Scenario 2: Failed Mandatory | Scenario 3: Missing Mandatory | Result |
| :--- | :---: | :---: | :---: | :---: |
| **Scheme 10: Udyogini Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `is_woman`, `age`) | **PASS** |
| **Scheme 11: Bhagyalakshmi Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `gender`) | **PASS** |
| **Scheme 12: Matru Poorna Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `is_woman`) | **PASS** |
| **Scheme 13: Thayi Bhagya & Prasoothi Araike** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `is_woman`) | **PASS** |
| **Scheme 14: Madilu Kit Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Home delivery) | `INSUFFICIENT_INFORMATION` (Missing `institutional_delivery`) | **PASS** |
| **Scheme 15: Santhwana Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `is_woman`) | **PASS** |
| **Scheme 16: Dhanashree & Chetana Scheme** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Male) | `INSUFFICIENT_INFORMATION` (Missing `age`) | **PASS** |
| **Scheme 35: Gruha Arogya Yojana** | `LIKELY_ELIGIBLE` | `NOT_ELIGIBLE` (Age 22 < 30) | `INSUFFICIENT_INFORMATION` (Missing `age`) | **PASS** |

---

## 3. Demographic Profile Verification (5 Diverse Profiles)

| Profile Tested | Attributes | Potential Matches | Check Requirements | Not Matched | Verification Finding |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **1. Mahesh** | Male, General, Student, ₹1.8L, Age 28, Unmarried | **0** | **4** | **24** | Zero false positives; girl-child/women schemes rejected. |
| **2. Female Applicant** | Female, OBC, Unemployed, ₹1.2L, Age 25, Unmarried | **10** | **3** | **15** | Gruha Lakshmi, Udyogini, Matru Poorna matched. |
| **3. SC Student** | Male, SC, Student, ₹1.5L, Age 21, Unmarried | **4** | **3** | **21** | Arivu Education Loan, Vidyasiri, Prabuddha matched. |
| **4. Farmer Applicant** | Male, General, Farmer, ₹90K, Age 42, Married | **4** | **4** | **20** | Krishi Bhagya, Raitha Siri, KAPY matched. |
| **5. Senior Citizen** | Male, OBC, Other, ₹25K, Age 68, Married | **4** | **4** | **20** | Sandhya Suraksha Pension, Basava Vasati matched. |

---

## 4. Test Conclusion

Every functional capability, security restriction, and eligibility condition has been tested against live running microservices with zero simulated data. All tests completed successfully.
