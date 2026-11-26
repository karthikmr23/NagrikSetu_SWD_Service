import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from app.main import app
from app.database.connection import Base, get_db
from app.models import Scheme, SchemeCategory, EligibilityRule
from app.core.security import create_access_token

# Test database: isolated SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_swd.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed baseline category and scheme
    db = TestingSessionLocal()
    cat = SchemeCategory(
        code="SCHOLARSHIPS",
        name="Education & Scholarships",
        name_kannada=None,
        description="Scholarships category",
        icon="GraduationCap"
    )
    db.add(cat)
    db.commit()

    scheme = Scheme(
        scheme_code="TEST-SSP-01",
        name="SSP Post-Matric Test Scheme",
        category_id=cat.id,
        administering_authority="SWD Karnataka",
        description="Test scheme description",
        benefit_summary="₹25,000 course fee assistance",
        benefit_type="SCHOLARSHIP",
        benefit_amount=25000.0,
        eligibility_summary="Karnataka residents, Income <= 250000",
        application_instructions="Apply online with marks card",
        application_start_date=date.today() - timedelta(days=10),
        application_end_date=date.today() + timedelta(days=30),
        status="PUBLISHED"
    )
    db.add(scheme)
    db.commit()

    # Add eligibility rules
    r1 = EligibilityRule(
        scheme_id=scheme.id,
        field_name="annual_income",
        operator="LESS_THAN_OR_EQUAL",
        expected_value="250000",
        value_type="FLOAT",
        is_mandatory=True,
        description="Income <= 250000"
    )
    r2 = EligibilityRule(
        scheme_id=scheme.id,
        field_name="residence_state",
        operator="EQUALS",
        expected_value="Karnataka",
        value_type="STRING",
        is_mandatory=True,
        description="State == Karnataka"
    )
    db.add_all([r1, r2])
    db.commit()
    db.close()

    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "swd-service"

def test_get_categories():
    res = client.get("/api/swd/categories")
    assert res.status_code == 200
    cats = res.json()
    assert len(cats) >= 1
    assert cats[0]["code"] == "SCHOLARSHIPS"

def test_get_published_schemes():
    res = client.get("/api/swd/schemes")
    assert res.status_code == 200
    schemes = res.json()
    assert len(schemes) >= 1
    assert schemes[0]["scheme_code"] == "TEST-SSP-01"

def test_eligibility_engine_satisfied():
    res = client.post("/api/swd/schemes/1/eligibility-check", json={
        "citizen_attributes": {
            "residence_state": "Karnataka",
            "annual_income": 180000
        }
    })
    assert res.status_code == 200
    data = res.json()
    assert data["preliminary_status"] == "LIKELY_ELIGIBLE"
    assert len(data["satisfied_criteria"]) == 2
    assert len(data["unmet_criteria"]) == 0

def test_eligibility_engine_unmet():
    res = client.post("/api/swd/schemes/1/eligibility-check", json={
        "citizen_attributes": {
            "residence_state": "Karnataka",
            "annual_income": 350000
        }
    })
    assert res.status_code == 200
    data = res.json()
    assert data["preliminary_status"] == "NOT_ELIGIBLE"
    assert len(data["unmet_criteria"]) >= 1

def test_eligibility_engine_missing_data_insufficient():
    res = client.post("/api/swd/schemes/1/eligibility-check", json={
        "citizen_attributes": {
            "residence_state": "Karnataka"
            # annual_income is missing
        }
    })
    assert res.status_code == 200
    data = res.json()
    assert data["preliminary_status"] == "INSUFFICIENT_INFORMATION"
    assert "annual_income" in data["missing_fields"]

