import urllib.request
import json

BASE_URL = "http://localhost:8005"

# Welfare admin login
data = json.dumps({"email": "welfareadmin@example.com", "password": "Welfare@123"}).encode("utf-8")
req = urllib.request.Request(f"{BASE_URL}/api/swd/auth/login", data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    token = res["access_token"]

# Admin applications
req = urllib.request.Request(f"{BASE_URL}/api/swd/admin/applications", headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    apps = json.loads(resp.read().decode("utf-8"))

print(f"Total admin applications: {len(apps)}")
shakti_apps = [a for a in apps if a.get("scheme_id") == 7 or "shakti" in str(a).lower()]
print(f"Shakti applications found: {len(shakti_apps)}")
for a in shakti_apps:
    print(f"  App ID={a.get('id')}, AppNum={a.get('application_number')}, SchemeID={a.get('scheme_id')}, Status={a.get('status')}")

# Also check admin dashboard counts
req = urllib.request.Request(f"{BASE_URL}/api/swd/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    dash = json.loads(resp.read().decode("utf-8"))
print("Dashboard overview:", dash)
