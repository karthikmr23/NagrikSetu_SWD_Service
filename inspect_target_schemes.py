import requests

BASE = "http://localhost:8005/api/swd"

def find_schemes():
    # Fetch all published schemes currently
    r = requests.get(f"{BASE}/schemes?limit=100")
    schemes = r.json()
    print(f"Total currently visible schemes: {len(schemes)}")
    
    target_names = [
        "Post-Matric Scholarship for SC/ST and Backward Classes Students",
        "Disability Maintenance & Assistive Aid Grant",
        "Farmer Irrigation Assistance Scheme (Micro-Irrigation)",
        "ELEVATE & ELEVATE NxT Startup Grants",
        "Rajiv Gandhi Entrepreneurship Program",
        "Ambedkar Karmika Sahaya Hastha",
        "Shakti",
        "Yuva Nidhi"
    ]
    
    print("\n--- TARGET SCHEMES MATCHING ---")
    for t in target_names:
        matches = [s for s in schemes if t.lower() in s.get("name", "").lower() or t.lower() in s.get("scheme_code", "").lower()]
        print(f"Query '{t}': {len(matches)} match(es)")
        for m in matches:
            print(f"   -> ID: {m.get('id')} | Code: {m.get('scheme_code')} | Name: {m.get('name')} | Cat: {m.get('category_id')}")

if __name__ == "__main__":
    find_schemes()
