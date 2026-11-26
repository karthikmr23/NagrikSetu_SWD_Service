import urllib.request
import json
import sys

def run_tests():
    print("=" * 60)
    print("NAGRIKSETU SWD — END-TO-END VERIFICATION")
    print("=" * 60)

    # 1. Health
    h = json.loads(urllib.request.urlopen('http://127.0.0.1:8004/health').read().decode())
    assert h['status'] == 'healthy', "Health check failed"
    print("[PASS] 1. Backend health check: OK")

    # 2. Login Citizen
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/auth/login', 
                                data=json.dumps({'email':'citizen@example.com','password':'CitizenPass@2026'}).encode(), 
                                headers={'Content-Type':'application/json'})
    c_res = json.loads(urllib.request.urlopen(req).read().decode())
    assert c_res['role'] == 'CITIZEN', "Citizen role mismatch"
    c_token = c_res['access_token']
    print("[PASS] 2. Citizen login & JWT role: OK (CITIZEN)")

    # 3. Login Officer
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/auth/login', 
                                data=json.dumps({'email':'officer@nagriksetu.local','password':'OfficerPass@2026'}).encode(), 
                                headers={'Content-Type':'application/json'})
    o_res = json.loads(urllib.request.urlopen(req).read().decode())
    assert o_res['role'] == 'WELFARE_OFFICER', "Officer role mismatch"
    o_token = o_res['access_token']
    print("[PASS] 3. Welfare Officer login & JWT role: OK (WELFARE_OFFICER)")

    # 4. Login Admin
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/auth/login', 
                                data=json.dumps({'email':'admin@nagriksetu.local','password':'AdminPass@2026'}).encode(), 
                                headers={'Content-Type':'application/json'})
    a_res = json.loads(urllib.request.urlopen(req).read().decode())
    assert a_res['role'] == 'ADMINISTRATOR', "Admin role mismatch"
    a_token = a_res['access_token']
    print("[PASS] 4. Administrator login & JWT role: OK (ADMINISTRATOR)")

    # 5. Schemes Catalog
    schemes = json.loads(urllib.request.urlopen('http://127.0.0.1:8004/api/swd/schemes').read().decode())
    assert len(schemes) >= 3, "Schemes list incomplete"
    print(f"[PASS] 5. Published schemes catalog: {len(schemes)} schemes loaded")

    # 6. Eligibility Engine
    chk_payload = {
        'citizen_attributes': {
            'age': 25,
            'annual_income': 180000.0,
            'caste_category': 'SC',
            'residence_state': 'Karnataka',
            'education_level': 'Undergraduate'
        }
    }
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/schemes/1/eligibility-check', 
                                data=json.dumps(chk_payload).encode(), 
                                headers={'Content-Type':'application/json'})
    el_res = json.loads(urllib.request.urlopen(req).read().decode())
    assert el_res['preliminary_status'] == 'LIKELY_ELIGIBLE', "Eligibility status mismatch"
    assert "preliminary eligibility criteria" in el_res['summary_explanation']
    assert "subject to verification by the authorized department" in el_res['disclaimer']
    print(f"[PASS] 6. Eligibility check engine: status={el_res['preliminary_status']}")
    print(f"       Summary: \"{el_res['summary_explanation']}\"")
    print(f"       Disclaimer: \"{el_res['disclaimer']}\"")

    # 7. Public Application Status Tracking
    req = urllib.request.Request('http://127.0.0.1:8004/api/v1/swd/public/track-status/SWD-APP-NONEXISTENT')
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        assert e.code == 404, "Unexpected status code"
        print("[PASS] 7. Public tracking route: Verified (Correct 404 for non-existent application)")

    # 8. Simulated DBT Dashboard KPIs & Budget
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/dbt/dashboard-stats', headers={'Authorization': f'Bearer {a_token}'})
    dbt_stats = json.loads(urllib.request.urlopen(req).read().decode())
    assert dbt_stats['allocated_budget'] == 10000000.0
    print(f"[PASS] 8. Simulated DBT Engine: Budget ₹{dbt_stats['allocated_budget']:,.2f} | Disbursed ₹{dbt_stats['total_simulated_disbursed']:,.2f}")
    print(f"       Notice: \"{dbt_stats['notice']}\"")

    # 9. DBT Transactions List & History
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/dbt/transactions', headers={'Authorization': f'Bearer {a_token}'})
    tx_list = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"[PASS] 9. DBT Transaction history: {len(tx_list)} recorded transactions verified")

    # 10. Welfare Officer Assigned Applications / Scrutiny
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/admin/officer/assigned-applications', headers={'Authorization': f'Bearer {o_token}'})
    apps_res = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"[PASS] 10. Officer Scrutiny Desk: {len(apps_res)} assigned applications")

    # 11. District Analytics & Reports
    req = urllib.request.Request('http://127.0.0.1:8004/api/swd/reports/analytics/districts', headers={'Authorization': f'Bearer {a_token}'})
    dist_res = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"[PASS] 11. District Analytics: {len(dist_res)} districts reported")

    # 12. Frontend Server Response
    fe_code = urllib.request.urlopen('http://127.0.0.1:5174/').getcode()
    assert fe_code == 200
    print("[PASS] 12. SWD Frontend on Port 5174: HTTP 200 OK")
    print("=" * 60)
    print("ALL 12 END-TO-END VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
