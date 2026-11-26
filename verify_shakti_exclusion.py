import requests

BASE = "http://localhost:8005/api/swd"

def verify():
    print("=== VERIFYING SHAKTI EXCLUSION ===")
    
    # 1. Scheme Catalogue
    r = requests.get(f"{BASE}/schemes")
    schemes = r.json()
    print(f"1. Total schemes returned in public catalogue: {len(schemes)}")
    shakti_in_cat = [s for s in schemes if "shakti" in s.get("name", "").lower() or "shakti" in s.get("scheme_code", "").lower()]
    print(f"   Shakti in catalogue: {shakti_in_cat} -> {'PASS (Excluded)' if len(shakti_in_cat) == 0 else 'FAIL'}")

    # 2. Scheme Search Results
    r_search = requests.get(f"{BASE}/schemes?search=shakti")
    search_res = r_search.json()
    print(f"2. Search results for 'shakti': {len(search_res)} -> {'PASS (Excluded)' if len(search_res) == 0 else 'FAIL'}")

    # 3. Category Filter (Category 5: Flagship Guarantees)
    r_cat = requests.get(f"{BASE}/schemes?category_id=5")
    cat_schemes = r_cat.json()
    print(f"3. Schemes in Category 5 (Flagship Guarantees): {len(cat_schemes)}")
    for s in cat_schemes:
        print(f"   - {s.get('scheme_code')}: {s.get('name')}")
    shakti_in_cat5 = [s for s in cat_schemes if "shakti" in s.get("name", "").lower()]
    print(f"   Shakti in Category 5: {'NONE (PASS)' if len(shakti_in_cat5) == 0 else 'FAIL'}")

    # 4. Smart Finder Match
    r_finder = requests.post(f"{BASE}/finder/match", json={
        "gender": "female",
        "is_woman": True,
        "residence_district": "Bengaluru Urban",
        "age": 25,
        "annual_income": 100000
    })
    finder_matches = r_finder.json().get("results", [])
    shakti_finder = [m for m in finder_matches if "shakti" in m.get("scheme_name", "").lower() or "shakti" in m.get("scheme_code", "").lower()]
    print(f"4. Smart Finder matches for women profile: {len(finder_matches)} total schemes, Shakti found: {len(shakti_finder)} -> {'PASS (Excluded)' if len(shakti_finder) == 0 else 'FAIL'}")

    # 5. Recommendations Match
    r_rec = requests.post(f"{BASE}/recommendations/match", json={
        "citizen_attributes": {
            "gender": "female",
            "is_woman": True,
            "residence_state": "Karnataka",
            "annual_income": 100000
        }
    })
    rec_matches = r_rec.json()
    shakti_rec = [m for m in rec_matches if "shakti" in m.get("scheme_name", "").lower() or "shakti" in m.get("scheme_code", "").lower()]
    print(f"5. Recommendations matches for women profile: {len(rec_matches)} total, Shakti found: {len(shakti_rec)} -> {'PASS (Excluded)' if len(shakti_rec) == 0 else 'FAIL'}")

    # 6. Direct Dynamic Form Retrieval for Scheme 7
    r_form = requests.get(f"{BASE}/schemes/7/form")
    print(f"6. Dynamic form for Scheme 7 (Shakti): Status {r_form.status_code}, Form={r_form.json()} -> {'PASS (Excluded/None)' if r_form.json() is None else 'FAIL'}")

    # 7. Application Submission Attempt for Scheme 7
    # Login citizen
    r_auth = requests.post(f"{BASE}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
    cit_token = r_auth.json().get("access_token")
    headers = {"Authorization": f"Bearer {cit_token}"}
    r_apply = requests.post(f"{BASE}/schemes/7/applications", json={
        "citizen_id": "CIT-KA-9901",
        "citizen_name": "Ramesh Kumar Nayak",
        "citizen_phone": "9876543210",
        "residence_district": "Bengaluru Urban",
        "annual_income": 120000,
        "caste_category": "SC",
        "form_data": {}
    }, headers=headers)
    print(f"7. Attempted application for Scheme 7: Status {r_apply.status_code}, Response={r_apply.json().get('detail')} -> {'PASS (Blocked)' if r_apply.status_code in [400, 403, 404] else 'FAIL'}")

    # 8. Admin Dashboard Scheme Count
    r_adm_auth = requests.post(f"{BASE}/auth/login", json={"email": "welfareadmin@example.com", "password": "Welfare@123"})
    adm_token = r_adm_auth.json().get("access_token")
    adm_headers = {"Authorization": f"Bearer {adm_token}"}
    r_dash = requests.get(f"{BASE}/admin/dashboard", headers=adm_headers)
    dash = r_dash.json()
    print(f"8. Admin Dashboard SWD Schemes count: {dash.get('published_schemes')} published, {dash.get('total_schemes')} total -> {'PASS (34 Schemes)' if dash.get('published_schemes') == 34 else 'FAIL'}")

    # 9. Verify other valid schemes remain functional (e.g. Gruha Lakshmi Scheme ID 5)
    r_gl_form = requests.get(f"{BASE}/schemes/5/form")
    print(f"9. Gruha Lakshmi (Scheme 5) dynamic form: Status {r_gl_form.status_code}, Fields count: {len(r_gl_form.json().get('fields', []))} -> {'PASS' if r_gl_form.status_code == 200 else 'FAIL'}")

if __name__ == "__main__":
    verify()
