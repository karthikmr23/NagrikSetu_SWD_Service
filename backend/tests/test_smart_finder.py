import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import get_db, Base
from app.models import SchemeCategory, Scheme, EligibilityRule
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup SQLite test database fixture
TEST_DATABASE_URL = "sqlite:///./test_finder.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_finder_test_data():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    # 1. Categories
    cat_edu = SchemeCategory(code="SCHOLARSHIPS", name="Education & Scholarships")
    cat_agr = SchemeCategory(code="AGRICULTURE", name="Agriculture & Rural Livelihoods")
    cat_wcm = SchemeCategory(code="WOMEN_CHILDREN", name="Women & Children Welfare")
    db.add_all([cat_edu, cat_agr, cat_wcm])
    db.commit()

    # 2. Education Scheme (SSP Post-Matric)
    scheme_edu = Scheme(
        scheme_code="KAR-SSP-POSTMATRIC",
        name="Post-Matric Scholarship for SC/ST and Backward Classes Students",
        category_id=cat_edu.id,
        administering_authority="Social Welfare Department, Government of Karnataka",
        description="State post-matric scholarship for higher education students.",
        benefit_summary="Tuition fee maintenance allowance.",
        benefit_amount=25000.0,
        eligibility_summary="Karnataka residents, SC/ST/OBC students, income <= 250,000",
        application_instructions="Apply online with student enrollment details.",
        application_start_date=date.today() - timedelta(days=10),
        application_end_date=date.today() + timedelta(days=60),
        status="PUBLISHED"
    )
    db.add(scheme_edu)
    db.commit()

    db.add_all([
        EligibilityRule(scheme_id=scheme_edu.id, field_name="residence_state", operator="EQUALS", expected_value="Karnataka", value_type="STRING", is_mandatory=True, description="Karnataka resident"),
        EligibilityRule(scheme_id=scheme_edu.id, field_name="annual_income", operator="LESS_THAN_OR_EQUAL", expected_value="250000", value_type="FLOAT", is_mandatory=True, description="Income under 2.5 Lakh"),
        EligibilityRule(scheme_id=scheme_edu.id, field_name="is_student", operator="EQUALS", expected_value="true", value_type="BOOLEAN", is_mandatory=True, description="Enrolled student"),
        EligibilityRule(scheme_id=scheme_edu.id, field_name="caste_category", operator="IN", expected_value="SC,ST,OBC,Cat-1,2A,2B,3A,3B", value_type="LIST", is_mandatory=True, description="Belong to reserved/backward category")
    ])

    # 3. Farmer Scheme (Krishi Bhagya)
    scheme_agr = Scheme(
        scheme_code="KAR-AGR-KRISHI-BHAGYA",
        name="Krishi Bhagya Scheme",
        category_id=cat_agr.id,
        administering_authority="Department of Agriculture, Government of Karnataka",
        description="Dryland agricultural support and farm pond construction.",
        benefit_summary="Up to 80% subsidy for micro-irrigation and water storage.",
        benefit_amount=50000.0,
        eligibility_summary="Practicing farmers in Karnataka.",
        application_instructions="Submit land RTC and FRUITS ID.",
        application_start_date=date.today() - timedelta(days=10),
        application_end_date=date.today() + timedelta(days=60),
        status="PUBLISHED"
    )
    db.add(scheme_agr)
    db.commit()

    db.add_all([
        EligibilityRule(scheme_id=scheme_agr.id, field_name="residence_state", operator="EQUALS", expected_value="Karnataka", value_type="STRING", is_mandatory=True, description="Karnataka resident"),
        EligibilityRule(scheme_id=scheme_agr.id, field_name="is_farmer", operator="EQUALS", expected_value="true", value_type="BOOLEAN", is_mandatory=True, description="Practicing farmer in Karnataka")
    ])

    # 4. Women Scheme (Shakti Free Bus Travel)
    scheme_wcm = Scheme(
        scheme_code="KAR-FLAG-SHAKTI",
        name="Shakti Free Bus Travel Scheme",
        category_id=cat_wcm.id,
        administering_authority="Transport Department & SWD, Karnataka",
        description="Free bus travel for all women across Karnataka State Road Transport.",
        benefit_summary="100% fare waiver in non-premium transit buses.",
        benefit_amount=0.0,
        eligibility_summary="All women domiciled in Karnataka.",
        application_instructions="Apply online or show valid domicile ID.",
        application_start_date=date.today() - timedelta(days=10),
        application_end_date=date.today() + timedelta(days=60),
        status="PUBLISHED"
    )
    db.add(scheme_wcm)
    db.commit()

    db.add_all([
        EligibilityRule(scheme_id=scheme_wcm.id, field_name="residence_state", operator="EQUALS", expected_value="Karnataka", value_type="STRING", is_mandatory=True, description="Karnataka resident"),
        EligibilityRule(scheme_id=scheme_wcm.id, field_name="is_woman", operator="EQUALS", expected_value="true", value_type="BOOLEAN", is_mandatory=True, description="Woman beneficiary")
    ])

    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.pop(get_db, None)

