import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.connection import Base, get_db
from app.models import User
from app.core.security import get_password_hash

# Test database: isolated SQLite
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

@pytest.fixture(autouse=True)
def setup_profile_test_user():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Ensure test user exists in the SQLite test db
    existing = db.query(User).filter(User.email == "citizen@example.com").first()
    if not existing:
        user = User(
            citizen_id="CIT-KA-9901",
            email="citizen@example.com",
            password_hash=get_password_hash("CitizenPass@2026"),
            full_name="Ramesh Kumar Nayak",
            role="CITIZEN",
            phone="9845098450",
            district="Bengaluru Urban",
            state="Karnataka",
            annual_income=180000.0,
            caste_category="SC",
            disability_percentage=0.0,
            bank_account_number="SBIN0040998877",
            bank_ifsc="SBIN0040998",
            is_active=True
        )
        db.add(user)
        db.commit()
    db.close()

def test_profile_retrieval_and_update_workflow():
    # 1. Login as standard citizen
    login_resp = client.post("/api/swd/auth/login", json={
        "email": "citizen@example.com",
        "password": "CitizenPass@2026"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get profile via /api/swd/auth/me
    me_resp = client.get("/api/swd/auth/me", headers=headers)
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert data["citizen_id"] == "CIT-KA-9901"
    assert "email" in data
    assert "role" in data
    assert data["role"] == "CITIZEN"

    # 3. Update permitted profile fields
    update_payload = {
        "full_name": "Ramesh Kumar Nayak (Verified Citizen)",
        "phone": "9845012345",
        "district": "Mysuru",
        "state": "Karnataka",
        "annual_income": 195000.0,
        "caste_category": "SC",
        "disability_percentage": 0.0,
        "bank_account_number": "SBIN0040998811",
        "bank_ifsc": "SBIN0040998"
    }
    put_resp = client.put("/api/swd/auth/profile", json=update_payload, headers=headers)
    assert put_resp.status_code == 200
    updated = put_resp.json()
    assert updated["full_name"] == "Ramesh Kumar Nayak (Verified Citizen)"
    assert updated["phone"] == "9845012345"
    assert updated["district"] == "Mysuru"
    assert updated["annual_income"] == 195000.0
    assert updated["bank_account_number"] == "SBIN0040998811"

    # 4. Re-fetch via /api/swd/auth/me to confirm persistence
    me_after = client.get("/api/swd/auth/me", headers=headers)
    assert me_after.status_code == 200
    assert me_after.json()["full_name"] == "Ramesh Kumar Nayak (Verified Citizen)"
    assert me_after.json()["phone"] == "9845012345"
    assert me_after.json()["district"] == "Mysuru"
    assert me_after.json()["bank_account_number"] == "SBIN0040998811"

def test_profile_security_role_escalation_forbidden():
    # Login as citizen
    login_resp = client.post("/api/swd/auth/login", json={
        "email": "citizen@example.com",
        "password": "CitizenPass@2026"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to inject role escalation or alter citizen_id
    malicious_payload = {
        "full_name": "Ramesh Citizen",
        "role": "ADMINISTRATOR",
        "citizen_id": "ADM-HACKED-001"
    }
    put_resp = client.put("/api/swd/auth/profile", json=malicious_payload, headers=headers)
    assert put_resp.status_code == 200
    res = put_resp.json()
    assert res["role"] == "CITIZEN"
    assert res["citizen_id"] == "CIT-KA-9901"

    # Verify via /me that role is still CITIZEN
    me_resp = client.get("/api/swd/auth/me", headers=headers)
    assert me_resp.json()["role"] == "CITIZEN"
    assert me_resp.json()["citizen_id"] == "CIT-KA-9901"

def test_profile_unauthenticated_rejected():
    get_resp = client.get("/api/swd/auth/me")
    assert get_resp.status_code == 401

    put_resp = client.put("/api/swd/auth/profile", json={"full_name": "Hacker"})
    assert put_resp.status_code == 401
