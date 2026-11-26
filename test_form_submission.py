import requests
import json
import pymysql

BASE_URL = "http://localhost:8005/api/v1/swd"

# 1. Citizen Login
login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
print("Citizen Login Status:", login_res.status_code)
login_data = login_res.json()
token = login_data.get("access_token")
citizen_id = login_data.get("citizen_id")
print("Citizen ID:", citizen_id, "User Role:", login_data.get("role"))

headers = {"Authorization": f"Bearer {token}"}

# 2. Test Submission for Scheme 1 (Post-Matric Scholarship)
scheme_1_payload = {
    "citizen_id": citizen_id,
    "citizen_name": "Ramesh Kumar Nayak",
    "citizen_phone": "9876543210",
    "annual_income": 120000,
    "caste_category": "SC",
    "residence_district": "Bengaluru Urban",
    "disability_percentage": 0,
    "bank_account_number": "912345678901",
    "bank_ifsc": "SBIN0001234",
    "application_data_json": {
        "student_admission_number": "ADM-2026-ENG-442",
        "institution_name": "Bangalore Institute of Technology",
        "course_name": "Bachelor of Engineering (B.E.)",
        "current_academic_year": "2nd Year",
        "previous_year_marks_percentage": 78.5,
        "hostel_stay_type": "Government Post-Matric Hostel",
        "ssp_student_id": "SSP-KAR-2026-88124",
        "declaration_non_receipt": True
    }
}

app_res1 = requests.post(f"{BASE_URL}/schemes/1/applications", json=scheme_1_payload, headers=headers)
print("\nScheme 1 Submission Status:", app_res1.status_code)
app_data1 = app_res1.json()
app_id_1 = app_data1.get("id")
app_num_1 = app_data1.get("application_number")
print("App 1 ID:", app_id_1, "Number:", app_num_1, "Category ID:", app_data1.get("category_id"))

# 3. Test Submission for Scheme 18 (Ganga Kalyana Scheme)
scheme_18_payload = {
    "citizen_id": citizen_id,
    "citizen_name": "Ramesh Kumar Nayak",
    "citizen_phone": "9876543210",
    "annual_income": 80000,
    "caste_category": "SC",
    "residence_district": "Tumakuru",
    "disability_percentage": 0,
    "bank_account_number": "912345678902",
    "bank_ifsc": "CNRB0002345",
    "application_data_json": {
        "fruits_farmer_fid": "FID-TUM-99882",
        "land_holding_acres": 2.5,
        "land_survey_numbers": "142/2A, 142/2B",
        "village_name": "Kunigal Grama Panchayat",
        "water_source_assessment": "Borewell Feasible (Certified Geologist)",
        "escom_subdivision": "BESCOM Kunigal Sub-Division"
    }
}

app_res18 = requests.post(f"{BASE_URL}/schemes/18/applications", json=scheme_18_payload, headers=headers)
print("\nScheme 18 Submission Status:", app_res18.status_code)
app_data18 = app_res18.json()
app_id_18 = app_data18.get("id")
app_num_18 = app_data18.get("application_number")
print("App 18 ID:", app_id_18, "Number:", app_num_18, "Category ID:", app_data18.get("category_id"))

# 4. Verify in MySQL Database
conn = pymysql.connect(host="127.0.0.1", user="swd_app", password="swd-secure-pass-2026", database="nagriksetu_swd", port=3306)
c = conn.cursor(pymysql.cursors.DictCursor)
c.execute("""
    SELECT id, application_number, scheme_id, category_id, status, citizen_id, application_data_json 
    FROM scheme_applications 
    WHERE id IN (%s, %s)
""", (app_id_1, app_id_18))
print("\nDatabase Application Records in MySQL (Port 3306):")
for r in c.fetchall():
    print(f"ID: {r['id']}, Num: {r['application_number']}, Scheme: {r['scheme_id']}, Cat: {r['category_id']}, Status: {r['status']}")
    print(f"   Data JSON: {r['application_data_json']}")

# 5. Verify PDF Receipt Endpoint
pdf_res = requests.get(f"{BASE_URL}/applications/{app_id_1}/receipt", headers=headers)
print(f"\nPDF Receipt Download Status for {app_num_1}:", pdf_res.status_code, "Content-Type:", pdf_res.headers.get("content-type"), "Length:", len(pdf_res.content), "bytes")

# 6. Verify Gov Welfare Admin queue reflects submitted applications
admin_login = requests.post(f"{BASE_URL}/auth/login", json={"email": "officer@nagriksetu.local", "password": "OfficerPass@2026"})
admin_token = admin_login.json().get("access_token")
admin_headers = {"Authorization": f"Bearer {admin_token}"}
admin_apps_res = requests.get(f"{BASE_URL}/admin/applications", headers=admin_headers)
print("\nGov Welfare Admin Applications Status:", admin_apps_res.status_code, "Total In Queue:", len(admin_apps_res.json()) if admin_apps_res.status_code == 200 else "N/A")

conn.close()
