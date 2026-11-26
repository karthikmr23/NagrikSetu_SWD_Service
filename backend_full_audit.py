import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:8005"

def post_json(path, data, token=None):
    payload = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def get_json(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def run_tests():
    print("================================================================================")
    print("NAGRIKSETU SWD — COMPREHENSIVE BACKEND API & WORKFLOW ACCEPTANCE SUITE")
    print("================================================================================")

    results = {}

    # 1. Health check
    status, data = get_json("/health")
    passed = (status == 200 and data.get("status") == "healthy")
    results["T01_Health_Check"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T01_Health_Check']}] T01 Health Check: {data}")

    # 2. Scheme Catalogue (All 34 valid SWD schemes, non-SWD Shakti excluded)
    status, data = get_json("/api/swd/schemes")
    passed = (status == 200 and len(data) == 28)
    results["T02_Scheme_Catalogue_Count"] = "PASS" if passed else f"FAIL ({status}, count={len(data) if isinstance(data, list) else 0})"
    print(f"[{results['T02_Scheme_Catalogue_Count']}] T02 Scheme Catalogue Count: {len(data) if isinstance(data, list) else 0} schemes")

    # 3. Category Listing
    status, data = get_json("/api/swd/categories")
    passed = (status == 200 and len(data) == 9)
    results["T03_Category_Count"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T03_Category_Count']}] T03 Scheme Categories: {len(data) if isinstance(data, list) else 0} categories")

    # 4. Deterministic Eligibility Check (Scheme 1)
    status, data = post_json("/api/swd/schemes/5/eligibility-check", {
        "citizen_attributes": {
            "annual_income": 150000,
            "caste_category": "SC",
            "residence_state": "Karnataka",
            "age": 30,
            "gender": "female",
            "is_woman": True
        }
    })
    passed = (status == 200 and isinstance(data, dict) and data.get("preliminary_status") == "LIKELY_ELIGIBLE")
    results["T04_Eligibility_Evaluation"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T04_Eligibility_Evaluation']}] T04 Eligibility Rule Engine (Scheme 5): Preliminary Status={data.get('preliminary_status') if isinstance(data, dict) else data}")

    # 5. Smart Scheme Finder Options & Match
    status, opt_data = get_json("/api/swd/finder/options")
    status2, match_resp = post_json("/api/swd/finder/match", {
        "annual_income": 120000,
        "caste_category": "SC",
        "residence_district": "Bengaluru Urban",
        "age": 21
    })
    results_list = match_resp.get("results", []) if isinstance(match_resp, dict) else []
    passed = (status == 200 and status2 == 200 and len(results_list) == 28)
    results["T05_Smart_Scheme_Finder"] = "PASS" if passed else f"FAIL (opt={status}, match={status2})"
    print(f"[{results['T05_Smart_Scheme_Finder']}] T05 Smart Scheme Finder: {len(results_list)} matched schemes (Total Matches: {match_resp.get('total_matches')})")

    # 6. Citizen Login
    status, cit_auth = post_json("/api/swd/auth/login", {"email": "citizen@example.com", "password": "CitizenPass@2026"})
    cit_token = cit_auth.get("access_token") if status == 200 else None
    passed = (status == 200 and cit_auth.get("role") == "CITIZEN" and cit_token is not None)
    results["T06_Citizen_Authentication"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T06_Citizen_Authentication']}] T06 Citizen Login: User={cit_auth.get('name')} Role={cit_auth.get('role')}")

    # 7. Citizen Profile & Own Applications
    status, my_apps = get_json("/api/swd/applications/CIT-KA-9901", token=cit_token)
    passed = (status == 200 and isinstance(my_apps, list))
    results["T07_Citizen_Own_Applications"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T07_Citizen_Own_Applications']}] T07 Citizen Applications Retrieval: {len(my_apps) if isinstance(my_apps, list) else 0} records")

    # 8. Citizen Data Isolation Guard (Cross-citizen access attempt)
    status, cross_data = get_json("/api/swd/applications/CIT-KA-TEST-001", token=cit_token)
    passed = (status == 403)
    results["T08_Citizen_Data_Isolation_Guard"] = "PASS" if passed else f"FAIL (Got {status}, expected 403)"
    print(f"[{results['T08_Citizen_Data_Isolation_Guard']}] T08 Citizen Isolation Guard: Attempt cross-read returned HTTP {status} (Expected 403)")

    # 9. Citizen Blocked from Administrative Operations
    status, admin_data = get_json("/api/swd/admin/dashboard", token=cit_token)
    passed = (status == 403)
    results["T09_Citizen_Admin_Mutation_Guard"] = "PASS" if passed else f"FAIL (Got {status}, expected 403)"
    print(f"[{results['T09_Citizen_Admin_Mutation_Guard']}] T09 Citizen Admin Access Guard: Attempt admin read returned HTTP {status} (Expected 403)")

    # 10. Welfare Admin Authentication
    status, welf_auth = post_json("/api/swd/auth/login", {"email": "welfareadmin@example.com", "password": "Welfare@123"})
    welf_token = welf_auth.get("access_token") if status == 200 else None
    passed = (status == 200 and welf_auth.get("role") == "GOVERNMENT_WELFARE_ADMIN" and welf_token is not None)
    results["T10_Welfare_Admin_Authentication"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T10_Welfare_Admin_Authentication']}] T10 Welfare Admin Login: User={welf_auth.get('name')} Role={welf_auth.get('role')}")

    # 11. Welfare Admin Dashboard & Applications Queue
    status, dash_data = get_json("/api/swd/admin/dashboard", token=welf_token)
    status2, apps_queue = get_json("/api/swd/admin/applications", token=welf_token)
    passed = (status == 200 and status2 == 200 and len(apps_queue) == 35)
    results["T11_Welfare_Admin_Dashboard_And_Queue"] = "PASS" if passed else f"FAIL (dash={status}, queue={status2})"
    print(f"[{results['T11_Welfare_Admin_Dashboard_And_Queue']}] T11 Welfare Admin Dashboard & Queue: {len(apps_queue) if isinstance(apps_queue, list) else 0} apps in queue")

    # 12. Welfare Admin Beneficiary Ledger
    status, bens = get_json("/api/swd/beneficiaries", token=welf_token)
    passed = (status == 200 and isinstance(bens, list) and len(bens) >= 20)
    results["T12_Beneficiary_Ledger"] = "PASS" if passed else f"FAIL ({status}, count={len(bens) if isinstance(bens, list) else 0})"
    print(f"[{results['T12_Beneficiary_Ledger']}] T12 Beneficiary Ledger: {len(bens) if isinstance(bens, list) else 0} beneficiaries")

    # 13. Simulated DBT Transactions & Batch Report
    status, dbt_stats = get_json("/api/swd/dbt/dashboard-stats", token=welf_token)
    status2, dbt_txs = get_json("/api/swd/dbt/transactions", token=welf_token)
    passed = (status == 200 and status2 == 200)
    results["T13_DBT_Simulated_Console"] = "PASS" if passed else f"FAIL (stats={status}, txs={status2})"
    print(f"[{results['T13_DBT_Simulated_Console']}] T13 Simulated DBT Transactions: {len(dbt_txs) if isinstance(dbt_txs, list) else 0} transactions tracked")

    # 14. Grievance Redressal Endpoint
    status, grvs = get_json("/api/swd/grievances", token=welf_token)
    passed = (status == 200 and isinstance(grvs, list) and len(grvs) >= 28)
    results["T14_Grievance_List"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T14_Grievance_List']}] T14 Grievances Queue: {len(grvs) if isinstance(grvs, list) else 0} grievances loaded")

    # 15. Notifications Stream
    status, notifs = get_json("/api/swd/notifications/CIT-KA-9901", token=cit_token)
    passed = (status == 200 and isinstance(notifs, list) and len(notifs) > 0)
    results["T15_Notification_Stream"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T15_Notification_Stream']}] T15 Notifications Stream: {len(notifs) if isinstance(notifs, list) else 0} notifications for CIT-KA-9901")

    # 16. Platform Admin Authentication & Access Guard
    status, plat_auth = post_json("/api/swd/auth/login", {"email": "platformadmin@example.com", "password": "Platform@123"})
    plat_token = plat_auth.get("access_token") if status == 200 else None
    passed = (status == 200 and plat_auth.get("role") == "PLATFORM_ADMIN" and plat_token is not None)
    results["T16_Platform_Admin_Authentication"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T16_Platform_Admin_Authentication']}] T16 Platform Admin Login: Role={plat_auth.get('role')}")

    # 17. Platform Admin Welfare Mutation Restriction (HTTP 422/403)
    status, plat_mut = post_json("/api/swd/admin/rules/test-draft", {}, token=plat_token)
    passed = (status in [403, 422])
    results["T17_Platform_Admin_Mutation_Guard"] = "PASS" if passed else f"FAIL (Got {status})"
    print(f"[{results['T17_Platform_Admin_Mutation_Guard']}] T17 Platform Admin Mutation Guard: Rejected with HTTP {status}")

    # 18. Office Locator Endpoints
    status, offices = get_json("/api/swd/offices")
    passed = (status == 200 and len(offices) == 10)
    results["T18_Office_Locator"] = "PASS" if passed else f"FAIL ({status})"
    print(f"[{results['T18_Office_Locator']}] T18 Office Locator: {len(offices) if isinstance(offices, list) else 0} offices loaded")

    # 19. Application PDF Receipt Endpoint
    req_receipt = urllib.request.Request(f"{BASE_URL}/api/swd/applications/1/receipt", headers={"Authorization": f"Bearer {cit_token}"})
    try:
        with urllib.request.urlopen(req_receipt) as resp:
            content = resp.read()
            passed = (resp.status == 200 and content.startswith(b"%PDF"))
            results["T19_PDF_Receipt_Generation"] = "PASS" if passed else f"FAIL (status={resp.status})"
            print(f"[{results['T19_PDF_Receipt_Generation']}] T19 Application PDF Receipt: {len(content)} bytes (Starts with %PDF)")
    except Exception as e:
        results["T19_PDF_Receipt_Generation"] = f"FAIL ({e})"
        print(f"[FAIL] T19 Application PDF Receipt: {e}")

    total_passed = sum(1 for v in results.values() if v == "PASS")
    print("\n================================================================================")
    print(f"BACKEND TEST SUMMARY: {total_passed}/{len(results)} TESTS PASSED ({round(total_passed/len(results)*100)}%)")
    print("================================================================================")
    return results

if __name__ == "__main__":
    run_tests()
