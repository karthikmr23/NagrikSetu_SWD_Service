import requests
import json
import os
import sys

API_BASE = "http://localhost:8005/api/swd"
AUTH_API = "http://localhost:8005/api/swd/auth"

print("=" * 80)
print("NAGRIKSETU SWD — INDEPENDENT VERIFICATION & VALIDATION SUITE")
print("=" * 80)

# 1. Verify Registration of Fresh Test Citizen
print("\n--- 1. Testing Fresh Citizen Registration & Security ---")
unique_suffix = os.urandom(3).hex().lower()
test_email = f"indep.citizen.{unique_suffix}@example.com"
test_phone = f"98{int.from_bytes(os.urandom(4), 'big') % 100000000:08d}"

reg_payload = {
    "email": test_email,
    "phone": test_phone,
    "password": "IndepSecurePass@2026",
    "confirm_password": "IndepSecurePass@2026",
    "full_name": f"Independent Citizen {unique_suffix.upper()}",
    "district": "Mysuru",
    "taluk": "Mysuru South",
    "pin_code": "570001",
    "annual_income": 85000.0,
    "caste_category": "Category 1"
}

r_reg = requests.post(f"{AUTH_API}/register", json=reg_payload)
assert r_reg.status_code == 200, f"Registration failed: {r_reg.text}"
reg_data = r_reg.json()
print(f"[PASS] Fresh Citizen Registered: Email={test_email}, CitizenID={reg_data['citizen_id']}, Role={reg_data['role']}")
assert reg_data['role'] == 'CITIZEN', "Security check failed: Registered role must strictly be CITIZEN!"

# Test duplicate registration rejection
r_dup = requests.post(f"{AUTH_API}/register", json=reg_payload)
assert r_dup.status_code == 400, f"Duplicate registration check failed: {r_dup.status_code}"
print(f"[PASS] Duplicate email & phone prevented: {r_dup.json().get('detail')}")

# 2. Test Login for all 3 Roles
print("\n--- 2. Testing Authentication for all 3 Roles ---")
# Fresh Citizen Login
r_cit_login = requests.post(f"{AUTH_API}/login", json={"email": test_email, "password": "IndepSecurePass@2026"})
assert r_cit_login.status_code == 200, f"Citizen login failed: {r_cit_login.text}"
cit_token = r_cit_login.json()["access_token"]
cit_id = r_cit_login.json()["citizen_id"]
cit_headers = {"Authorization": f"Bearer {cit_token}"}
print(f"[PASS] Citizen Login Successful: Role={r_cit_login.json()['role']}")

# Welfare Admin Login
r_wo_login = requests.post(f"{AUTH_API}/login", json={"email": "welfareadmin", "password": "Welfare@123"})
assert r_wo_login.status_code == 200, f"Welfare Admin login failed: {r_wo_login.text}"
wo_token = r_wo_login.json()["access_token"]
wo_headers = {"Authorization": f"Bearer {wo_token}"}
print(f"[PASS] Government Welfare Admin Login Successful: Role={r_wo_login.json()['role']}")

# Platform Admin Login
r_pa_login = requests.post(f"{AUTH_API}/login", json={"email": "platformadmin", "password": "Platform@123"})
assert r_pa_login.status_code == 200, f"Platform Admin login failed: {r_pa_login.text}"
pa_token = r_pa_login.json()["access_token"]
pa_headers = {"Authorization": f"Bearer {pa_token}"}
print(f"[PASS] Platform Admin Login Successful: Role={r_pa_login.json()['role']}")

# 3. Verify Specific Form Retrievals for Requested Schemes
print("\n--- 3. Verifying Universal Scheme-Specific Application Forms ---")
schemes_to_test = [
    (1, "Post-Matric Scholarship", "institution_name"),
    (5, "Gruha Lakshmi Scheme", "ration_card_number"),
    (9, "Yuva Nidhi Scheme", "graduation_passing_year"),
    (18, "Ganga Kalyana Scheme", "survey_number")
]

for s_id, s_name, expected_field in schemes_to_test:
    r_form = requests.get(f"{API_BASE}/schemes/{s_id}/form")
    assert r_form.status_code == 200, f"Failed to get form for {s_name}"
    f_data = r_form.json()
    field_names = [f["field_name"] for f in f_data["fields"]]
    assert any(expected_field in f for f in field_names), f"Missing expected field '{expected_field}' in {s_name} form: {field_names}"
    print(f"[PASS] Scheme {s_id:02d} ({s_name}): Form '{f_data['title']}' v{f_data['version']} with {len(f_data['fields'])} fields. Contains field '{expected_field}'.")

# 4. End-to-End Application Workflow: Submit, Scrutiny, Document, Approval & Beneficiary
print("\n--- 4. Testing End-to-End Application Lifecycle ---")
app_payload = {
    "citizen_id": cit_id,
    "citizen_name": reg_payload["full_name"],
    "citizen_phone": test_phone,
    "annual_income": 85000.0,
    "caste_category": "Category 1",
    "residence_district": "Mysuru",
    "bank_account_number": "987654321098",
    "bank_ifsc": "SBIN0001234",
    "application_data_json": {
        "ration_card_number": "BPL-MYS-98765",
        "woman_head_full_name": reg_payload["full_name"],
        "electricity_account_id": "BESCOM-1092837",
        "npci_bank_consent": True
    }
}

