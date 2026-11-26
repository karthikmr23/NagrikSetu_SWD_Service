# NAGRIKSETU — SWD APPLICATION WORKFLOW SPECIFICATION (FR-SWD-014 to FR-SWD-021)

### 1. Application Lifecycle States
1. **`SUBMITTED`**: Application registered by citizen with bank details and profile particulars.
2. **`UNDER_REVIEW`**: Assigned to welfare department officer for scrutiny and verification.
3. **`MORE_INFORMATION_REQUIRED`**: Administrative officer requests supplementary certificates or clarification.
4. **`APPROVED`**: Official sanction order issued; creates beneficiary record and Aadhaar DBT bridge.
5. **`REJECTED`**: Official rejection recorded with mandatory administrative justification.

### 2. Safeguards & Protections
* **Duplicate Detection (FR-SWD-020):** Flags suspected duplicate applications (`is_duplicate_suspect`) for human review without automatic rejection.
* **Beneficiary Generation (FR-SWD-019):** Strictly tied to authorized administrative approval.
