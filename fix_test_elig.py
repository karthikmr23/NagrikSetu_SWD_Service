with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\test_multi_role_rbac.py", "r", encoding="utf-8") as f:
    text = f.read()

old_elig = """    # Citizen can check preliminary eligibility
    r_elig = requests.post(f"{API_BASE}/eligibility/check", json={
        "scheme_id": 1,
        "applicant_profile": {
            "annual_income": 180000,
            "caste_category": "SC",
            "residence_state": "Karnataka",
            "education_level": "Undergraduate",
            "age": 21
        }
    })"""

new_elig = """    # Citizen can check preliminary eligibility
    r_elig = requests.post(f"{API_BASE}/schemes/1/eligibility-check", json={
        "annual_income": 180000,
        "caste_category": "SC",
        "residence_state": "Karnataka",
        "education_level": "Undergraduate",
        "age": 21,
        "disability_percentage": 0
    })"""

if old_elig in text:
    text = text.replace(old_elig, new_elig)
    with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\test_multi_role_rbac.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed eligibility check in test_multi_role_rbac.py")
else:
    print("old_elig not found")