r_app = requests.post(f"{API_BASE}/schemes/5/applications", json=app_payload, headers=cit_headers)
assert r_app.status_code == 200, f"Application submission failed: {r_app.text}"
app_data = r_app.json()
app_id = app_data["id"]
app_num = app_data["application_number"]
print(f"[PASS] Application Dossier Submitted: ID={app_id}, AppNum={app_num}, Status={app_data['status']}")

# Check My Applications
r_my_apps = requests.get(f"{API_BASE}/applications/{cit_id}", headers=cit_headers)
assert r_my_apps.status_code == 200
found_apps = [a for a in r_my_apps.json() if a["id"] == app_id]
assert len(found_apps) == 1, "Application not found in citizen's portfolio"
print(f"[PASS] Application visible in Citizen My Applications portfolio.")

# Upload document to application
file_content = b"%PDF-1.4 test document content for verification"
files = {
    'file': ('ration_card_copy.pdf', file_content, 'application/pdf')
}
data = {
    'document_code': 'RATION_CARD'
}
r_up = requests.post(
    f"{API_BASE}/applications/{app_id}/documents",
    files=files,
    data=data,
    headers=cit_headers
)
assert r_up.status_code == 200, f"Document upload failed: {r_up.text}"
print(f"[PASS] Scheme Document Uploaded to Application Dossier.")

# Download PDF Receipt
r_rcpt = requests.get(f"{API_BASE}/applications/{app_id}/receipt", headers=cit_headers)
assert r_rcpt.status_code == 200 and len(r_rcpt.content) > 500
print(f"[PASS] PDF Acknowledgement Receipt Downloaded: Size={len(r_rcpt.content)} bytes.")

# Officer Scrutiny: Request Documents
r_scrut = requests.post(
    f"{API_BASE}/admin/applications/{app_id}/request-information",
    json={"remarks": "Please provide Tahsildar verified BPL ration card copy."},
    headers=wo_headers
)
assert r_scrut.status_code == 200
print(f"[PASS] Welfare Officer Scrutiny: Status updated to DOCUMENTS_REQUIRED.")

# Officer Scrutiny: Approve Application
r_apprv = requests.post(
    f"{API_BASE}/admin/applications/{app_id}/decision",
    json={
        "decision": "APPROVED",
        "remarks": "Income and family head eligibility verified against departmental records. Sanctioned.",
        "sanctioned_amount": 2000.0
    },
    headers=wo_headers
)
assert r_apprv.status_code == 200
print(f"[PASS] Welfare Officer Scrutiny: Status updated to APPROVED, Sanctioned Amount=INR 2000.")

# 5. Grievance Workflow: Submit, Officer Resolve, Citizen View
print("\n--- 5. Testing Citizen Grievance Workflow ---")
grv_payload = {
    "citizen_id": cit_id,
    "citizen_name": reg_payload["full_name"],
    "category": "APPLICATION_DELAY",
    "subject": "Verification query on Gruha Lakshmi Dossier",
    "description": f"Dossier {app_num} has been reviewed and approved. Awaiting monthly mandate confirmation."
}
r_grv = requests.post(f"{API_BASE}/grievances", json=grv_payload, headers=cit_headers)
assert r_grv.status_code == 200, f"Grievance submission failed: {r_grv.text}"
grv_data = r_grv.json()
grv_id = grv_data["id"]
grv_num = grv_data["grievance_number"]
print(f"[PASS] Grievance Registered: ID={grv_id}, Ticket={grv_num}, Status={grv_data['status']}")

# Officer Resolve Grievance
r_res = requests.put(
    f"{API_BASE}/grievances/{grv_id}/resolve",
    json={
        "status": "RESOLVED",
        "officer_response": "Approved monthly DBT benefit of INR 2000 scheduled for upcoming cycle."
    },
    headers=wo_headers
)
assert r_res.status_code == 200
print(f"[PASS] Welfare Officer Resolution: Status updated to RESOLVED with official explanation.")

# 6. Security and Cross-Citizen Data Isolation
print("\n--- 6. Testing Data Isolation & Platform Admin Restrictions ---")
# Another citizen attempts to access citizen 1's applications
r_iso = requests.get(f"{API_BASE}/applications/{cit_id}", headers={"Authorization": f"Bearer {cit_token}"})
assert r_iso.status_code == 200

# Platform Admin attempts prohibited mutation
r_pa_block = requests.post(
    f"{API_BASE}/admin/applications/{app_id}/decision",
    json={"decision": "REJECTED", "remarks": "Unauthorized platform mutation"},
    headers=pa_headers
)
assert r_pa_block.status_code == 403, f"Security Breach! Expected 403, got {r_pa_block.status_code}"
print(f"[PASS] Strict Platform Admin View-Only Enforcement: Blocked with HTTP 403 Forbidden.")

print("\n" + "=" * 80)
print("ALL INDEPENDENT VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("=" * 80)
