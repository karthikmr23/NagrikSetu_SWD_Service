import urllib.request, json

BASE_BACKEND = "http://localhost:8005/api/swd"
FRONTEND_URL = "http://localhost:5174"

results = []

def record(test_name, expected, actual, passed, details=""):
    results.append({
        "test": test_name,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })
    print(f"[{'PASS' if passed else 'FAIL'}] {test_name}")

# Test 1: Health
try:
    req = urllib.request.urlopen("http://localhost:8005/health")
    data = json.loads(req.read().decode())
    passed = (req.status == 200 and data.get("status") == "healthy")
    record("Backend /health endpoint", "HTTP 200, status=healthy", f"HTTP {req.status}, {data}", passed)
except Exception as e:
    record("Backend /health endpoint", "HTTP 200, status=healthy", str(e), False)

# Test 2: Frontend Availability
try:
    req = urllib.request.urlopen(FRONTEND_URL)
    passed = (req.status == 200)
    record("Frontend Web Interface (Port 5174)", "HTTP 200 OK", f"HTTP {req.status}", passed)
except Exception as e:
    record("Frontend Web Interface (Port 5174)", "HTTP 200 OK", str(e), False)

# Test 3: Citizen Login (Mukesh)
cit_token = None
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/auth/login", data=json.dumps({
        "email": "mukesh2345@gmail.com",
        "password": "CitizenPass@2026"
    }).encode(), headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req).read().decode())
    cit_token = res.get("access_token")
    passed = bool(cit_token and res.get("citizen_id") == "CIT-KA-2026-DE2B4F")
    record("Citizen Login (mukesh2345@gmail.com)", "JWT Token + Citizen ID issued", f"Token issued, citizen_id={res.get('citizen_id')}", passed)
except Exception as e:
    record("Citizen Login (mukesh2345@gmail.com)", "JWT Token issued", str(e), False)

# Test 4: Welfare Admin Login
welfare_token = None
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/auth/login", data=json.dumps({
        "email": "welfareadmin@example.com",
        "password": "AdminPass@2026"
    }).encode(), headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req).read().decode())
    welfare_token = res.get("access_token")
    passed = bool(welfare_token and res.get("role") in ["GOVERNMENT_WELFARE_ADMIN", "ADMINISTRATOR"])
    record("Welfare Admin Login (welfareadmin@example.com)", "JWT Token + Role authorized", f"Token issued, role={res.get('role')}", passed)
except Exception as e:
    record("Welfare Admin Login (welfareadmin@example.com)", "JWT Token issued", str(e), False)

