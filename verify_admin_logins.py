import requests

BASE_URL = "http://localhost:8005/api/v1/swd"

def test_login(identifier, password, label):
    print(f"\nTesting Login for [{label}] using identifier: '{identifier}'")
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": identifier, "password": password})
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"SUCCESS -> Role: {data.get('role')}, Citizen/Username ID: {data.get('citizen_id')}, Email: {data.get('email')}, Name: {data.get('name')}")
        token = data.get("access_token")
        
        # Test protected endpoint with token
        headers = {"Authorization": f"Bearer {token}"}
        me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Auth /me Status: {me_res.status_code} -> Authenticated Profile Role: {me_res.json().get('role')}")
        
        if data.get("role") == "PLATFORM_ADMIN":
            audit_res = requests.get(f"{BASE_URL}/admin/audit-logs", headers=headers)
            print(f"Platform Admin Audit Logs Access: {audit_res.status_code}")
        elif data.get("role") == "GOVERNMENT_WELFARE_ADMIN":
            apps_res = requests.get(f"{BASE_URL}/admin/applications", headers=headers)
            print(f"Gov Welfare Admin Applications Access: {apps_res.status_code}")
        return True
    else:
        print(f"FAILED -> {res.text}")
        return False

# 1. Platform Admin via Username
test_login("platformadmin", "Platform@123", "Platform Admin via Username")

# 2. Platform Admin via Email
test_login("platformadmin@example.com", "Platform@123", "Platform Admin via Email")

# 3. Government Welfare Admin via Username
test_login("welfareadmin", "Welfare@123", "Government Welfare Admin via Username")

# 4. Government Welfare Admin via Email
test_login("welfareadmin@example.com", "Welfare@123", "Government Welfare Admin via Email")

# 5. Invalid Password Check
print("\nTesting Invalid Password Check for 'platformadmin':")
invalid_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "platformadmin", "password": "WrongPassword!"})
print(f"Status Code (Expected 401): {invalid_res.status_code}")
