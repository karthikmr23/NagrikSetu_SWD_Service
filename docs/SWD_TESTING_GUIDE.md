# NAGRIKSETU — SWD TESTING GUIDE & VERIFICATION SUITE

### 1. Test Harness Overview
Automated backend unit and integration tests are executed using Pytest and FastAPI TestClient.

### 2. Execution Command
```bash
cd backend
python -m pytest tests/test_swd_service.py -v
```

### 3. Test Coverage Matrix
* `test_health_endpoint`: Asserts 200 OK and service status `healthy`.
* `test_get_categories`: Verifies retrieval of welfare scheme categories.
* `test_get_published_schemes`: Verifies published scheme filtering.
* `test_eligibility_engine_satisfied`: Verifies positive match logic.
* `test_eligibility_engine_unmet`: Verifies rule failure detection.
* `test_eligibility_engine_missing_data_insufficient`: Verifies that missing data generates `INSUFFICIENT_INFORMATION`.
* `test_submit_application_workflow`: Verifies application dossier persistence and citizen ownership.
* `test_admin_dashboard_and_decision`: Verifies administrative approval and beneficiary generation.
