import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)

def test_legacy_administrator_cannot_access_platform_admin():
    """Verify legacy ADMINISTRATOR role does NOT receive Platform Admin permissions."""
    admin_token = create_access_token({
        "sub": "LEGACY-ADM",
        "role": "ADMINISTRATOR",
        "email": "legacy.admin@example.com"
    })
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Platform Admin user management must be forbidden (403)
    res = client.get("/api/swd/admin/users", headers=headers)
    assert res.status_code == 403, f"Expected 403 for legacy ADMINISTRATOR accessing users, got {res.status_code}"
    
    # Platform Admin audit logs must be forbidden (403)
    res = client.get("/api/swd/admin/audit-logs", headers=headers)
    assert res.status_code == 403, f"Expected 403 for legacy ADMINISTRATOR accessing audit-logs, got {res.status_code}"

def test_platform_admin_can_access_government_welfare_admin():
    """Verify Platform Admin has intentional, explicit permission to access Government Welfare Admin features."""
    platform_token = create_access_token({
        "sub": "SUPER-ADM",
        "role": "PLATFORM_ADMIN",
        "email": "platform.admin@example.com"
    })
    headers = {"Authorization": f"Bearer {platform_token}"}
    
    # Category stats in Welfare Admin
    res = client.get("/api/swd/admin/categories/stats", headers=headers)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    # Applications list in Welfare Admin
    res = client.get("/api/swd/admin/applications", headers=headers)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"

def test_server_side_logout_revocation():
    """Verify server-side logout invalidation: token issued before logout is rejected after logout."""
    # 1. Login or create token
    token = create_access_token({
        "sub": "CIT-REVOKE-01",
        "citizen_id": "CIT-REVOKE-01",
        "role": "CITIZEN",
        "email": "revoke.citizen@example.com"
    })
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Before logout, protected endpoint succeeds
    res_before = client.get("/api/swd/auth/me", headers=headers)
    assert res_before.status_code == 200, f"Expected 200 before logout, got {res_before.status_code}"
    
    # 3. Call server logout endpoint
    res_logout = client.post("/api/swd/auth/logout", headers=headers)
    assert res_logout.status_code == 200, f"Expected 200 on logout, got {res_logout.status_code}"
    assert res_logout.json()["status"] == "SUCCESS"
    
    # 4. Attempt to reuse the exact same token after logout -> MUST return 401 Unauthorized
    res_after = client.get("/api/swd/auth/me", headers=headers)
    assert res_after.status_code == 401, f"Expected 401 after logout revocation, got {res_after.status_code}"
    assert "revoked on server" in res_after.json()["detail"].lower()

def test_idor_protection_for_citizen_applications():
    """Verify citizen ownership checks prevent accessing another citizen's records."""
    token = create_access_token({
        "sub": "CIT-USER-A",
        "citizen_id": "CIT-USER-A",
        "role": "CITIZEN",
        "email": "user.a@example.com"
    })
    headers = {"Authorization": f"Bearer {token}"}
    
    # Citizen A attempts to access Citizen B's dossier
    res = client.get("/api/swd/applications/CIT-USER-B", headers=headers)
    assert res.status_code == 403, f"Expected 403 Forbidden for IDOR attempt, got {res.status_code}"
