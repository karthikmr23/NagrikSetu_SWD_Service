# NAGRIKSETU — SWD ELIGIBILITY ENGINE SPECIFICATION (FR-SWD-007 to FR-SWD-013)

### 1. Engine Design & Philosophy
The Social Welfare Department preliminary eligibility engine is a deterministic, rule-based assessment component designed to provide transparent, explainable guidance to citizens before application submission.

### 2. Supported Criteria & Evaluation Logic
* **Field Scope:** `annual_income`, `caste_category`, `residence_state`, `education_level`, `age`, `disability_percentage`, `sslc_percentage`, `hostel_allotted`, `intercaste_registered`.
* **Operators:** `EQUALS`, `NOT_EQUALS`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`, `IN`, `NOT_IN`.
* **Evaluation Statuses:**
  * `SATISFIED`: Input value meets the configured threshold.
  * `UNMET`: Input value fails the configured threshold.
  * `UNKNOWN`: Attribute is missing or incomplete (FR-SWD-010: unknown attributes are NEVER assumed satisfied).

### 3. Statutory Human Decision Disclaimer
> *"You appear to meet the preliminary criteria based on the information available. Final eligibility is determined by the authorized department."*
(In accordance with BR-15 and FR-SWD-012, no automated approval or rejection is ever executed without human administrative review.)
