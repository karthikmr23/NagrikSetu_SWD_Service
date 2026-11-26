import urllib.request, json

mahesh_profile = {
    'age': 28,
    'district': 'Bengaluru Urban',
    'taluk': 'Bengaluru South',
    'gender': 'Male',
    'caste_category': 'General',
    'annual_income': 180000,
    'occupation': 'Student',
    'education_level': 'Professional / Engineering / Medical',
    'disability_status': 'No',
    'disability_percentage': 0,
    'marital_status': 'Unmarried',
    'is_student': True,
    'is_farmer': False,
    'is_woman': False
}

req = urllib.request.Request('http://localhost:8005/api/swd/finder/match', data=json.dumps(mahesh_profile).encode(), headers={'Content-Type': 'application/json'})
resp = json.loads(urllib.request.urlopen(req).read().decode())

print("Total schemes matched:", resp.get("total_matches"))
print("Potential Matches:", resp.get("potential_match_count"))
print("Check Requirements:", resp.get("check_requirements_count"))

target_schemes = [
    'Bhagyalakshmi Scheme',
    'Financial Incentive Scheme for Inter-Caste Marriages',
    'Anna Bhagya Scheme',
    'Gruha Jyothi Scheme',
    'Yeshasvini Cooperative Health Insurance Scheme',
    'Gruha Lakshmi Scheme',
    'Udyogini Scheme',
    'Chief Minister Raitha Vidya Nidhi',
    'Arivu Education Loan Scheme',
    'Vidyasiri (Food & Accommodation Stipend)'
]

print("\n=== RESULTS FOR KEY SCHEMES FOR MAHESH ===")
for item in resp.get("results", []):
    for ts in target_schemes:
        if ts.lower() in item.get("scheme_name", "").lower():
            print(f"Scheme: {item.get('scheme_name')} ({item.get('scheme_code')})")
            print(f"  Match Status: {item.get('match_status')} | Score: {item.get('match_score')}")
            print(f"  Why Matched: {item.get('why_matched')}")
            print(f"  Missing Requirements: {item.get('missing_requirements')}")
            print()