def test_submit_application_workflow():
    token = create_access_token({
        "sub": "CIT-TEST-001",
        "citizen_id": "CIT-TEST-001",
        "role": "CITIZEN",
        "email": "test.citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "citizen_id": "CIT-TEST-001",
        "citizen_name": "Test Citizen Student",
        "citizen_email": "test.citizen@example.com",
        "citizen_phone": "9876543210",
        "annual_income": 120000.0,
        "caste_category": "SC",
        "residence_district": "Bengaluru",
        "disability_percentage": 0.0,
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0001234"
    }

    res = client.post("/api/swd/schemes/1/applications", json=payload, headers=headers)
    assert res.status_code == 200
    app_data = res.json()
    assert app_data["status"] == "SUBMITTED"
    assert "SWD-APP-" in app_data["application_number"]

    # Verify citizen tracking
    track_res = client.get("/api/swd/applications/CIT-TEST-001", headers=headers)
    assert track_res.status_code == 200
    assert len(track_res.json()) >= 1

def test_admin_dashboard_and_decision():
    admin_token = create_access_token({
        "sub": "ADM-001",
        "role": "SWD_ADMIN",
        "email": "swd.admin@nagriksetu.local"
    })
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Check dashboard stats
    dash_res = client.get("/api/swd/admin/dashboard", headers=admin_headers)
    assert dash_res.status_code == 200
    stats = dash_res.json()
    assert stats["total_schemes"] >= 1
    assert stats["total_applications"] >= 1

    # Record approval decision
    decision_payload = {
        "decision": "APPROVED",
        "remarks": "Income and caste certificates verified. Approved for course fee reimbursement.",
        "sanctioned_amount": 25000.0
    }
    dec_res = client.post("/api/swd/admin/applications/1/decision", json=decision_payload, headers=admin_headers)
    assert dec_res.status_code == 200
    assert dec_res.json()["status"] == "APPROVED"

    # Verify beneficiary created (FR-SWD-019)
    ben_res = client.get("/api/swd/beneficiaries", headers=admin_headers)
    assert ben_res.status_code == 200
    bens = ben_res.json()
    assert len(bens) >= 1
    assert bens[0]["citizen_id"] == "CIT-TEST-001"

def test_scheme_creation_and_update():
    admin_token = create_access_token({
        "sub": "ADM-001",
        "role": "SWD_ADMIN",
        "email": "swd.admin@nagriksetu.local"
    })
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Create a scheme
    payload = {
        "scheme_code": "TEST-NEW-02",
        "name": "Vidyasiri Hostel Alternate Scheme",
        "category_id": 1,
        "department": "Backward Classes Welfare Department",
        "administering_authority": "Govt of Karnataka",
        "description": "Financial stipend for boarding",
        "benefit_summary": "Rs 1500 per month stipend",
        "benefit_type": "FINANCIAL_ASSISTANCE",
        "benefit_amount": 15000.0,
        "eligibility_summary": "Income <= 250000, Cat-1 or OBC",
        "application_instructions": "Submit distance certificate",
        "application_start_date": "2026-06-01",
        "application_end_date": "2026-12-31",
        "status": "DRAFT"
    }
    create_res = client.post("/api/swd/schemes", json=payload, headers=headers)
    assert create_res.status_code == 200
    created = create_res.json()
    assert created["scheme_code"] == "TEST-NEW-02"
    scheme_id = created["id"]

    # 2. Update scheme status to PUBLISHED
    update_res = client.put(f"/api/swd/schemes/{scheme_id}", json={"status": "PUBLISHED"}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "PUBLISHED"

    # 3. Deactivate scheme
    del_res = client.delete(f"/api/swd/schemes/{scheme_id}", headers=headers)
    assert del_res.status_code == 200
    assert "deactivated" in del_res.json()["message"]

def test_duplicate_application_detection():
    token = create_access_token({
        "sub": "CIT-TEST-DUP",
        "citizen_id": "CIT-TEST-DUP",
        "role": "CITIZEN",
        "email": "dup.citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "citizen_id": "CIT-TEST-DUP",
        "citizen_name": "Duplicate Check Applicant",
        "citizen_phone": "9887766554",
        "annual_income": 100000.0,
        "caste_category": "SC",
        "residence_district": "Mysuru",
        "bank_account_number": "1122334455",
        "bank_ifsc": "SBIN0009988"
    }

    # First submission
    res1 = client.post("/api/swd/schemes/1/applications", json=payload, headers=headers)
    assert res1.status_code == 200
    assert res1.json()["is_duplicate_suspect"] is False

    # Second submission (should succeed but be flagged as suspect for human review - FR-SWD-020)
    res2 = client.post("/api/swd/schemes/1/applications", json=payload, headers=headers)
    assert res2.status_code == 200
    assert res2.json()["is_duplicate_suspect"] is True
    assert "Previous application" in res2.json()["duplicate_reason"]

def test_recommendation_match_endpoint():
    req_body = {
        "citizen_attributes": {
            "residence_state": "Karnataka",
            "annual_income": 150000,
            "caste_category": "SC",
            "education_level": "Undergraduate"
        }
    }
    res = client.post("/api/swd/recommendations/match", json=req_body)
    assert res.status_code == 200
    matches = res.json()
    assert len(matches) >= 1
    assert matches[0]["match_category"] in ["LIKELY_MATCH", "POSSIBLE_MATCH"]
    assert matches[0]["score"] > 0
    assert "preliminary" in matches[0]["disclaimer"].lower()

def test_unauthorized_and_ownership_restrictions():
    # Citizen A cannot access Citizen B's applications
    token_a = create_access_token({"sub": "CIT-A", "citizen_id": "CIT-A", "role": "CITIZEN"})
    headers_a = {"Authorization": f"Bearer {token_a}"}

    res = client.get("/api/swd/applications/CIT-B", headers=headers_a)
    assert res.status_code == 403

    # Citizen cannot access admin endpoints
    admin_dash_res = client.get("/api/swd/admin/dashboard", headers=headers_a)
    assert admin_dash_res.status_code == 403

def test_draft_rule_testing_and_invalid_rule_rejection():
    admin_token = create_access_token({"sub": "ADM-001", "role": "SWD_ADMIN"})
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. FR-SWD-008: Reject invalid rule operators
    invalid_rule_payload = {
        "field_name": "annual_income",
        "operator": "INVALID_OP",
        "expected_value": "200000",
        "value_type": "FLOAT",
        "description": "Invalid rule"
    }
    res_invalid = client.post("/api/swd/schemes/1/rules", json=invalid_rule_payload, headers=admin_headers)
    assert res_invalid.status_code == 422  # Pydantic validation rejection

    # 2. FR-SWD-007: Add valid rule
    valid_rule_payload = {
        "field_name": "age",
        "operator": "GREATER_THAN_OR_EQUAL",
        "expected_value": "18",
        "value_type": "INTEGER",
        "is_mandatory": True,
        "description": "Age 18 and above"
    }
    res_valid = client.post("/api/swd/schemes/1/rules", json=valid_rule_payload, headers=admin_headers)
    assert res_valid.status_code == 200
    assert res_valid.json()["field_name"] == "age"

    # 3. FR-SWD-013: Test draft rules without modifying published rules
    draft_test_payload = {
        "draft_rules": [
            {
                "field_name": "annual_income",
                "operator": "LESS_THAN_OR_EQUAL",
                "expected_value": "150000",
                "value_type": "FLOAT",
                "is_mandatory": True,
                "description": "Income <= 150000"
            },
            {
                "field_name": "caste_category",
                "operator": "EQUALS",
                "expected_value": "SC",
                "value_type": "STRING",
                "is_mandatory": True,
                "description": "Must be SC"
            }
        ],
        "synthetic_profiles": [
            {"annual_income": 120000, "caste_category": "SC"},
            {"annual_income": 200000, "caste_category": "SC"},
            {"annual_income": 100000}  # missing caste
        ]
    }
    res_draft = client.post("/api/swd/admin/rules/test-draft", json=draft_test_payload, headers=admin_headers)
    assert res_draft.status_code == 200
    draft_data = res_draft.json()
    assert draft_data["total_profiles_tested"] == 3
    assert draft_data["results"][0]["preliminary_status"] == "LIKELY_ELIGIBLE"
    assert draft_data["results"][1]["preliminary_status"] == "NOT_ELIGIBLE"
    assert draft_data["results"][2]["preliminary_status"] == "INSUFFICIENT_INFORMATION"

def test_outbox_event_creation_and_processing():
    from app.events.rabbitmq_publisher import process_pending_outbox_events
    from app.models import OutboxEvent

    db = TestingSessionLocal()
    # Check outbox events exist from earlier submissions
    events = db.query(OutboxEvent).all()
    assert len(events) >= 1
    first_evt = events[0]
    assert first_evt.event_id.startswith("evt_swd_")
    assert first_evt.schema_version == "1.0"
    assert first_evt.event_type in ["SCHEME_APPLICATION_CREATED", "SCHEME_APPLICATION_UPDATED"]
    assert "citizen_id" in first_evt.payload or "application_id" in first_evt.payload

    # Process outbox events
    processed = process_pending_outbox_events(db)
    assert processed >= 0
    db.close()
