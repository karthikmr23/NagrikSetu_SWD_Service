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
def setup_auth_test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Clean up any non-baseline test users before each test
    db.query(User).filter(User.email != "citizen@example.com").delete()
    db.commit()

    # Ensure baseline user exists for login testing
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

def test_registration_valid_citizen():
    # 1. New citizen registration with valid details
    payload = {
        "full_name": "Pooja Hegde",
        "email": "pooja.hegde@example.com",
        "phone": "9876543210",
        "password": "SecurePassword@123",
        "confirm_password": "SecurePassword@123",
        "date_of_birth": "1998-05-15",
        "gender": "Female",
        "district": "Udupi",
        "taluk": "Kundapura",
        "pin_code": "576201",
        "caste_category": "OBC",
        "annual_income": 250000.0
    }
    resp = client.post("/api/swd/auth/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["full_name"] == "Pooja Hegde"
    assert data["email"] == "pooja.hegde@example.com"
    assert data["role"] == "CITIZEN"
    assert data["phone"] == "9876543210"
    assert data["district"] == "Udupi"
    assert data["caste_category"] == "OBC"
    assert "password_hash" not in data

def test_registration_missing_required_fields():
    # 2. Registration with missing required fields
    resp = client.post("/api/swd/auth/register", json={
        "email": "missing.fields@example.com"
    })
    assert resp.status_code == 422

def test_registration_invalid_email():
    # 3. Registration with invalid email
    resp = client.post("/api/swd/auth/register", json={
        "full_name": "Invalid Email",
        "email": "not-an-email",
        "phone": "9876543210",
        "password": "Password123"
    })
    assert resp.status_code == 422

def test_registration_invalid_mobile():
    # 4. Registration with invalid mobile number
    resp = client.post("/api/swd/auth/register", json={
        "full_name": "Invalid Mobile",
        "email": "valid.mobile@example.com",
        "phone": "123",  # invalid phone
        "password": "Password123"
    })
    assert resp.status_code == 422

def test_registration_mismatched_passwords():
    # 5. Registration with mismatched passwords
    resp = client.post("/api/swd/auth/register", json={
        "full_name": "Mismatched Password",
        "email": "mismatch@example.com",
        "phone": "9876543211",
        "password": "Password123",
        "confirm_password": "PasswordDifferent"
    })
    assert resp.status_code == 400
    assert "Password and Confirm Password do not match" in resp.json()["detail"]

def test_registration_weak_password():
    # 6. Registration with weak password (< 6 chars)
    resp = client.post("/api/swd/auth/register", json={
        "full_name": "Weak Pass",
        "email": "weak@example.com",
        "phone": "9876543212",
        "password": "123"
    })
    assert resp.status_code == 422

def test_registration_duplicate_email():
    # 7. Duplicate email registration
    resp = client.post("/api/swd/auth/register", json={
        "full_name": "Duplicate Ramesh",
        "email": "citizen@example.com",
        "phone": "9876543219",
        "password": "Password123"
    })
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"]

def test_successful_login_and_failed_logins():
    # 8. Successful login with correct credentials
    login_resp = client.post("/api/swd/auth/login", json={
        "email": "citizen@example.com",
        "password": "CitizenPass@2026"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token is not None
    assert login_resp.json()["role"] == "CITIZEN"

    # 9. Failed login with incorrect password
    bad_pass = client.post("/api/swd/auth/login", json={
        "email": "citizen@example.com",
        "password": "WrongPassword@999"
    })
    assert bad_pass.status_code == 401

    # 10. Login with unregistered email
    unreg = client.post("/api/swd/auth/login", json={
        "email": "unknown_user_99999@example.com",
        "password": "SomePassword@123"
    })
    assert unreg.status_code == 401
