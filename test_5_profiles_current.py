import urllib.request, json

def test_profile(title, profile):
    req = urllib.request.Request('http://localhost:8005/api/swd/finder/match', data=json.dumps(profile).encode(), headers={'Content-Type': 'application/json'})
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"=== {title} ===")
    print(f"Potential Matches: {resp.get('potential_match_count')}, Check Requirements: {resp.get('check_requirements_count')}")
    pot_names = [r['scheme_name'] for r in resp.get('results', []) if r['match_status'] == 'Potential Match']
    chk_names = [r['scheme_name'] for r in resp.get('results', []) if r['match_status'] == 'Check Requirements']
    not_names = [r['scheme_name'] for r in resp.get('results', []) if r['match_status'] == 'Not Matched']
    print(f"Potential ({len(pot_names)}): {pot_names}")
    print(f"Check Requirements ({len(chk_names)}): {chk_names}")
    print(f"Not Matched ({len(not_names)}): {len(not_names)} schemes")
    print()

test_profile("1. Mahesh (Male, Gen, Student, 1.8L, 28, Unmarried)", {
    'age': 28, 'district': 'Bengaluru Urban', 'gender': 'Male', 'caste_category': 'General',
    'annual_income': 180000, 'occupation': 'Student', 'is_student': True, 'is_farmer': False, 'is_woman': False,
    'marital_status': 'Unmarried'
})
test_profile("2. Female Applicant (Female, OBC, Unemployed, 1.2L, 25, Unmarried)", {
    'age': 25, 'district': 'Mysuru', 'gender': 'Female', 'caste_category': 'OBC',
    'annual_income': 120000, 'occupation': 'Unemployed', 'is_student': False, 'is_farmer': False, 'is_woman': True,
    'marital_status': 'Unmarried'
})
test_profile("3. SC Student (Male, SC, Student, 1.5L, 21, Unmarried)", {
    'age': 21, 'district': 'Dharwad', 'gender': 'Male', 'caste_category': 'SC',
    'annual_income': 150000, 'occupation': 'Student', 'is_student': True, 'is_farmer': False, 'is_woman': False,
    'marital_status': 'Unmarried'
})
test_profile("4. Farmer Applicant (Male, Gen, Farmer, 90K, 42, Married)", {
    'age': 42, 'district': 'Mandya', 'gender': 'Male', 'caste_category': 'General',
    'annual_income': 90000, 'occupation': 'Farmer', 'is_student': False, 'is_farmer': True, 'is_woman': False,
    'marital_status': 'Married'
})
test_profile("5. Senior Citizen (Male, OBC, Other, 25K, 68, Married)", {
    'age': 68, 'district': 'Tumakuru', 'gender': 'Male', 'caste_category': 'OBC',
    'annual_income': 25000, 'occupation': 'Other', 'is_student': False, 'is_farmer': False, 'is_woman': False,
    'marital_status': 'Married'
})
