import re

target_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\master_e2e_verification.py"

with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Citizen registration
code = code.replace(
    'email = f"test.citizen.{rand_suffix}@nagriksetu.test"',
    'email = f"citizen_{rand_suffix.lower()}@example.com"'
)
code = re.sub(
    r'"phone":\s*f"988\{os\.urandom\(3\)\.hex\(\)\[:7\]\}",',
    '"phone": f"9845{str(hash(rand_suffix) % 1000000).zfill(6)}",',
    code
)

# 2. Scheme discovery and eligibility
code = code.replace(
    'r_elig = requests.post(f"{BASE_URL}/eligibility/evaluate", json={\n        "scheme_id": 1,\n        "applicant_profile": {',
    'r_elig = requests.post(f"{BASE_URL}/schemes/1/eligibility-check", json={\n        "citizen_attributes": {'
)
code = code.replace(
    'if res.get("is_eligible") is True:',
    'if res.get("preliminary_status") in ["LIKELY_ELIGIBLE", "ELIGIBLE"] or res.get("is_eligible") is True:'
)
code = code.replace(
    "res.get('is_eligible')}",
    "res.get('preliminary_status', True)}"
)

# 3. Dynamic form and application submit
old_submit = '''    # Submit application
    r_sub = requests.post(f"{BASE_URL}/applications", json={
        "scheme_id": 1,
        "citizen_id": citizen_auth["citizen_id"],
        "full_name": citizen_auth["name"],
        "phone": "9845012345",
        "district": "Bengaluru Urban",
        "bank_account_number": "SBIN0040123991",
        "bank_ifsc": "SBIN0040123",
        "caste_category": "SC",
        "consent_declaration": True,
        "dynamic_form_data": {
            "college_name": "Bangalore University Institute of Technology",
            "student_registration_number": "BU-ENG-2026-9901",
            "current_year_of_study": "3rd Year",
            "annual_tuition_fee": 18500
        }
    }, headers=headers)'''

new_submit = '''    # Submit application
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
    }, headers=headers)'''

code = code.replace(old_submit, new_submit)

# 4. Citizen dashboard stats grievances lookup
code = code.replace(
    'r_grvs = requests.get(f"{BASE_URL}/grievances/{citizen_auth[\'citizen_id\']}", headers=headers)',
    'r_grvs = requests.get(f"{BASE_URL}/grievances?citizen_id={citizen_auth[\'citizen_id\']}", headers=headers)'
)

# 5. Platform admin monitoring stats
code = code.replace(
    'r_stats = requests.get(f"{BASE_URL}/admin/dashboard-stats", headers=headers)',
    'r_stats = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)'
)
code = code.replace(
    'r_cats = requests.get(f"{BASE_URL}/admin/category-application-stats", headers=headers)',
    'r_cats = requests.get(f"{BASE_URL}/admin/categories/stats", headers=headers)'
)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Harness script updated successfully!")
