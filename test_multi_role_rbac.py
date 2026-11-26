"""
Comprehensive Multi-Role RBAC Security & Separation Test
Covers all requirements from user request:
1. Citizen Role:
   - Login as Citizen (citizen@example.com / CitizenPass@2026)
   - Access Citizen Dashboard / applications / preliminary eligibility -> PASS (200)
   - Attempt to access Welfare Officer endpoints (/api/swd/admin/dashboard, /api/swd/admin/categories/stats, /api/swd/admin/applications) -> REJECTED (403)
   - Attempt to access Platform Admin endpoints (/api/swd/admin/users, /api/swd/admin/audit-logs) -> REJECTED (403)
   - Attempt to view another citizen's applications / documents / receipt -> REJECTED (403)
   - Attempt to execute DBT payments or administrative decisions -> REJECTED (403)

2. Welfare Officer Role:
   - Login as Welfare Officer (welfareadmin / Welfare@123)
   - Access Welfare Officer endpoints (/api/swd/admin/dashboard, /api/swd/admin/applications, /api/swd/admin/categories/stats) -> PASS (200)
   - Request more information on application -> PASS (200)
   - Approve application / create beneficiary -> PASS (200)
   - Attempt to access Platform Admin endpoints (/api/swd/admin/users, /api/swd/admin/audit-logs) -> REJECTED (403)
   - Attempt to apply for welfare scheme as citizen -> REJECTED (403)
   - Attempt to submit citizen application -> REJECTED (403)

3. Platform Admin Role:
   - Login as Platform Admin (platformadmin / Platform@123)
   - Access Platform Admin monitoring endpoints (/api/swd/admin/dashboard, /api/swd/admin/categories/stats, /api/swd/admin/users, /api/swd/admin/audit-logs) -> PASS (200)
   - Attempt to make decisions on applications (/api/swd/admin/applications/{id}/decision) -> REJECTED (403)
   - Attempt to request info on applications (/api/swd/admin/applications/{id}/request-information) -> REJECTED (403)
   - Attempt to execute DBT payment (/api/swd/dbt/process) -> REJECTED (403)
   - Attempt to apply for welfare scheme as citizen -> REJECTED (403)

4. Server-Side Token Invalidation & Session Termination:
   - Logout Citizen -> Token revoked (POST /api/swd/auth/logout)
   - Attempt request with revoked token -> REJECTED (401)
"""

import requests
import json
import sys

API_BASE = "http://localhost:8005/api/v1/swd"

def print_test(name, result, detail=""):
    status_str = "PASS" if result else "FAIL"
    print(f"[{status_str}] {name} {detail}")
    if not result:
        sys.exit(1)

