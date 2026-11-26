import requests
import json
import pymysql
import os

BASE_URL = "http://localhost:8005/api/v1/swd"
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "swd_app",
    "password": "swd-secure-pass-2026",
    "database": "nagriksetu_swd",
    "port": 3306
}

def run_end_to_end_verification():
    print("=" * 80)
    print("NAGRIKSETU SWD — COMPREHENSIVE END-TO-END WORKFLOW VERIFICATION")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 1. CITIZEN AUTHENTICATION & PROFILE
    # --------------------------------------------------------------------------
    print("\n[STEP 1] Citizen Authentication...")
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
    assert login_res.status_code == 200, f"Citizen login failed: {login_res.text}"
    citizen_token = login_res.json()["access_token"]
    citizen_id = login_res.json()["citizen_id"]
    citizen_headers = {"Authorization": f"Bearer {citizen_token}"}
    print(f"  -> Citizen Authenticated: ID={citizen_id}, Role={login_res.json()['role']}")

    # --------------------------------------------------------------------------
    # 2. EXPLORE SCHEMES & PRELIMINARY ELIGIBILITY CHECK
    # --------------------------------------------------------------------------
    print("\n[STEP 2] Explore Schemes & Preliminary Eligibility Assessment...")
    schemes_res = requests.get(f"{BASE_URL}/schemes")
    assert schemes_res.status_code == 200, "Failed to load schemes catalogue"
    schemes = schemes_res.json()
    print(f"  -> Total Active Schemes Retrieved: {len(schemes)}")

    # Check eligibility for Scheme 1 (Post-Matric Scholarship)
    elig_payload = {
        "citizen_attributes": {
            "caste_category": "SC",
            "annual_income": 150000,
            "state": "Karnataka",
            "student_status": "ENROLLED_POSTMATRIC"
        }
    }
    elig_res = requests.post(f"{BASE_URL}/schemes/1/eligibility-check", json=elig_payload)
    assert elig_res.status_code == 200, f"Eligibility check failed: {elig_res.text}"
    elig_data = elig_res.json()
    print(f"  -> Scheme 1 Preliminary Status: {elig_data.get('status')} | Reason: {elig_data.get('reason')}")
    print(f"  -> Disclaimer Present: {bool(elig_data.get('disclaimer'))}")

    # --------------------------------------------------------------------------
    # 3. APPLY FOR SCHEME (CREATE APPLICATION IN MYSQL)
    # --------------------------------------------------------------------------
    print("\n[STEP 3] Submit Application Dossier with Dynamic Form Responses...")
    app_payload = {
        "citizen_id": citizen_id,
        "citizen_name": "Ramesh Kumar Nayak",
        "citizen_phone": "9876543210",
        "annual_income": 150000,
        "caste_category": "SC",
        "residence_district": "Bengaluru Urban",
        "disability_percentage": 0,
        "bank_account_number": "912345678901",
        "bank_ifsc": "SBIN0001234",
        "application_data_json": {
            "student_admission_number": "ADM-2026-ENG-901",
            "institution_name": "RV College of Engineering",
            "course_name": "Bachelor of Technology (B.Tech)",
            "current_academic_year": "3rd Year",
            "previous_year_marks_percentage": 82.4,
            "hostel_stay_type": "Government Post-Matric Hostel",
            "ssp_student_id": "SSP-KAR-2026-90123",
            "declaration_non_receipt": True
        }
    }
    app_res = requests.post(f"{BASE_URL}/schemes/1/applications", json=app_payload, headers=citizen_headers)
    assert app_res.status_code == 200, f"Application submission failed: {app_res.text}"
    app_data = app_res.json()
    app_id = app_data["id"]
    app_num = app_data["application_number"]
    print(f"  -> Application Registered: ID={app_id}, AppNum={app_num}, Status={app_data['status']}, CategoryID={app_data['category_id']}")

    # --------------------------------------------------------------------------
    # 4. UPLOAD SUPPORTING DOCUMENT & VERIFY METADATA PERSISTENCE
    # --------------------------------------------------------------------------
    print("\n[STEP 4] Upload Supporting Document to Application...")
    test_doc_content = b"%PDF-1.4 Mock supporting income and caste verification document content for testing"
    files = {"file": ("caste_income_cert.pdf", test_doc_content, "application/pdf")}
    data = {"document_code": "INCOME_CERTIFICATE"}
    upload_res = requests.post(f"{BASE_URL}/applications/{app_id}/documents", data=data, files=files, headers=citizen_headers)
    assert upload_res.status_code == 200, f"Document upload failed: {upload_res.text}"
    doc_data = upload_res.json()
    print(f"  -> Document Stored: DocID={doc_data['id']}, DocCode={doc_data['document_code']}, FilePath={doc_data['file_path']}")

    # --------------------------------------------------------------------------
    # 5. VERIFY CITIZEN APPLICATION TRACKING & DOWNLOAD RECEIPT
    # --------------------------------------------------------------------------
    print("\n[STEP 5] Citizen Tracking & PDF Receipt Download...")
    cit_apps_res = requests.get(f"{BASE_URL}/applications/{citizen_id}", headers=citizen_headers)
    assert cit_apps_res.status_code == 200, "Citizen applications fetch failed"
    matching_apps = [a for a in cit_apps_res.json() if a["id"] == app_id]
    assert len(matching_apps) > 0, "Submitted application not listed in citizen tracking"
    print(f"  -> Application found in Citizen tracking list: Status={matching_apps[0]['status']}")

    pdf_res = requests.get(f"{BASE_URL}/applications/{app_id}/receipt", headers=citizen_headers)
    assert pdf_res.status_code == 200, f"PDF receipt fetch failed: {pdf_res.status_code}"
    assert pdf_res.headers.get("content-type") == "application/pdf", "Expected application/pdf content type"
    print(f"  -> PDF Acknowledgement Receipt Generated: Length={len(pdf_res.content)} bytes")

    # --------------------------------------------------------------------------
    # 6. GOVERNMENT WELFARE ADMIN: SCRUTINIZE, REQUEST INFO & APPROVE
    # --------------------------------------------------------------------------
    print("\n[STEP 6] Government Welfare Admin Review & Scrutiny Workflow...")
    welfare_login = requests.post(f"{BASE_URL}/auth/login", json={"email": "welfareadmin", "password": "Welfare@123"})
    assert welfare_login.status_code == 200, f"Welfare Admin login failed: {welfare_login.text}"
    welfare_token = welfare_login.json()["access_token"]
    welfare_headers = {"Authorization": f"Bearer {welfare_token}"}
    print(f"  -> Government Welfare Admin Authenticated: Role={welfare_login.json()['role']}")

    # Check category-wise scrutiny list
    admin_apps_res = requests.get(f"{BASE_URL}/admin/applications?category_id=1", headers=welfare_headers)
    assert admin_apps_res.status_code == 200, "Failed to load admin applications queue"
    admin_apps = admin_apps_res.json()
    assert any(a["id"] == app_id for a in admin_apps), "Target application not found in Welfare Admin scrutiny queue"
    print(f"  -> Target application present in category 1 scrutiny queue (Total queue items: {len(admin_apps)})")

    # Action 6A: Request Supplementary Information
    req_info_payload = {"remarks": "Please provide verified Tahsildar caste validity certificate copy."}
    req_res = requests.post(f"{BASE_URL}/admin/applications/{app_id}/request-information", json=req_info_payload, headers=welfare_headers)
    assert req_res.status_code == 200, f"Request info failed: {req_res.text}"
    assert req_res.json()["status"] == "DOCUMENTS_REQUIRED", "Status should be DOCUMENTS_REQUIRED"
    print(f"  -> Status updated to DOCUMENTS_REQUIRED: Remarks='{req_res.json()['admin_remarks']}'")

    # Action 6B: Approve Application & Create Beneficiary Record
    decision_payload = {
        "decision": "APPROVED",
        "remarks": "Income and enrollment verified against collegiate database. Approved for state scholarship.",
        "sanctioned_amount": 25000.0,
        "disbursement_mode": "DIRECT_BENEFIT_TRANSFER"
    }
    decision_res = requests.post(f"{BASE_URL}/admin/applications/{app_id}/decision", json=decision_payload, headers=welfare_headers)
    assert decision_res.status_code == 200, f"Decision submission failed: {decision_res.text}"
    assert decision_res.json()["status"] == "APPROVED", "Status should be APPROVED"
    print(f"  -> Status updated to APPROVED: Sanctioned Amount=25000.0")

    # --------------------------------------------------------------------------
    # 7. PLATFORM ADMIN MONITORING DASHBOARD (VIEW-ONLY ENFORCEMENT)
    # --------------------------------------------------------------------------
    print("\n[STEP 7] Platform Admin Monitoring & Restriction Verification...")
    plat_login = requests.post(f"{BASE_URL}/auth/login", json={"email": "platformadmin", "password": "Platform@123"})
    assert plat_login.status_code == 200, f"Platform Admin login failed: {plat_login.text}"
    plat_token = plat_login.json()["access_token"]
    plat_headers = {"Authorization": f"Bearer {plat_token}"}
    print(f"  -> Platform Admin Authenticated: Role={plat_login.json()['role']}")

    # 7A: Platform Admin CAN monitor statistics
    stats_res = requests.get(f"{BASE_URL}/admin/dashboard", headers=plat_headers)
    assert stats_res.status_code == 200, f"Platform Admin dashboard fetch failed: {stats_res.text}"
    stats_data = stats_res.json()
    print(f"  -> Platform Admin Monitoring Stats:")
    print(f"     * Total Schemes: {stats_data['total_schemes']}")
    print(f"     * Total Applications: {stats_data['total_applications']}")
    print(f"     * Approved Applications: {stats_data['approved_applications']}")
    print(f"     * Total Beneficiaries: {stats_data['total_beneficiaries']}")

    # 7B: Platform Admin CANNOT approve or reject applications (Strict Backend 403 Enforcement)
    plat_decision_res = requests.post(f"{BASE_URL}/admin/applications/{app_id}/decision", json=decision_payload, headers=plat_headers)
    assert plat_decision_res.status_code == 403, f"Expected 403 Forbidden for Platform Admin on application decision endpoint, got {plat_decision_res.status_code}"
    print(f"  -> Strict Backend Enforcement PASS: Platform Admin attempt to modify application decision rejected with 403 Forbidden!")

    # --------------------------------------------------------------------------
    # 8. DIRECT MYSQL DATABASE PERSISTENCE VERIFICATION
    # --------------------------------------------------------------------------
    print("\n[STEP 8] Direct MySQL Database Verification (Port 3306)...")
    conn = pymysql.connect(**DB_CONFIG)
    c = conn.cursor(pymysql.cursors.DictCursor)

    # Verify application record
    c.execute("SELECT * FROM scheme_applications WHERE id = %s", (app_id,))
    app_row = c.fetchone()
    assert app_row is not None, "Application row missing in MySQL"
    assert app_row["status"] == "APPROVED", f"Expected status APPROVED in MySQL, got {app_row['status']}"
    assert app_row["category_id"] == 1, f"Expected category_id 1 in MySQL, got {app_row['category_id']}"
    print(f"  -> MySQL scheme_applications record verified: ID={app_row['id']}, Num={app_row['application_number']}, Status={app_row['status']}")

    # Verify application history
    c.execute("SELECT * FROM application_history WHERE application_id = %s ORDER BY id", (app_id,))
    hist_rows = c.fetchall()
    assert len(hist_rows) >= 2, f"Expected at least 2 history entries, got {len(hist_rows)}"
    print(f"  -> MySQL application_history records verified: {len(hist_rows)} transition entries:")
    for h in hist_rows:
        print(f"     * From '{h['from_status']}' -> '{h['to_status']}' by '{h['changed_by']}': {h['remarks']}")

    # Verify beneficiary record created
    c.execute("SELECT * FROM beneficiaries WHERE application_id = %s", (app_id,))
    ben_row = c.fetchone()
    assert ben_row is not None, "Beneficiary record was not created upon approval"
    assert float(ben_row["sanctioned_amount"]) == 25000.0, f"Expected 25000.0, got {ben_row['sanctioned_amount']}"
    print(f"  -> MySQL beneficiaries record verified: Code={ben_row['beneficiary_code']}, Name={ben_row['citizen_name']}, Amount={ben_row['sanctioned_amount']}, Status={ben_row['status']}")

    # Verify document record in MySQL
    c.execute("SELECT * FROM application_documents WHERE application_id = %s", (app_id,))
    doc_row = c.fetchone()
    assert doc_row is not None, "Document record missing in MySQL"
    print(f"  -> MySQL application_documents record verified: ID={doc_row['id']}, File={doc_row['file_name']}, Path={doc_row['file_path']}")

    # Verify citizen notification record in MySQL
    c.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY id DESC LIMIT 2", (citizen_id,))
    notifs = c.fetchall()
    assert len(notifs) > 0, "No notifications found for citizen"
    print(f"  -> MySQL notifications verified: Latest Notification = '{notifs[0]['title']}'")

    # Verify outbox event record in MySQL
    c.execute("SELECT * FROM outbox_events WHERE correlation_id = %s ORDER BY id DESC LIMIT 1", (app_num,))
    outbox = c.fetchone()
    assert outbox is not None, "Outbox event not generated"
    print(f"  -> MySQL outbox_events verified: EventType={outbox['event_type']}, Status={outbox['status']}")

    conn.close()

    print("\n" + "=" * 80)
    print("ALL 8 END-TO-END WORKFLOW TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_end_to_end_verification()