def test_finder_options():
    res = client.get("/api/swd/finder/options")
    assert res.status_code == 200
    data = res.json()
    assert "districts" in data
    assert "Bengaluru Urban" in data["districts"]
    assert "social_categories" in data
    assert "SC" in data["social_categories"]
    assert "occupations" in data
    assert "Student" in data["occupations"]
    assert "Farmer" in data["occupations"]

def test_finder_student_matching():
    payload = {
        "age": 20,
        "district": "Bengaluru Urban",
        "gender": "male",
        "caste_category": "SC",
        "annual_income": 120000,
        "occupation": "Student",
        "is_student": True,
        "is_farmer": False
    }
    res = client.post("/api/swd/finder/match", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] > 0
    matched_codes = [r["scheme_code"] for r in data["results"] if r["match_status"] == "Potential Match"]
    assert "KAR-SSP-POSTMATRIC" in matched_codes
    first_match = next(r for r in data["results"] if r["scheme_code"] == "KAR-SSP-POSTMATRIC")
    assert len(first_match["why_matched"]) > 0

def test_finder_farmer_matching():
    payload = {
        "age": 42,
        "district": "Mandya",
        "gender": "male",
        "caste_category": "OBC",
        "annual_income": 95000,
        "occupation": "Farmer",
        "is_farmer": True,
        "is_student": False
    }
    res = client.post("/api/swd/finder/match", json=payload)
    assert res.status_code == 200
    data = res.json()
    matched_codes = [r["scheme_code"] for r in data["results"] if r["match_status"] == "Potential Match"]
    assert "KAR-AGR-KRISHI-BHAGYA" in matched_codes

def test_finder_women_matching():
    payload = {
        "age": 32,
        "district": "Mysuru",
        "gender": "female",
        "is_woman": True,
        "caste_category": "General",
        "annual_income": 80000
    }
    res = client.post("/api/swd/finder/match", json=payload)
    assert res.status_code == 200
    data = res.json()
    matched_codes = [r["scheme_code"] for r in data["results"] if r["match_status"] == "Potential Match"]
    assert "KAR-FLAG-SHAKTI" in matched_codes

def test_finder_missing_info_check_requirements():
    payload = {
        "district": "Bengaluru Urban"
    }
    res = client.post("/api/swd/finder/match", json=payload)
    assert res.status_code == 200
    data = res.json()
    check_reqs = [r for r in data["results"] if r["match_status"] == "Check Requirements"]
    assert len(check_reqs) > 0

def test_finder_disclaimer_and_no_guarantees():
    res = client.post("/api/swd/finder/match", json={"age": 25})
    assert res.status_code == 200
    data = res.json()
    assert "disclaimer" in data
    assert "Final eligibility" in data["disclaimer"]
    for r in data["results"]:
        assert "Government Approved" not in r["match_status"]
        assert "Guaranteed" not in r["match_status"]
