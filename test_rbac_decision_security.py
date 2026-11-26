import urllib.request
import json

BASE_URL = "http://localhost:8005"

def test_rbac():
    print("=== RBAC SECURITY & ROLE-BASED ACCESS VERIFICATION ===")

    # 1. Unauthenticated Request
    req = urllib.request.Request(
        f"{BASE_URL}/api/swd/applications/22/decision",
        data=json.dumps({"decision": "APPROVED", "remarks": "Unauthorized test"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
        print("1. Unauthenticated decision attempt: FAIL (Allowed)")
    except urllib.error.HTTPError as e:
        print(f"1. Unauthenticated decision attempt: PASS (HTTP {e.code} Expected 401)")

    # 2. Citizen Login & Self-Decision Attempt
    login_data = json.dumps({"email": "citizen@example.com", "password": "CitizenPass@2026"}).encode("utf-8")
    req_login = urllib.request.Request(f"{BASE_URL}/api/swd/auth/login", data=login_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req_login) as resp:
        cit_token = json.loads(resp.read().decode("utf-8"))["access_token"]

    req_cit_dec = urllib.request.Request(
        f"{BASE_URL}/api/swd/applications/22/decision",
        data=json.dumps({"decision": "APPROVED", "remarks": "Citizen self-approval attempt"}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {cit_token}"}
    )
    try:
        urllib.request.urlopen(req_cit_dec)
        print("2. Citizen self-approval attempt: FAIL (Allowed)")
    except urllib.error.HTTPError as e:
        print(f"2. Citizen self-approval attempt: PASS (HTTP {e.code} Expected 403 Forbidden)")

    # 3. Platform Admin Login & Mutation Attempt
    login_plat = json.dumps({"email": "platformadmin@example.com", "password": "Platform@123"}).encode("utf-8")
    req_plat_login = urllib.request.Request(f"{BASE_URL}/api/swd/auth/login", data=login_plat, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req_plat_login) as resp:
        plat_token = json.loads(resp.read().decode("utf-8"))["access_token"]

    # Platform Admin can view queue but CANNOT create categories or modify scheme forms
    req_plat_cat = urllib.request.Request(
        f"{BASE_URL}/api/swd/categories",
        data=json.dumps({"code": "TEST_CAT", "name": "Test Cat"}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {plat_token}"}
    )
    try:
        urllib.request.urlopen(req_plat_cat)
        print("3. Platform Admin category mutation guard: FAIL (Allowed)")
    except urllib.error.HTTPError as e:
        print(f"3. Platform Admin category mutation guard: PASS (HTTP {e.code} Expected 403 Forbidden)")

    # 4. Welfare Admin Login & Permission Verification
    login_welf = json.dumps({"email": "welfareadmin@example.com", "password": "Welfare@123"}).encode("utf-8")
    req_welf_login = urllib.request.Request(f"{BASE_URL}/api/swd/auth/login", data=login_welf, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req_welf_login) as resp:
        welf_data = json.loads(resp.read().decode("utf-8"))
        welf_token = welf_data["access_token"]
        welf_user = welf_data["user"]
        print(f"4. Welfare Admin login: User='{welf_user['name']}', Role='{welf_user['role']}' -> PASS")

    # Verify Welfare Admin can view queues
    req_queue = urllib.request.Request(f"{BASE_URL}/api/swd/admin/applications", headers={"Authorization": f"Bearer {welf_token}"})
    with urllib.request.urlopen(req_queue) as resp:
        apps_data = json.loads(resp.read().decode("utf-8"))
        print(f"   Welfare Admin applications queue access: {len(apps_data)} records accessible -> PASS")

if __name__ == "__main__":
    test_rbac()
