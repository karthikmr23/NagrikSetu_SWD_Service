import requests
import sys

API_BASE = "http://localhost:8005/api/v1/swd"

def print_test(name, passed, detail=""):
    status_str = "PASS" if passed else "FAIL"
    print(f"[{status_str}] {name} {detail}")
    if not passed:
        sys.exit(1)

def run():
    print("=" * 80)
    print("NAGRIKSETU SWD — COMPREHENSIVE CITIZEN, GRIEVANCE & PLATFORM ADMIN PERMISSION SUITE")
    print("=" * 80)

    # 1. Login all 3 roles
    r_cit = requests.post(f"{API_BASE}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
    print_test("Citizen Login", r_cit.status_code == 200, f"(Role: {r_cit.json().get('role')})")
    cit_tok = r_cit.json()["access_token"]
    cit_id = r_cit.json().get("citizen_id", "CIT-KA-9901")
    cit_h = {"Authorization": f"Bearer {cit_tok}"}

    r_wo = requests.post(f"{API_BASE}/auth/login", json={"email": "welfareadmin", "password": "Welfare@123"})
    print_test("Welfare Officer Login", r_wo.status_code == 200, f"(Role: {r_wo.json().get('role')})")
    wo_tok = r_wo.json()["access_token"]
    wo_h = {"Authorization": f"Bearer {wo_tok}"}

    r_pa = requests.post(f"{API_BASE}/auth/login", json={"email": "platformadmin", "password": "Platform@123"})
    print_test("Platform Admin Login", r_pa.status_code == 200, f"(Role: {r_pa.json().get('role')})")
    pa_tok = r_pa.json()["access_token"]
    pa_h = {"Authorization": f"Bearer {pa_tok}"}

    # 2. Test Citizen Profile & Editing
    print("\n--- 2. Citizen Profile & Persistence ---")
    r_prof = requests.get(f"{API_BASE}/auth/profile", headers=cit_h)
    print_test("Fetch Citizen Profile", r_prof.status_code == 200, f"(Name: {r_prof.json().get('full_name')})")
    
    r_upd_prof = requests.put(f"{API_BASE}/auth/profile", json={
        "full_name": "Ramesh Kumar Nayak",
        "phone": "9845012345",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "taluk": "Bengaluru South",
        "caste_category": "SC"
    }, headers=cit_h)
    print_test("Update Citizen Profile", r_upd_prof.status_code == 200, f"(Persisted: {r_upd_prof.json().get('full_name')})")

    # 3. Test My Applications & Cross-Citizen Isolation
    print("\n--- 3. My Applications & Cross-Citizen Data Isolation ---")
    r_my_apps = requests.get(f"{API_BASE}/applications/{cit_id}", headers=cit_h)
    print_test("Fetch Own Applications", r_my_apps.status_code == 200, f"({len(r_my_apps.json())} apps retrieved)")
    
    # Attempting to fetch another citizen's applications
    r_foreign_apps = requests.get(f"{API_BASE}/applications/CIT-OTHER-9999", headers=cit_h)
    print_test("Cross-Citizen Data Isolation (Foreign Dossiers)", r_foreign_apps.status_code == 403, f"(Expected 403, got {r_foreign_apps.status_code})")

    # Attempting to fetch another citizen's receipt
    r_foreign_receipt = requests.get(f"{API_BASE}/applications/999/receipt", headers=cit_h)
    print_test("Cross-Citizen Receipt Isolation", r_foreign_receipt.status_code in [403, 404], f"(Expected 403/404, got {r_foreign_receipt.status_code})")

    # 4. Test Citizen Grievance Workflow
    print("\n--- 4. Citizen Grievance Submission, Officer Resolution & Notification ---")
    r_new_grv = requests.post(f"{API_BASE}/grievances", json={
        "citizen_id": cit_id,
        "citizen_name": "Ramesh Kumar Nayak",
        "category": "DBT_PAYMENT_DELAY",
        "subject": "Delay in DBT Sanction Credit for Post-Matric Hostel Fee",
        "description": "Please verify if the Aadhaar bridge payment has been initiated for the current semester."
    }, headers=cit_h)
    print_test("Submit Citizen Grievance", r_new_grv.status_code == 200, f"(Grievance #: {r_new_grv.json().get('grievance_number')})")
    grv_id = r_new_grv.json()["id"]
    grv_num = r_new_grv.json()["grievance_number"]

    # Citizen viewing own grievances
    r_cit_grvs = requests.get(f"{API_BASE}/grievances", headers=cit_h)
    print_test("Citizen View Own Grievances", r_cit_grvs.status_code == 200, f"({len(r_cit_grvs.json())} grievances listed)")

    # Citizen Notifications
    r_notifs = requests.get(f"{API_BASE}/notifications/{cit_id}", headers=cit_h)
    print_test("Citizen View Notifications", r_notifs.status_code == 200, f"({len(r_notifs.json())} notifications)")

    # Welfare Officer resolving grievance
    r_resolve = requests.put(f"{API_BASE}/grievances/{grv_id}/resolve", json={
        "status": "RESOLVED",
        "officer_response": "DBT batch approved and sent to State Direct Benefit Transfer cell. Credit expected in 48 hours."
    }, headers=wo_h)
    print_test("Welfare Officer Resolve Grievance", r_resolve.status_code == 200, f"(Status: {r_resolve.json().get('status')})")

    # Verify citizen now sees officer response
    r_cit_grv_updated = requests.get(f"{API_BASE}/grievances", headers=cit_h)
    matching = [g for g in r_cit_grv_updated.json() if g["id"] == grv_id]
    has_resp = len(matching) > 0 and matching[0].get("officer_response") is not None
    print_test("Citizen Visible Officer Response", has_resp, f"(Officer note: {matching[0].get('officer_response')[:50]}...)")

    # 5. Strict Platform Admin View-Only Permissions
    print("\n--- 5. Platform Admin Strict View-Only Permission Checks ---")
    
    # PA viewing grievances (read-only audit)
    r_pa_grv_list = requests.get(f"{API_BASE}/grievances", headers=pa_h)
    print_test("Platform Admin View-Only Grievance Audit", r_pa_grv_list.status_code == 200, f"({len(r_pa_grv_list.json())} total grievances audited)")

    # PA attempting to resolve/close grievance -> MUST BE 403
    r_pa_resolve = requests.put(f"{API_BASE}/grievances/{grv_id}/resolve", json={
        "status": "RESOLVED",
        "officer_response": "Platform Admin unauthorized resolution attempt"
    }, headers=pa_h)
    print_test("Platform Admin Blocked from Resolving Grievance", r_pa_resolve.status_code == 403, f"(Expected 403, got {r_pa_resolve.status_code})")

    # PA attempting to modify user roles -> MUST BE 403
    r_pa_role = requests.put(f"{API_BASE}/admin/users/1/role?role=ADMINISTRATOR", headers=pa_h)
    print_test("Platform Admin Blocked from Changing User Roles", r_pa_role.status_code == 403, f"(Expected 403, got {r_pa_role.status_code})")

    # PA attempting to toggle user status -> MUST BE 403
    r_pa_status = requests.put(f"{API_BASE}/admin/users/1/status?is_active=false", headers=pa_h)
    print_test("Platform Admin Blocked from Modifying Citizen/User Status", r_pa_status.status_code == 403, f"(Expected 403, got {r_pa_status.status_code})")

    # PA attempting to create a scheme -> MUST BE 403
    r_pa_create_scheme = requests.post(f"{API_BASE}/schemes", json={
        "scheme_code": "TEST-SCHEME",
        "name": "Test Scheme",
        "category_id": 1,
        "department": "Test",
        "administering_authority": "Test",
        "description": "Test",
        "benefit_summary": "Test",
        "benefit_type": "CASH",
        "eligibility_summary": "Test",
        "application_instructions": "Test",
        "application_start_date": "2026-01-01",
        "application_end_date": "2026-12-31"
    }, headers=pa_h)
    print_test("Platform Admin Blocked from Creating Schemes", r_pa_create_scheme.status_code == 403, f"(Expected 403, got {r_pa_create_scheme.status_code})")

    # PA attempting to approve/reject an application -> MUST BE 403
    r_pa_decision = requests.post(f"{API_BASE}/admin/applications/1/decision", json={
        "decision": "APPROVED",
        "remarks": "Unauthorized Platform Admin decision"
    }, headers=pa_h)
    print_test("Platform Admin Blocked from Application Decisions", r_pa_decision.status_code == 403, f"(Expected 403, got {r_pa_decision.status_code})")

    print("\n" + "=" * 80)
    print("ALL VERIFICATION AND RBAC PERMISSION TESTS PASSED!")
    print("=" * 80)

if __name__ == "__main__":
    run()
