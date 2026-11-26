import requests

BASE = "http://localhost:8005/api/swd"
login_payload = {"email": "welfareadmin@example.com", "password": "Welfare@123"}
r_auth = requests.post(f"{BASE}/auth/login", json=login_payload)
token = r_auth.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

r_apps = requests.get(f"{BASE}/applications", headers=headers)
print("Applications status code:", r_apps.status_code)
if r_apps.status_code == 200:
    apps = r_apps.json()
    print("Total apps:", len(apps))
    shakti_apps = [a for a in apps if a.get("scheme_id") == 7 or "shakti" in str(a).lower()]
    print("Shakti apps count:", len(shakti_apps))
    for a in shakti_apps:
        print("  App:", a.get("id"), a.get("application_number"), a.get("scheme_name"), a.get("status"))
else:
    print("Apps response:", r_apps.text[:300])
