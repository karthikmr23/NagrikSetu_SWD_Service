import requests
BASE = "http://localhost:8005/api/swd"
schemes = requests.get(f"{BASE}/schemes").json()
print("Total schemes:", len(schemes))
forms_found = 0
for s in schemes:
    r = requests.get(f"{BASE}/schemes/{s['id']}/form")
    if r.status_code == 200 and r.json() is not None:
        forms_found += 1
    else:
        print("No form for scheme id:", s["id"], s["name"])
print("Forms found:", forms_found)
