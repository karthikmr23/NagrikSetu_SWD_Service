import requests

BASE_URL = "http://localhost:8005/api/swd"

def verify_account(identifier, password, label):
    print(f"\n==================================================")
    print(f"VERIFYING ACCOUNT: [{label}]")
    print(f"Identifier: {identifier}")
    print(f"==================================================")
    
    # 1. Authenticate via POST /auth/login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": identifier, "password": password})
    print(f"Login Status: {login_res.status_code}")
    if login_res.status_code != 200:
        print(f"Login Failed: {login_res.text}")
        return False
        
    data = login_res.json()
    token = data.get("access_token")
    role = data.get("role")
    email = data.get("email")
    name = data.get("name")
    citizen_id = data.get("citizen_id")
    
    print(f"Authenticated Role: {role}")
    print(f"Authenticated Name: {name}")
    print(f"Authenticated Email: {email}")
    print(f"Authenticated Citizen/User ID: {citizen_id}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Check /auth/me
    me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"/auth/me Status: {me_res.status_code} | User: {me_res.json().get('email')} | Role: {me_res.json().get('role')}")
    
    # 3. Role-based endpoint permission checks
    if role == "GOVERNMENT_WELFARE_ADMIN":
        # Can access applications scrutiny list
        apps = requests.get(f"{BASE_URL}/admin/applications", headers=headers)
        print(f"Permission: Access Applications Scrutiny (/admin/applications): {apps.status_code} ({'PERMITTED' if apps.status_code == 200 else 'DENIED'})")
        
        # Can access beneficiaries
        bens = requests.get(f"{BASE_URL}/admin/beneficiaries", headers=headers)
        print(f"Permission: Access Beneficiaries (/admin/beneficiaries): {bens.status_code} ({'PERMITTED' if bens.status_code == 200 else 'DENIED'})")
        
        # Can access dashboard stats
        dash = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
        print(f"Permission: Access Welfare Dashboard Stats (/admin/dashboard): {dash.status_code} ({'PERMITTED' if dash.status_code == 200 else 'DENIED'})")

        # Can access DBT simulation
        dbt = requests.get(f"{BASE_URL}/admin/dbt/transactions", headers=headers)
        print(f"Permission: Access DBT Transaction Stream (/admin/dbt/transactions): {dbt.status_code} ({'PERMITTED' if dbt.status_code == 200 else 'DENIED'})")

    elif role == "PLATFORM_ADMIN":
        # Can access system metrics
        dash = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
        print(f"Permission: System Metrics Monitoring (/admin/dashboard): {dash.status_code} ({'PERMITTED' if dash.status_code == 200 else 'DENIED'})")
        
        # Can access user registry
        users = requests.get(f"{BASE_URL}/admin/users", headers=headers)
        print(f"Permission: Platform User Monitoring (/admin/users): {users.status_code} ({'PERMITTED' if users.status_code == 200 else 'DENIED'})")
        
        # Can access security audit logs
        logs = requests.get(f"{BASE_URL}/admin/audit-logs", headers=headers)
        print(f"Permission: Security Audit Trail (/admin/audit-logs): {logs.status_code} ({'PERMITTED' if logs.status_code == 200 else 'DENIED'})")
        
        # Guard check: operational application mutation should be forbidden (View-Only guard)
        rev = requests.post(f"{BASE_URL}/admin/applications/1/review", json={"status": "APPROVED", "remarks": "Unauthorized test"}, headers=headers)
        print(f"View-Only Enforcement: Reject Mutation (/admin/applications/1/review): {rev.status_code} ({'STRICT GUARD ACTIVE' if rev.status_code == 403 else 'UNEXPECTED'})")

    return True

print("=== VERIFYING GOVERNMENT WELFARE ADMINISTRATOR ===")
welfare_ok = verify_account("welfareadmin@example.com", "Welfare@123", "Government Welfare Admin")

print("\n=== VERIFYING PLATFORM ADMINISTRATOR ===")
platform_ok = verify_account("platformadmin@example.com", "Platform@123", "Platform Admin")