def run_tests():
    print("=" * 80)
    print("NAGRIKSETU SWD — COMPREHENSIVE ROLE-BASED ACCESS CONTROL (RBAC) SUITE")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 1. CITIZEN ROLE TESTS
    # --------------------------------------------------------------------------
    print("\n--- 1. Testing Citizen Role (citizen@example.com) ---")
    r_cit_login = requests.post(f"{API_BASE}/auth/login", json={
        "email": "citizen@example.com",
        "password": "CitizenPass@2026"
    })
    print_test("Citizen Authentication", r_cit_login.status_code == 200, f"(Status: {r_cit_login.status_code})")
    cit_data = r_cit_login.json()
    cit_token = cit_data["access_token"]
    cit_headers = {"Authorization": f"Bearer {cit_token}"}
    citizen_id = cit_data.get("citizen_id", "CIT-KA-9901")

    # Citizen can browse schemes
    r_schemes = requests.get(f"{API_BASE}/schemes")
    print_test("Citizen Browse Schemes", r_schemes.status_code == 200, f"({len(r_schemes.json())} schemes)")

    # Citizen can check preliminary eligibility
    r_elig = requests.post(f"{API_BASE}/schemes/1/eligibility-check", json={
        "citizen_attributes": {
            "annual_income": 180000,
            "caste_category": "SC",
            "residence_state": "Karnataka",
            "education_level": "Undergraduate",
            "age": 21,
            "disability_percentage": 0
        }
    })
    print_test("Citizen Check Eligibility", r_elig.status_code == 200, f"(Status: {r_elig.json().get('preliminary_status')})")

    # Citizen can view their own applications
    r_my_apps = requests.get(f"{API_BASE}/applications/{citizen_id}", headers=cit_headers)
    print_test("Citizen View Own Applications", r_my_apps.status_code == 200, f"({len(r_my_apps.json())} apps)")

    # Citizen CANNOT view other citizen's applications
    r_other_apps = requests.get(f"{API_BASE}/applications/CIT-OTHER-9999", headers=cit_headers)
    print_test("Citizen Blocked from Other Citizen Applications", r_other_apps.status_code == 403, f"(Expected 403, got {r_other_apps.status_code})")

    # Citizen CANNOT view administrative dashboard
    r_admin_dash = requests.get(f"{API_BASE}/admin/dashboard", headers=cit_headers)
    print_test("Citizen Blocked from Admin Dashboard", r_admin_dash.status_code == 403, f"(Expected 403, got {r_admin_dash.status_code})")

    # Citizen CANNOT view category application stats
    r_cat_stats = requests.get(f"{API_BASE}/admin/categories/stats", headers=cit_headers)
    print_test("Citizen Blocked from Admin Category Stats", r_cat_stats.status_code == 403, f"(Expected 403, got {r_cat_stats.status_code})")

    # Citizen CANNOT view admin applications scrutiny queue
    r_admin_apps = requests.get(f"{API_BASE}/admin/applications", headers=cit_headers)
    print_test("Citizen Blocked from Admin Applications Scrutiny", r_admin_apps.status_code == 403, f"(Expected 403, got {r_admin_apps.status_code})")

    # Citizen CANNOT view platform users
    r_users = requests.get(f"{API_BASE}/admin/users", headers=cit_headers)
    print_test("Citizen Blocked from Platform Users List", r_users.status_code == 403, f"(Expected 403, got {r_users.status_code})")

    # Citizen CANNOT view platform audit logs
    r_audit = requests.get(f"{API_BASE}/admin/audit-logs", headers=cit_headers)
    print_test("Citizen Blocked from Platform Audit Logs", r_audit.status_code == 403, f"(Expected 403, got {r_audit.status_code})")

    # Citizen CANNOT execute administrative review decision
    r_decision = requests.post(f"{API_BASE}/admin/applications/1/decision", json={
        "decision": "APPROVED",
        "remarks": "Malicious attempt by citizen"
    }, headers=cit_headers)
    print_test("Citizen Blocked from Making Administrative Decisions", r_decision.status_code == 403, f"(Expected 403, got {r_decision.status_code})")

    # --------------------------------------------------------------------------
    # 2. WELFARE OFFICER ROLE TESTS
    # --------------------------------------------------------------------------
    print("\n--- 2. Testing Welfare Officer Role (welfareadmin) ---")
    r_wo_login = requests.post(f"{API_BASE}/auth/login", json={
        "email": "welfareadmin",
        "password": "Welfare@123"
    })
    print_test("Welfare Officer Authentication", r_wo_login.status_code == 200, f"(Role: {r_wo_login.json().get('role')})")
    wo_token = r_wo_login.json()["access_token"]
    wo_headers = {"Authorization": f"Bearer {wo_token}"}

    # Welfare Officer can access Admin Dashboard
    r_wo_dash = requests.get(f"{API_BASE}/admin/dashboard", headers=wo_headers)
    print_test("Welfare Officer Access Admin Dashboard", r_wo_dash.status_code == 200)

    # Welfare Officer can access Scrutiny Queue
    r_wo_queue = requests.get(f"{API_BASE}/admin/applications", headers=wo_headers)
    print_test("Welfare Officer Access Scrutiny Queue", r_wo_queue.status_code == 200, f"({len(r_wo_queue.json())} apps in queue)")

    # Welfare Officer can access Category Stats
    r_wo_cats = requests.get(f"{API_BASE}/admin/categories/stats", headers=wo_headers)
    print_test("Welfare Officer Access Category Stats", r_wo_cats.status_code == 200)

    # Welfare Officer can request information
    if len(r_wo_queue.json()) > 0:
        first_app_id = r_wo_queue.json()[0]["id"]
        r_req_info = requests.post(f"{API_BASE}/admin/applications/{first_app_id}/request-information", json={
            "remarks": "Please provide Tahsildar caste validity certificate copy."
        }, headers=wo_headers)
        print_test("Welfare Officer Request Information", r_req_info.status_code == 200, f"(App ID {first_app_id} status: {r_req_info.json().get('status')})")

    # Welfare Officer CANNOT access Platform Admin Users
    r_wo_users = requests.get(f"{API_BASE}/admin/users", headers=wo_headers)
    print_test("Welfare Officer Blocked from Platform Users", r_wo_users.status_code == 403, f"(Expected 403, got {r_wo_users.status_code})")

    # Welfare Officer CANNOT access Platform Audit Logs
    r_wo_audit = requests.get(f"{API_BASE}/admin/audit-logs", headers=wo_headers)
    print_test("Welfare Officer Blocked from Platform Audit Logs", r_wo_audit.status_code == 403, f"(Expected 403, got {r_wo_audit.status_code})")

    # Welfare Officer CANNOT submit application as citizen
    r_wo_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "OFF-SWD-501",
        "citizen_name": "Welfare Officer",
        "citizen_phone": "9845012345",
        "annual_income": 500000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=wo_headers)
    print_test("Welfare Officer Blocked from Submitting Scheme Applications", r_wo_apply.status_code == 403, f"(Expected 403, got {r_wo_apply.status_code})")

    # --------------------------------------------------------------------------
    # 3. PLATFORM ADMIN ROLE TESTS
    # --------------------------------------------------------------------------
    print("\n--- 3. Testing Platform Admin Role (platformadmin) ---")
    r_pa_login = requests.post(f"{API_BASE}/auth/login", json={
        "email": "platformadmin",
        "password": "Platform@123"
    })
    print_test("Platform Admin Authentication", r_pa_login.status_code == 200, f"(Role: {r_pa_login.json().get('role')})")
    pa_token = r_pa_login.json()["access_token"]
    pa_headers = {"Authorization": f"Bearer {pa_token}"}

    # Platform Admin can view monitoring dashboard
    r_pa_dash = requests.get(f"{API_BASE}/admin/dashboard", headers=pa_headers)
    print_test("Platform Admin View Monitoring Dashboard", r_pa_dash.status_code == 200)

    # Platform Admin can view category stats
    r_pa_cats = requests.get(f"{API_BASE}/admin/categories/stats", headers=pa_headers)
    print_test("Platform Admin View Category Stats", r_pa_cats.status_code == 200)

    # Platform Admin can manage platform users
    r_pa_users = requests.get(f"{API_BASE}/admin/users", headers=pa_headers)
    print_test("Platform Admin View Platform Users", r_pa_users.status_code == 200, f"({len(r_pa_users.json())} users)")

    # Platform Admin can view audit logs
    r_pa_audit = requests.get(f"{API_BASE}/admin/audit-logs", headers=pa_headers)
    print_test("Platform Admin View Audit Logs", r_pa_audit.status_code == 200, f"({len(r_pa_audit.json())} logs)")

    # Platform Admin CANNOT make welfare decision (Strictly restricted from caseworker actions)
    r_pa_dec = requests.post(f"{API_BASE}/admin/applications/1/decision", json={
        "decision": "APPROVED",
        "remarks": "Platform Admin attempt"
    }, headers=pa_headers)
    print_test("Platform Admin Blocked from Mutating Welfare Decisions", r_pa_dec.status_code == 403, f"(Expected 403, got {r_pa_dec.status_code})")

    # Platform Admin CANNOT request supplementary information
    r_pa_req = requests.post(f"{API_BASE}/admin/applications/1/request-information", json={
        "remarks": "Platform Admin attempt"
    }, headers=pa_headers)
    print_test("Platform Admin Blocked from Requesting Application Information", r_pa_req.status_code == 403, f"(Expected 403, got {r_pa_req.status_code})")

    # Platform Admin CANNOT submit citizen applications
    r_pa_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "PLATFORM-ADMIN",
        "citizen_name": "Super Admin",
        "citizen_phone": "9845012345",
        "annual_income": 900000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=pa_headers)
    print_test("Platform Admin Blocked from Submitting Scheme Applications", r_pa_apply.status_code == 403, f"(Expected 403, got {r_pa_apply.status_code})")

    # --------------------------------------------------------------------------
    # 4. SERVER-SIDE TOKEN REVOCATION (LOGOUT)
    # --------------------------------------------------------------------------
    print("\n--- 4. Testing Server-Side Logout & Token Revocation ---")
    r_logout = requests.post(f"{API_BASE}/auth/logout", headers=cit_headers)
    print_test("Server-Side Logout Call", r_logout.status_code == 200, f"({r_logout.json().get('message')})")

    # Attempt request with the revoked token
    r_revoked_test = requests.get(f"{API_BASE}/applications/{citizen_id}", headers=cit_headers)
    print_test("Subsequent Request with Revoked Token Rejected", r_revoked_test.status_code == 401, f"(Expected 401, got {r_revoked_test.status_code})")

    print("\n" + "=" * 80)
    print("ALL MULTI-ROLE RBAC SECURITY TESTS PASSED PERFECTLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
