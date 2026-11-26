import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from app.main import app
from app.database.connection import Base, get_db
from app.models import Scheme, SchemeCategory, EligibilityRule, Office, SchemeApplication
from app.core.security import create_access_token

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
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_features_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Seed office if none exists
    if db.query(Office).count() == 0:
        o = Office(
            name="District Social Welfare Office, Bengaluru Urban",
            office_type="District Welfare Office",
            district="Bengaluru Urban",
            taluk="Bengaluru North",
            address="Podium Block, V.V. Towers, Bengaluru - 560001",
            contact_number="080-22864223",
            email="dswobangaloreurban@gmail.com",
            working_hours="10:00 AM - 5:30 PM",
            services_offered="Scholarships, hostels, DBT",
            latitude=12.9791,
            longitude=77.5912,
            map_link="https://maps.google.com/?q=12.9791,77.5912",
            is_active=True,
            verification_status="VERIFIED"
        )
        db.add(o)

    # Seed application if none exists
    if db.query(SchemeApplication).count() == 0:
        # Check scheme
        scheme = db.query(Scheme).first()
        if not scheme:
            cat = SchemeCategory(code="TESTCAT", name="Test Cat", icon="Icon")
            db.add(cat)
            db.commit()
            scheme = Scheme(
                scheme_code="TEST-SCH-01",
                name="Test Scheme for Receipt",
                category_id=cat.id,
                administering_authority="SWD",
                description="Desc",
                benefit_summary="Rs 5000",
                eligibility_summary="Elig",
                application_instructions="Apply",
                application_start_date=date.today() - timedelta(days=5),
                application_end_date=date.today() + timedelta(days=30),
                status="PUBLISHED"
            )
            db.add(scheme)
            db.commit()

        app_rec = SchemeApplication(
            application_number="SWD-APP-2026-TEST01",
            scheme_id=scheme.id,
            citizen_id="CIT-KA-TEST-001",
            citizen_name="Test Citizen",
            citizen_phone="9876543210",
            annual_income=150000.0,
            caste_category="SC",
            residence_district="Bengaluru Urban",
            bank_account_number="SBIN0040123991",
            bank_ifsc="SBIN0040123",
            status="SUBMITTED"
        )
        db.add(app_rec)

    db.commit()
    db.close()

def test_office_locator_list():
    response = client.get("/api/swd/offices")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first = data[0]
    assert "name" in first
    assert "district" in first
    assert "taluk" in first
    assert "contact_number" in first

def test_office_locator_filter_by_district():
    response = client.get("/api/swd/offices?district=Bengaluru Urban")
    assert response.status_code == 200
    data = response.json()
    assert all("Bengaluru Urban" in o["district"] for o in data)

def test_pdf_receipt_generation():
    # Use existing application
    db = TestingSessionLocal()
    app_rec = db.query(SchemeApplication).first()
    app_id = app_rec.id if app_rec else 1
    db.close()

    response = client.get(f"/api/swd/applications/{app_id}/receipt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000
    assert response.content[:4] == b"%PDF"

def test_grievances_flow():
    # Submit grievance
    payload = {
        "citizen_id": "CIT-KA-TEST-001",
        "citizen_name": "Test Citizen",
        "category": "DELAY_IN_SANCTION",
        "subject": "Delayed verification for post-matric stipend",
        "description": "My application was submitted 2 weeks ago and is still in review."
    }
    create_resp = client.post("/api/swd/grievances", json=payload)
    assert create_resp.status_code == 200
    grv = create_resp.json()
    assert grv["grievance_number"].startswith("GRV-SWD-")
    assert grv["status"] == "SUBMITTED"

    # List grievances
    list_resp = client.get(f"/api/swd/grievances?citizen_id=CIT-KA-TEST-001")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

def test_notifications_flow():
    # Check notifications for user
    resp = client.get("/api/swd/notifications/CIT-KA-TEST-001")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    notif = data[0]
    assert notif["user_id"] == "CIT-KA-TEST-001"

    # Mark one read
    read_resp = client.patch(f"/api/swd/notifications/{notif['id']}/read")
    assert read_resp.status_code == 200
    assert read_resp.json()["is_read"] is True

    # Mark all read
    all_read_resp = client.post("/api/swd/notifications/CIT-KA-TEST-001/mark-all-read")
    assert all_read_resp.status_code == 200
    assert all_read_resp.json()["status"] == "success"
