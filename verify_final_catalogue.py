import requests

BASE = "http://localhost:8005/api/swd"

def verify():
    print("=== FINAL SCHEME CATALOGUE CORRECTION VERIFICATION ===")

    # 1. Total Visible Schemes in Public Catalogue
    r = requests.get(f"{BASE}/schemes?limit=100")
    schemes = r.json()
    visible_count = len(schemes)
    print(f"1. Actual number of visible schemes in public catalogue: {visible_count}")
    
    # 2. Check Shakti is completely excluded
    shakti = [s for s in schemes if "shakti" in s.get("name", "").lower() or "shakti" in s.get("scheme_code", "").lower()]
    print(f"2. Shakti Scheme in catalogue: {shakti} -> {'PASS (Excluded)' if len(shakti) == 0 else 'FAIL'}")

    # 3. Check the six temporarily hidden schemes are not visible
    hidden_names = [
        "Post-Matric Scholarship for SC/ST and Backward Classes Students",
        "Disability Maintenance & Assistive Aid Grant",
        "Farmer Irrigation Assistance Scheme (Micro-Irrigation)",
        "ELEVATE & ELEVATE NxT Startup Grants",
        "Rajiv Gandhi Entrepreneurship Program",
        "Ambedkar Karmika Sahaya Hastha"
    ]
    print("\n3. Verifying 6 temporarily hidden schemes are absent from public catalogue:")
    for h in hidden_names:
        matches = [s for s in schemes if h.lower() in s.get("name", "").lower()]
        print(f"   - '{h}': {len(matches)} visible -> {'PASS (Hidden)' if len(matches) == 0 else 'FAIL'}")

    # 4. Search Verification
    print("\n4. Search verification:")
    for query in ["shakti", "elevate", "rajiv gandhi", "micro-irrigation", "sahaya hastha"]:
        r_srch = requests.get(f"{BASE}/schemes?search={query}")
        srch_data = r_srch.json()
        print(f"   - Search '{query}': {len(srch_data)} results -> {'PASS (0 Results)' if len(srch_data) == 0 else 'FAIL'}")

    # 5. Yuva Nidhi Scheme Verification
    print("\n5. Yuva Nidhi check:")
    yuva_matches = [s for s in schemes if "yuva" in s.get("name", "").lower()]
    print(f"   - Yuva Nidhi entries count: {len(yuva_matches)}")
    for ym in yuva_matches:
        print(f"     ID: {ym.get('id')} | Name: '{ym.get('name')}' | Code: '{ym.get('scheme_code')}'")
    has_exact_one = len(yuva_matches) == 1 and yuva_matches[0].get("name") == "Yuva Nidhi Scheme"
    print(f"   - Status: {'PASS (Exactly one Yuva Nidhi Scheme)' if has_exact_one else 'FAIL'}")

    # 6. Apply Now Routes Verification
    print("\n6. Apply Now Route Verification:")
    # Scheme 1 (Hidden)
    r_form1 = requests.get(f"{BASE}/schemes/1/form")
    print(f"   - Form for Scheme 1 (Hidden): Form={r_form1.json()} -> {'PASS (None)' if r_form1.json() is None else 'FAIL'}")

    # Scheme 7 (Shakti)
    r_form7 = requests.get(f"{BASE}/schemes/7/form")
    print(f"   - Form for Scheme 7 (Shakti): Form={r_form7.json()} -> {'PASS (None)' if r_form7.json() is None else 'FAIL'}")

    # Scheme 5 (Gruha Lakshmi - Active Karnataka Scheme)
    r_form5 = requests.get(f"{BASE}/schemes/5/form")
    print(f"   - Form for Scheme 5 (Gruha Lakshmi): Fields={len(r_form5.json().get('fields', []))} -> {'PASS' if r_form5.status_code == 200 and r_form5.json() else 'FAIL'}")

    # 7. Check Karnataka Schemes Preserved
    print("\n7. Recognisable Karnataka Government Schemes Preserved:")
    karnataka_core = [
        "Gruha Lakshmi Scheme",
        "Gruha Jyothi Scheme",
        "Anna Bhagya Scheme",
        "Yuva Nidhi Scheme",
        "Arivu Minority Education Loan Scheme",
        "Vidyasiri Hostel & Higher Education Stipend Scheme",
        "Raitha Vidya Nidhi Scholarship",
        "Ganga Kalyana Scheme",
        "Karnataka Gig Workers Welfare & Social Security Scheme"
    ]
    for kn in karnataka_core:
        km = [s for s in schemes if kn.lower() in s.get("name", "").lower()]
        print(f"   - '{kn}': {len(km)} present -> {'PASS' if len(km) == 1 else 'FAIL'}")

    # 8. List all visible schemes
    print(f"\n8. Complete List of All {visible_count} Visible Schemes:")
    for idx, s in enumerate(schemes, 1):
        print(f"   {idx}. [ID {s['id']}] {s['scheme_code']}: {s['name']} (Cat: {s['category_id']})")

if __name__ == "__main__":
    verify()
