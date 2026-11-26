import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)

def test_citizen_cannot_access_government_welfare_admin_api():
    """Verify citizens are rejected with 403 when trying to access Welfare Officer endpoints."""
    citizen_token = create_access_token({
        "sub": "CIT-KA-9901",
        "citizen_id": "CIT-KA-9901",
        "role": "CITIZEN",
        "email": "citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {citizen_token}"}
    
    # 1. Admin dashboard
    res = client.get("/api/swd/admin/dashboard", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # 2. Category application statistics
    res = client.get("/api/swd/admin/categories/stats", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # 3. Application review list
    res = client.get("/api/swd/admin/applications", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"

def test_citizen_cannot_access_platform_admin_api():
    """Verify citizens are rejected with 403 when trying to access Platform Admin endpoints."""
    citizen_token = create_access_token({
        "sub": "CIT-KA-9901",
        "citizen_id": "CIT-KA-9901",
        "role": "CITIZEN",
        "email": "citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {citizen_token}"}
    
    # User management
    res = client.get("/api/swd/admin/users", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # Audit logs
    res = client.get("/api/swd/admin/audit-logs", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # Role modification
    res = client.put("/api/swd/admin/users/1/role?role=PLATFORM_ADMIN", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"

def test_welfare_officer_cannot_access_platform_admin_api():
    """Verify Government Welfare Admin cannot access Platform Admin user/role management."""
    officer_token = create_access_token({
        "sub": "OFF-001",
        "role": "WELFARE_OFFICER",
        "email": "officer@nagriksetu.local"
    })
    headers = {"Authorization": f"Bearer {officer_token}"}
    
    # User management
    res = client.get("/api/swd/admin/users", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # Role elevation attempt
    res = client.put("/api/swd/admin/users/2/role?role=PLATFORM_ADMIN", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"
    
    # Audit logs
    res = client.get("/api/swd/admin/audit-logs", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"

def test_citizen_cannot_view_or_manipulate_other_citizens_applications():
    """Verify strict citizen data isolation (IDOR protection)."""
    citizen_token = create_access_token({
        "sub": "CIT-KA-9901",
        "citizen_id": "CIT-KA-9901",
        "role": "CITIZEN",
        "email": "citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {citizen_token}"}
    
    # Attempting to fetch another citizen's application dossier
    res = client.get("/api/swd/applications/CIT-OTHER-9999", headers=headers)
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"

def test_unauthenticated_request_rejected():
    """Verify unauthenticated requests to protected endpoints return 401."""
    res = client.get("/api/swd/admin/dashboard")
    assert res.status_code in [401, 403], f"Expected 401/403, got {res.status_code}"
    
    res = client.get("/api/swd/admin/users")
    assert res.status_code in [401, 403], f"Expected 401/403, got {res.status_code}"
