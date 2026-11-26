with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\test_multi_role_rbac.py", "r", encoding="utf-8") as f:
    text = f.read()

old_wo_apply = """    # Welfare Officer CANNOT submit application as citizen
    r_wo_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "OFF-SWD-501",
        "citizen_name": "Welfare Officer",
        "annual_income": 500000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=wo_headers)"""

new_wo_apply = """    # Welfare Officer CANNOT submit application as citizen
    r_wo_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "OFF-SWD-501",
        "citizen_name": "Welfare Officer",
        "citizen_phone": "9845012345",
        "annual_income": 500000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=wo_headers)"""

old_pa_apply = """    # Platform Admin CANNOT submit citizen applications
    r_pa_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "PLATFORM-ADMIN",
        "citizen_name": "Super Admin",
        "annual_income": 900000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=pa_headers)"""

new_pa_apply = """    # Platform Admin CANNOT submit citizen applications
    r_pa_apply = requests.post(f"{API_BASE}/schemes/1/applications", json={
        "citizen_id": "PLATFORM-ADMIN",
        "citizen_name": "Super Admin",
        "citizen_phone": "9845012345",
        "annual_income": 900000,
        "caste_category": "General",
        "residence_district": "Bengaluru Urban",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0040123"
    }, headers=pa_headers)"""

text = text.replace(old_wo_apply, new_wo_apply)
text = text.replace(old_pa_apply, new_pa_apply)

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\test_multi_role_rbac.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated phone number in test payload")
