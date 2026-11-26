# NAGRIKSETU — SWD ELIGIBILITY ENGINE & APPLICATION WORKFLOW

### 1. Preliminary Eligibility Rules Engine (FR-SWD-007 to FR-SWD-013)

The Social Welfare Department preliminary assessment engine is deterministic and rule-based:

1. **Configurable Criteria Stored in MySQL:**
   * Supported fields: `annual_income`, `caste_category`, `residence_state`, `education_level`, `age`, `disability_percentage`, `sslc_percentage`, `hostel_allotted`, `intercaste_registered`.
   * Supported operators: `EQUALS`, `NOT_EQUALS`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`, `IN`, `NOT_IN`.
   * Value types: `STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`, `LIST`.
2. **Evaluation States:**
   * **`SATISFIED`**: Attribute meets or exceeds rule criteria.
   * **`UNMET`**: Attribute explicitly violates rule condition.
   * **`UNKNOWN`**: Attribute is missing from citizen input. (FR-SWD-010: Missing fields are NEVER assumed satisfied).
3. **Overall Preliminary Status:**
   * `LIKELY_ELIGIBLE`: All mandatory rules are satisfied.
   * `NOT_ELIGIBLE`: One or more mandatory rules are unmet.
   * `INSUFFICIENT_INFORMATION`: One or more mandatory rules are unknown.
4. **Mandatory Human Decision Boundary (FR-SWD-012 & BR-15):**
   * Displays required disclaimer: *"You appear to meet the preliminary criteria based on the information available. Final eligibility is determined by the authorized department."*
   * System never performs official approvals automatically; human administrator retains final authority.

---

### 2. Application Lifecycle State Machine (FR-SWD-014 to FR-SWD-021)

```
       [ Citizen Submits Application ]
                     |
                     v
             +---------------+
             |   SUBMITTED   |
             +---------------+
                     |
                     v
             +---------------+
             | UNDER_REVIEW  | <-------------------+
             +---------------+                     |
               |           |                       |
               |           v                       |
               |   +---------------------------+   |
               |   | MORE_INFORMATION_REQUIRED | --+ (Citizen uploads document)
               |   +---------------------------+
               |
         +-----+-----+
         |           |
         v           v
   +----------+ +----------+
   | APPROVED | | REJECTED |
   +----------+ +----------+
         |
         v
[ Creates Beneficiary Record & DBT Mandate ]
```

1. **Duplicate Detection (FR-SWD-020):**
   * Previous applications from the same citizen on the same scheme are flagged with `is_duplicate_suspect = True` and displayed to reviewers.
   * Potential duplicates are **never automatically rejected**; human discretion applies.
2. **Beneficiary Generation (FR-SWD-019):**
   * Beneficiary record (`BEN-YYYY-SWD-XXXXXX`) is created **strictly upon authorized approval**.
   * Records sanctioned DBT amount and disbursement channel (Aadhaar Bridge).
