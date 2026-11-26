# Update backend_full_audit.py to test eligibility on an active visible scheme (Scheme 5 Gruha Lakshmi or Scheme 3 Sandhya Suraksha)
# and verify catalogue count is exactly 28 visible schemes

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend_full_audit.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Update T02 to expect 28 schemes
code = code.replace(
    'passed = (status == 200 and len(data) == 34)',
    'passed = (status == 200 and len(data) == 28)'
)

# In T04, evaluate eligibility on an active scheme (Scheme 3 or Scheme 5)
code = code.replace(
    'status, data = post_json("/api/swd/schemes/1/eligibility-check"',
    'status, data = post_json("/api/swd/schemes/5/eligibility-check"'
)
code = code.replace(
    '"annual_income": 150000,\n            "caste_category": "SC",\n            "residence_state": "Karnataka",\n            "age": 20,\n            "education_level": "Undergraduate"',
    '"annual_income": 150000,\n            "caste_category": "SC",\n            "residence_state": "Karnataka",\n            "age": 30,\n            "gender": "female",\n            "is_woman": True'
)
code = code.replace(
    'T04 Eligibility Rule Engine (Scheme 1)',
    'T04 Eligibility Rule Engine (Scheme 5)'
)

# In T05, expect 28 matched schemes
code = code.replace(
    'passed = (status == 200 and status2 == 200 and len(results_list) > 0)',
    'passed = (status == 200 and status2 == 200 and len(results_list) == 28)'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated backend_full_audit.py successfully")
