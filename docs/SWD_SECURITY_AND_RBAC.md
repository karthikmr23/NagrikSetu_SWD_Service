# NAGRIKSETU — SWD SECURITY & ROLE-BASED ACCESS CONTROL (RBAC)

### 1. Token Claims & Verification
* Standard JWT header: `Authorization: Bearer <token>`
* Expected Claims:
  * `sub`: Unique citizen or administrative subject ID
  * `role`: `CITIZEN` | `SWD_ADMIN` | `PLATFORM_ADMIN`
  * `citizen_id`: Required for ownership checks on `/api/swd/applications/{citizen_id}`

### 2. Authorization Boundaries
* **CITIZEN:** May browse published schemes, execute preliminary assessments, submit personal applications, upload own documents, and view own application timelines.
* **SWD_ADMIN:** May manage schemes, update criteria rules, inspect the application queue, request supplementary information, record sanction decisions, and manage beneficiaries.
