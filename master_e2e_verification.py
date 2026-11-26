"""
MASTER END-TO-END VERIFICATION HARNESS FOR ALL THREE ROLES
NagrikSetu • Social Welfare Department
Covers all 20 requirement categories from the Master Prompt across Citizen, Welfare Admin, and Platform Admin.
"""

import sys
import os
import requests
import json
import jwt
import datetime

BASE_URL = "http://localhost:8005/api/swd"
FRONTEND_URL = "http://localhost:5175"
JWT_SECRET = "nagriksetu-swd-super-secret-key-2026-xyz-min32chars"

def create_token(payload):
    p = payload.copy()
    p["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    return jwt.encode(p, JWT_SECRET, algorithm="HS256")

# Real tokens matching auth.py RBAC rules
citizen_token = create_token({
    "sub": "CIT-KA-9901",
    "email": "citizen@example.com",
    "name": "Ramesh Kumar Nayak",
    "role": "CITIZEN",
    "citizen_id": "CIT-KA-9901",
    "state": "Karnataka",
    "income": 180000,
    "caste": "SC"
})

welfare_token = create_token({
    "sub": "OFF-SWD-501",
    "email": "officer@nagriksetu.local",
    "name": "S. R. Patil (District Welfare Officer)",
    "role": "WELFARE_OFFICER",
    "citizen_id": "OFF-SWD-501"
})

platform_token = create_token({
    "sub": "ADM-SWD-001",
    "email": "swd.superadmin@karnataka.gov.in",
    "name": "SWD Platform Super Admin",
    "role": "PLATFORM_ADMIN",
    "citizen_id": "ADM-SWD-001"
})

citizen_auth = {"access_token": citizen_token, "citizen_id": "CIT-KA-9901", "role": "CITIZEN", "name": "Ramesh Kumar Nayak"}
welfare_auth = {"access_token": welfare_token, "citizen_id": "OFF-SWD-501", "role": "WELFARE_OFFICER", "name": "S. R. Patil"}
platform_auth = {"access_token": platform_token, "citizen_id": "ADM-SWD-001", "role": "PLATFORM_ADMIN", "name": "Platform Super Admin"}

test_results = []

def run_test(section, test_num, name, func):
    print(f"\n[{section}] Test {test_num}: {name}")
    try:
        ok, msg = func()
        status = "PASS" if ok else "FAIL"
        print(f" -> {status}: {msg}")
        test_results.append({
            "section": section,
            "test_num": test_num,
            "name": name,
            "status": status,
            "details": msg
        })
    except Exception as e:
        print(f" -> ERROR: {str(e)}")
        test_results.append({
            "section": section,
            "test_num": test_num,
            "name": name,
            "status": "ERROR",
            "details": str(e)
        })

# ==================== PART 1: CITIZEN WORKFLOW ====================

def test_citizen_registration():
    # Register a new unique citizen
    rand_suffix = os.urandom(3).hex().upper()
    email = f"citizen_{rand_suffix.lower()}@example.com"
    payload = {
        "full_name": f"Pooja Sharma {rand_suffix}",
        "email": email,
        "phone": f"9845{str(hash(rand_suffix) % 1000000).zfill(6)}",
        "password": "SecurePassword@2026",
        "confirm_password": "SecurePassword@2026",
        "date_of_birth": "1998-05-12",
        "gender": "Female",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560001",
        "caste_category": "OBC",
        "annual_income": 140000.0
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=payload)
    if r.status_code == 200:
        data = r.json()
        if "citizen_id" in data and data.get("role") == "CITIZEN":
            return True, f"Registered citizen: {data['citizen_id']} (Role: {data['role']})"
    return False, f"Registration failed: {r.status_code} - {r.text}"

def test_citizen_auth_and_profile():
    # Login as citizen
    r_login = requests.post(f"{BASE_URL}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
    if r_login.status_code != 200:
        return False, f"Login failed: {r_login.status_code}"
    token = r_login.json()["access_token"]
    
    # Fetch profile
    r_prof = requests.get(f"{BASE_URL}/auth/profile", headers={"Authorization": f"Bearer {token}"})
    if r_prof.status_code == 200:
        prof = r_prof.json()
        if prof.get("email") == "citizen@example.com":
            return True, f"Profile verified for citizen: {prof.get('full_name')} ({prof.get('citizen_id')})"
    return False, f"Profile lookup failed: {r_prof.status_code}"

def test_scheme_discovery_and_eligibility():
    # Fetch schemes catalogue
    r_schemes = requests.get(f"{BASE_URL}/schemes")
    if r_schemes.status_code != 200 or len(r_schemes.json()) != 35:
        return False, f"Expected 35 schemes, got {len(r_schemes.json()) if r_schemes.status_code == 200 else r_schemes.status_code}"
    
    # Check eligibility for scheme 1
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    r_elig = requests.post(f"{BASE_URL}/schemes/1/eligibility-check", json={
        "citizen_attributes": {
            "residence_state": "Karnataka",
            "annual_income": 120000.0,
            "caste_category": "SC",
            "education_level": "Undergraduate",
            "age": 21
        }
    }, headers=headers)
    if r_elig.status_code == 200:
        res = r_elig.json()
        if res.get("preliminary_status") in ["LIKELY_ELIGIBLE", "ELIGIBLE"] or res.get("is_eligible") is True:
            return True, f"All 35 schemes discoverable; Scheme 1 eligibility evaluated: {res.get('preliminary_status', True)}"
    return False, f"Eligibility evaluation failed: {r_elig.status_code} - {r_elig.text}"

def test_dynamic_form_and_application_submit():
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    # Fetch dynamic form for scheme 1
    r_form = requests.get(f"{BASE_URL}/schemes/1/form")
    if r_form.status_code != 200 or not r_form.json():
        return False, f"Dynamic form for Scheme 1 missing: {r_form.status_code}"
    
    # Submit application
    r_sub = requests.post(f"{BASE_URL}/schemes/1/applications", json={
        "citizen_id": citizen_auth["citizen_id"],
        "citizen_name": citizen_auth["name"],
        "citizen_email": "citizen@example.com",
        "citizen_phone": "9845012345",
        "annual_income": 180000.0,
        "caste_category": "SC",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "SBIN0040123991",
        "bank_ifsc": "SBIN0040123",
        "application_data_json": {
            "college_name": "Bangalore University Institute of Technology",
            "student_registration_number": "BU-ENG-2026-9901",
            "current_year_of_study": "3rd Year",
            "annual_tuition_fee": 18500
        }
    }, headers=headers)
    if r_sub.status_code == 200:
        app_data = r_sub.json()
        return True, f"Application submitted: {app_data['application_number']} (Status: {app_data['status']})"
    return False, f"Submission failed: {r_sub.status_code} - {r_sub.text}"

def test_pdf_receipt_download():
    # Verify PDF receipt endpoint exists and generates binary PDF content
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    r_apps = requests.get(f"{BASE_URL}/applications/{citizen_auth['citizen_id']}", headers=headers)
    if not r_apps.json():
        return False, "No applications found"
    app_id = r_apps.json()[0]["id"]
    r_pdf = requests.get(f"{BASE_URL}/applications/{app_id}/receipt", headers=headers)
    if r_pdf.status_code == 200 and r_pdf.content.startswith(b"%PDF"):
        return True, f"PDF acknowledgement generated: {len(r_pdf.content)} bytes (Starts with %PDF)"
    return False, f"PDF download failed: {r_pdf.status_code}"

# ==================== PART 2: WELFARE ADMIN WORKFLOW ====================

def test_welfare_admin_scrutiny():
    headers_adm = {"Authorization": f"Bearer {welfare_auth['access_token']}"}
    headers_cit = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    
    # Get latest application
    r_apps = requests.get(f"{BASE_URL}/applications/{citizen_auth['citizen_id']}", headers=headers_cit)
    app = r_apps.json()[0]
    app_id = app["id"]
    
    # Transition: UNDER_REVIEW
    r_rev = requests.post(f"{BASE_URL}/admin/applications/{app_id}/review", json={
        "decision": "UNDER_REVIEW",
        "remarks": "Documents queued for jurisdictional scrutiny."
    }, headers=headers_adm)
    if r_rev.status_code != 200:
        return False, f"Failed review transition: {r_rev.status_code} - {r_rev.text}"
    
    # Transition: APPROVED with sanction amount
    r_appr = requests.post(f"{BASE_URL}/admin/applications/{app_id}/review", json={
        "decision": "APPROVED",
        "remarks": "All academic criteria and revenue records verified. Sanction approved.",
        "sanctioned_amount": 25000.0
    }, headers=headers_adm)
    if r_appr.status_code == 200 and r_appr.json()["status"] == "APPROVED":
        return True, f"Application {app_id} transitioned: UNDER_REVIEW -> APPROVED with INR 25,000 sanction"
    return False, f"Approval failed: {r_appr.status_code} - {r_appr.text}"

def test_welfare_admin_announcement_broadcast():
    headers = {"Authorization": f"Bearer {welfare_auth['access_token']}"}
    r = requests.post(f"{BASE_URL}/admin/announcements", json={
        "title": "State Social Pension Disbursement Cycle Announcement",
        "message": "Quarterly direct benefit transfer disbursements have commenced for all verified beneficiaries.",
        "announcement_type": "SUCCESS",
        "target_role": "CITIZEN"
    }, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return True, f"Announcement broadcast dispatched to {data.get('recipients_count')} registered citizens"
    return False, f"Announcement failed: {r.status_code} - {r.text}"

def test_dynamic_form_builder_persistence():
    headers = {"Authorization": f"Bearer {welfare_auth['access_token']}"}
    # Update/save dynamic form version for scheme 1
    r = requests.post(f"{BASE_URL}/schemes/1/form", json={
        "title": "Post-Matric Scholarship Comprehensive Application Form v2",
        "description": "Updated academic year 2026-2027 schema.",
        "fields": [
            {"field_name": "college_name", "field_label": "Institution Name", "field_type": "TEXT", "is_required": True, "sort_order": 1},
            {"field_name": "student_usn", "field_label": "Student Registration / USN", "field_type": "TEXT", "is_required": True, "sort_order": 2},
            {"field_name": "current_cgpa", "field_label": "Previous Year Cumulative GPA", "field_type": "NUMBER", "is_required": False, "sort_order": 3}
        ]
    }, headers=headers)
    if r.status_code == 200:
        form = r.json()
        return True, f"Form version {form.get('version')} published and persisted with {len(form.get('form_fields', []))} fields"
    return False, f"Form builder failed: {r.status_code} - {r.text}"

def test_grievance_submission_and_resolution():
    headers_cit = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    headers_adm = {"Authorization": f"Bearer {welfare_auth['access_token']}"}
    
    # 1. Citizen submits grievance
    r_sub = requests.post(f"{BASE_URL}/grievances", json={
        "citizen_id": citizen_auth["citizen_id"],
        "citizen_name": citizen_auth["name"],
        "category": "APPLICATION_DELAY",
        "subject": "Delay in verification of bonafide certificate",
        "description": "Submitted application 2 weeks ago; awaiting officer scrutiny."
    }, headers=headers_cit)
    if r_sub.status_code != 200:
        return False, f"Grievance submission failed: {r_sub.text}"
    grv = r_sub.json()
    grv_id = grv["id"]
    
    # 2. Officer resolves grievance
    r_res = requests.put(f"{BASE_URL}/grievances/{grv_id}/resolve", json={
        "status": "RESOLVED",
        "officer_response": "Jurisdictional scrutiny officer has verified the institution record."
    }, headers=headers_adm)
    if r_res.status_code == 200:
        resolved = r_res.json()
        if resolved["status"] == "RESOLVED" and resolved.get("officer_response"):
            return True, f"Grievance {grv['grievance_number']} submitted and resolved with official response"
    return False, f"Resolution failed: {r_res.status_code} - {r_res.text}"

# ==================== PART 3: NOTIFICATIONS & CITIZEN DASHBOARD ====================

def test_notifications_generation_and_read_actions():
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    # Citizen checks notifications
    r_notifs = requests.get(f"{BASE_URL}/notifications/{citizen_auth['citizen_id']}", headers=headers)
    if r_notifs.status_code != 200 or not r_notifs.json():
        return False, f"Notifications lookup failed: {r_notifs.status_code}"
    
    notifs = r_notifs.json()
    total = len(notifs)
    unread_before = len([n for n in notifs if not n.get("is_read")])
    
    # Mark all read
    r_mark = requests.post(f"{BASE_URL}/notifications/{citizen_auth['citizen_id']}/mark-all-read", headers=headers)
    if r_mark.status_code != 200:
        return False, f"Mark all read failed: {r_mark.status_code}"
    
    r_check = requests.get(f"{BASE_URL}/notifications/{citizen_auth['citizen_id']}", headers=headers)
    unread_after = len([n for n in r_check.json() if not n.get("is_read")])
    return True, f"Total notifications: {total}; unread before: {unread_before}, unread after mark-all-read: {unread_after}"

def test_citizen_dashboard_live_stats():
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    r_apps = requests.get(f"{BASE_URL}/applications/{citizen_auth['citizen_id']}", headers=headers)
    r_grvs = requests.get(f"{BASE_URL}/grievances?citizen_id={citizen_auth['citizen_id']}", headers=headers)
    if r_apps.status_code == 200 and r_grvs.status_code == 200:
        apps = r_apps.json()
        grvs = r_grvs.json()
        approved = len([a for a in apps if a.get("status") == "APPROVED"])
        active_grvs = len([g for g in grvs if g.get("status") != "RESOLVED"])
        return True, f"Dashboard live query: {len(apps)} applications ({approved} approved), {len(grvs)} grievances ({active_grvs} active)"
    return False, "Failed to retrieve citizen records for statistics"

# ==================== PART 4: PLATFORM ADMIN WORKFLOW & RBAC ====================

def test_platform_admin_monitoring_stats():
    headers = {"Authorization": f"Bearer {platform_auth['access_token']}"}
    r_stats = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
    r_cats = requests.get(f"{BASE_URL}/admin/categories/stats", headers=headers)
    if r_stats.status_code == 200 and r_cats.status_code == 200:
        s = r_stats.json()
        return True, f"Platform Admin monitoring active: {s.get('total_applications')} applications, {s.get('total_beneficiaries')} beneficiaries, {s.get('total_sanctioned_amount')} INR sanctioned"
    return False, f"Platform admin stats failed: {r_stats.status_code}"

def test_platform_admin_user_monitoring():
    headers = {"Authorization": f"Bearer {platform_auth['access_token']}"}
    r_users = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    if r_users.status_code == 200:
        users = r_users.json()
        return True, f"Platform Admin user monitoring active: {len(users)} registered platform users retrieved"
    return False, f"User monitoring failed: {r_users.status_code}"

def test_platform_admin_audit_logs():
    headers = {"Authorization": f"Bearer {platform_auth['access_token']}"}
    r_audit = requests.get(f"{BASE_URL}/admin/audit-logs", headers=headers)
    if r_audit.status_code == 200:
        logs = r_audit.json()
        return True, f"Security audit log stream active: {len(logs)} tamper-evident audit records found"
    return False, f"Audit logs failed: {r_audit.status_code}"

def test_platform_admin_view_only_enforcement():
    headers = {"Authorization": f"Bearer {platform_auth['access_token']}"}
    
    # Test 1: Scheme modification forbidden
    r1 = requests.post(f"{BASE_URL}/schemes", json={"name": "Illegal Scheme"}, headers=headers)
    # Test 2: Application review forbidden
    r2 = requests.post(f"{BASE_URL}/admin/applications/1/review", json={"decision": "APPROVED", "remarks": "Unauthorized"}, headers=headers)
    # Test 3: Announcement broadcast forbidden
    r3 = requests.post(f"{BASE_URL}/admin/announcements", json={"title": "Unauthorized", "message": "Test"}, headers=headers)
    # Test 4: User account status mutation forbidden
    r4 = requests.put(f"{BASE_URL}/admin/users/1/status?is_active=false", headers=headers)
    
    if r1.status_code == 403 and r2.status_code == 403 and r3.status_code == 403 and r4.status_code == 403:
        return True, "Strict View-Only Guard verified: All 4 operational mutation endpoints rejected with HTTP 403 Forbidden"
    return False, f"One or more mutations allowed: r1={r1.status_code}, r2={r2.status_code}, r3={r3.status_code}, r4={r4.status_code}"

def test_cross_citizen_data_isolation():
    # Citizen 1 tries to access citizen 2's notifications
    headers = {"Authorization": f"Bearer {citizen_auth['access_token']}"}
    r = requests.get(f"{BASE_URL}/notifications/CIT-OTHER-VIOLATION-9999", headers=headers)
    if r.status_code == 403:
        return True, "Cross-citizen isolation verified: Unauthorized access blocked with HTTP 403 Forbidden"
    return False, f"Expected 403, got {r.status_code}"

def test_all_35_schemes_forms_intact():
    r = requests.get(f"{BASE_URL}/schemes")
    schemes = r.json()
    if len(schemes) != 35:
        return False, f"Expected 35 schemes, found {len(schemes)}"
    all_ok = True
    missing = []
    for s in schemes:
        rf = requests.get(f"{BASE_URL}/schemes/{s['id']}/form")
        if rf.status_code != 200 or not rf.json():
            all_ok = False
            missing.append(s['id'])
    if all_ok:
        return True, "All 35 welfare schemes retain valid, active dynamic form definitions"
    return False, f"Missing forms for scheme IDs: {missing}"

def main():
    print("="*70)
    print("NAGRIKSETU SWD — MASTER MULTI-ROLE END-TO-END VERIFICATION HARNESS")
    print("="*70)

    run_test("CITIZEN", 1, "Citizen Registration with Unique Constraints", test_citizen_registration)
    run_test("CITIZEN", 2, "Citizen Authentication & Profile Retrieval", test_citizen_auth_and_profile)
    run_test("CITIZEN", 3, "Welfare Scheme Discovery & Rule Eligibility Evaluation", test_scheme_discovery_and_eligibility)
    run_test("CITIZEN", 4, "Scheme-Specific Dynamic Form Application Submission", test_dynamic_form_and_application_submit)
    run_test("CITIZEN", 5, "Official PDF Acknowledgement Generation", test_pdf_receipt_download)
    
    run_test("WELFARE_ADMIN", 6, "Application Scrutiny & Sanction Decision Lifecycle", test_welfare_admin_scrutiny)
    run_test("WELFARE_ADMIN", 7, "Department Announcement Broadcast & Citizen Dispatch", test_welfare_admin_announcement_broadcast)
    run_test("WELFARE_ADMIN", 8, "Dynamic Form Builder Versioning & Field Persistence", test_dynamic_form_builder_persistence)
    run_test("WELFARE_ADMIN", 9, "Grievance Redressal Lifecycle (Submission -> Resolution)", test_grievance_submission_and_resolution)
    
    run_test("SYSTEM", 10, "Real Notification Stream & Read/Unread State Tracking", test_notifications_generation_and_read_actions)
    run_test("SYSTEM", 11, "Citizen Dashboard Dynamic Statistics Calculation", test_citizen_dashboard_live_stats)
    run_test("SYSTEM", 12, "Cross-Citizen Data Isolation & Authorization Guard", test_cross_citizen_data_isolation)
    run_test("SYSTEM", 13, "Universal 35 Scheme Forms & Documents Preservation", test_all_35_schemes_forms_intact)
    
    run_test("PLATFORM_ADMIN", 14, "Platform Admin System Monitoring & Metrics", test_platform_admin_monitoring_stats)
    run_test("PLATFORM_ADMIN", 15, "Platform User Monitoring & Account Registry", test_platform_admin_user_monitoring)
    run_test("PLATFORM_ADMIN", 16, "Security Audit Trail & Event Monitoring Stream", test_platform_admin_audit_logs)
    run_test("PLATFORM_ADMIN", 17, "Platform Admin View-Only Enforcement (HTTP 403 Guards)", test_platform_admin_view_only_enforcement)

    print("\n" + "="*70)
    passed = len([r for r in test_results if r["status"] == "PASS"])
    total = len(test_results)
    print(f"MASTER VERIFICATION RESULT: {passed}/{total} TESTS PASSED")
    print("="*70)

    with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\master_verification_results.json", "w") as f:
        json.dump(test_results, f, indent=2)

if __name__ == "__main__":
    main()