# Test 5: Platform Admin Login
platform_token = None
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/auth/login", data=json.dumps({
        "email": "platformadmin@example.com",
        "password": "AdminPass@2026"
    }).encode(), headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req).read().decode())
    platform_token = res.get("access_token")
    passed = bool(platform_token and res.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"])
    record("Platform Admin Login (platformadmin@example.com)", "JWT Token + Platform Admin role", f"Token issued, role={res.get('role')}", passed)
except Exception as e:
    record("Platform Admin Login (platformadmin@example.com)", "JWT Token issued", str(e), False)

# Test 6: Scheme Catalogue
try:
    req = urllib.request.urlopen(f"{BASE_BACKEND}/schemes")
    schemes = json.loads(req.read().decode())
    has_shakti = any("shakti" in s.get("name", "").lower() for s in schemes)
    passed = (len(schemes) == 28 and not has_shakti)
    record("Public Scheme Catalogue (Shakti excluded)", "28 Karnataka schemes, 0 Shakti", f"{len(schemes)} schemes, Shakti included={has_shakti}", passed)
except Exception as e:
    record("Public Scheme Catalogue (Shakti excluded)", "28 schemes", str(e), False)

# Test 7: Citizen Application Tracking (Mukesh SWD-APP-2026-98E64D)
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/applications/CIT-KA-2026-DE2B4F", headers={"Authorization": f"Bearer {cit_token}"})
    apps = json.loads(urllib.request.urlopen(req).read().decode())
    target = next((a for a in apps if a.get("application_number") == "SWD-APP-2026-98E64D"), None)
    passed = (target is not None and target.get("status") == "UNDER_REVIEW")
    record("Application Tracking (SWD-APP-2026-98E64D)", "Application found with status UNDER_REVIEW", f"App found={target is not None}, status={target.get('status') if target else None}", passed)
except Exception as e:
    record("Application Tracking (SWD-APP-2026-98E64D)", "Application found", str(e), False)

# Test 8: PDF Receipt Download
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/applications/36/receipt", headers={"Authorization": f"Bearer {cit_token}"})
    resp = urllib.request.urlopen(req)
    content_type = resp.headers.get("Content-Type", "")
    pdf_bytes = resp.read()
    passed = (resp.status == 200 and "pdf" in content_type.lower() and pdf_bytes.startswith(b"%PDF-1.4"))
    record("Pure-Python PDF Receipt Generation", "HTTP 200, application/pdf, %PDF-1.4 header", f"HTTP {resp.status}, size={len(pdf_bytes)} bytes", passed)
except Exception as e:
    record("Pure-Python PDF Receipt Generation", "Valid PDF 1.4", str(e), False)

# Test 9: Welfare Admin Scrutiny Queue & Metrics
try:
    req = urllib.request.Request(f"{BASE_BACKEND}/admin/dashboard", headers={"Authorization": f"Bearer {welfare_token}"})
    dash = json.loads(urllib.request.urlopen(req).read().decode())
    passed = (dash.get("total_applications", 0) >= 44 and dash.get("total_schemes", 0) == 28)
    record("Welfare Admin Dashboard Metrics", "Dynamic MySQL counters (>=44 apps, 28 schemes)", f"total_applications={dash.get('total_applications')}, schemes={dash.get('total_schemes')}", passed)
except Exception as e:
    record("Welfare Admin Dashboard Metrics", "Dynamic counters", str(e), False)

# Test 10: Platform Admin Monitoring (Users & Audit Logs)
try:
    req_u = urllib.request.Request(f"{BASE_BACKEND}/admin/users", headers={"Authorization": f"Bearer {platform_token}"})
    users = json.loads(urllib.request.urlopen(req_u).read().decode())
    req_a = urllib.request.Request(f"{BASE_BACKEND}/admin/audit-logs", headers={"Authorization": f"Bearer {platform_token}"})
    audit = json.loads(urllib.request.urlopen(req_a).read().decode())
    passed = (len(users) >= 39 and len(audit) > 0)
    record("Platform Admin Monitoring APIs", "User list >= 39, Audit logs retrieved", f"Users={len(users)}, Audit logs={len(audit)}", passed)
except Exception as e:
    record("Platform Admin Monitoring APIs", "Users & Audit logs", str(e), False)

# Test 11: Grievance Resolution Workflow
try:
    # Submit grievance
    grv_payload = {
        "citizen_id": "CIT-KA-2026-DE2B4F",
        "citizen_name": "Mukesh",
        "category": "DIRECT_BENEFIT_TRANSFER",
        "subject": "Demo DBT Inquiry",
        "description": "Checking DBT status for academic demonstration."
    }
    req_g = urllib.request.Request(f"{BASE_BACKEND}/grievances", data=json.dumps(grv_payload).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {cit_token}"})
    grv_resp = json.loads(urllib.request.urlopen(req_g).read().decode())
    grv_id = grv_resp.get("id")
    
    # Admin resolves grievance
    res_payload = {
        "status": "RESOLVED",
        "officer_response": "Issue scrutinized and resolved for presentation verification."
    }
    req_r = urllib.request.Request(f"{BASE_BACKEND}/grievances/{grv_id}/resolve", data=json.dumps(res_payload).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {welfare_token}"}, method="PUT")
    res_resp = json.loads(urllib.request.urlopen(req_r).read().decode())
    passed = (res_resp.get("status") == "RESOLVED")
    record("Grievance Submission & Administrative Resolution", "Grievance status transitioned to RESOLVED", f"Ticket ID={grv_id}, final status={res_resp.get('status')}", passed)
except Exception as e:
    record("Grievance Submission & Administrative Resolution", "Transition to RESOLVED", str(e), False)

# Test 12: Unauthorized Access Restriction (RBAC Security)
try:
    # Citizen trying to call admin dashboard
    req_bad = urllib.request.Request(f"{BASE_BACKEND}/admin/dashboard", headers={"Authorization": f"Bearer {cit_token}"})
    urllib.request.urlopen(req_bad)
    record("RBAC Access Restriction (Citizen on Admin Route)", "HTTP 403 Forbidden", "HTTP 200 (Violation)", False)
except urllib.error.HTTPError as he:
    passed = (he.code == 403)
    record("RBAC Access Restriction (Citizen on Admin Route)", "HTTP 403 Forbidden", f"HTTP {he.code}", passed)
except Exception as e:
    record("RBAC Access Restriction (Citizen on Admin Route)", "HTTP 403 Forbidden", str(e), False)

with open(r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\functional_test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nCompleted {len(results)} functional tests. All logged to functional_test_results.json")
