import urllib.request, json

BASE_URL = "http://localhost:8005/api/swd/schemes"

# 8 schemes to test:
# 1. Udyogini Scheme (ID: 10)
# 2. Bhagyalakshmi Scheme (ID: 11)
# 3. Matru Poorna Scheme (ID: 12)
# 4. Thayi Bhagya & Prasoothi Araike Scheme (ID: 13)
# 5. Madilu Kit Scheme (ID: 14)
# 6. Santhwana Scheme (ID: 15)
# 7. Dhanashree & Chetana Scheme (ID: 16)
# 8. Gruha Arogya Yojana (ID: 35)

schemes_config = [
    {
        "id": 10,
        "name": "Udyogini Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female", "age": 28, "annual_income": 120000},
        "failed": {"residence_state": "Karnataka", "gender": "Male", "age": 28, "annual_income": 120000}, # Failed gender/is_woman
        "missing": {"residence_state": "Karnataka", "annual_income": 120000} # Missing gender/is_woman and age
    },
    {
        "id": 11,
        "name": "Bhagyalakshmi Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female"},
        "failed": {"residence_state": "Karnataka", "gender": "Male"}, # Failed gender
        "missing": {"residence_state": "Karnataka"} # Missing gender
    },
    {
        "id": 12,
        "name": "Matru Poorna Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female"},
        "failed": {"residence_state": "Karnataka", "gender": "Male"}, # Failed is_woman
        "missing": {"residence_state": "Karnataka"} # Missing gender/is_woman
    },
    {
        "id": 13,
        "name": "Thayi Bhagya & Prasoothi Araike Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female"},
        "failed": {"residence_state": "Karnataka", "gender": "Male"}, # Failed is_woman
        "missing": {"residence_state": "Karnataka"} # Missing gender/is_woman
    },
    {
        "id": 14,
        "name": "Madilu Kit Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female", "institutional_delivery": True},
        "failed": {"residence_state": "Karnataka", "gender": "Female", "institutional_delivery": False}, # Failed delivery
        "missing": {"residence_state": "Karnataka", "gender": "Female"} # Missing institutional_delivery
    },
    {
        "id": 15,
        "name": "Santhwana Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female"},
        "failed": {"residence_state": "Karnataka", "gender": "Male"}, # Failed is_woman
        "missing": {"residence_state": "Karnataka"} # Missing gender/is_woman
    },
    {
        "id": 16,
        "name": "Dhanashree & Chetana Scheme",
        "satisfied": {"residence_state": "Karnataka", "gender": "Female", "age": 30},
        "failed": {"residence_state": "Karnataka", "gender": "Male", "age": 30}, # Failed is_woman
        "missing": {"residence_state": "Karnataka", "gender": "Female"} # Missing age
    },
    {
        "id": 35,
        "name": "Gruha Arogya Yojana",
        "satisfied": {"residence_state": "Karnataka", "age": 45},
        "failed": {"residence_state": "Karnataka", "age": 22}, # Failed age < 30
        "missing": {"residence_state": "Karnataka"} # Missing age
    }
]

def check(scheme_id, payload):
    req = urllib.request.Request(
        f"{BASE_URL}/{scheme_id}/eligibility-check",
        data=json.dumps({"citizen_attributes": payload}).encode(),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode())

print("=== EXECUTING ELIGIBILITY ASSESSMENT AUDIT (8 SCHEMES x 3 SCENARIOS) ===")
all_pass = True

for s in schemes_config:
    sid = s["id"]
    sname = s["name"]
    print(f"\n------------------------------------------------------------")
    print(f"SCHEME {sid}: {sname}")
    print(f"------------------------------------------------------------")

    # 1. Satisfied Scenario
    res_sat = check(sid, s["satisfied"])
    status_sat = res_sat.get("preliminary_status")
    sat_ok = (status_sat == "LIKELY_ELIGIBLE")
    print(f"  [Scenario 1: SATISFIED]")
    print(f"    Payload: {s['satisfied']}")
    print(f"    Expected: LIKELY_ELIGIBLE | Actual: {status_sat}")
    print(f"    Summary: {res_sat.get('summary_explanation')}")
    print(f"    Evaluation: {'PASS' if sat_ok else 'FAIL'}")
    if not sat_ok: all_pass = False

    # 2. Failed Scenario
    res_fail = check(sid, s["failed"])
    status_fail = res_fail.get("preliminary_status")
    fail_ok = (status_fail == "NOT_ELIGIBLE")
    print(f"  [Scenario 2: FAILED MANDATORY]")
    print(f"    Payload: {s['failed']}")
    print(f"    Expected: NOT_ELIGIBLE | Actual: {status_fail}")
    print(f"    Summary: {res_fail.get('summary_explanation')}")
    print(f"    Evaluation: {'PASS' if fail_ok else 'FAIL'}")
    if not fail_ok: all_pass = False

    # 3. Missing Scenario
    res_miss = check(sid, s["missing"])
    status_miss = res_miss.get("preliminary_status")
    miss_ok = (status_miss == "INSUFFICIENT_INFORMATION")
    print(f"  [Scenario 3: MISSING MANDATORY]")
    print(f"    Payload: {s['missing']}")
    print(f"    Expected: INSUFFICIENT_INFORMATION | Actual: {status_miss}")
    print(f"    Missing Fields: {res_miss.get('missing_fields')}")
    print(f"    Summary: {res_miss.get('summary_explanation')}")
    print(f"    Evaluation: {'PASS' if miss_ok else 'FAIL'}")
    if not miss_ok: all_pass = False

print("\n============================================================")
print(f"FINAL AUDIT RESULT: {'ALL 24 SCENARIOS PASSED WITH 100% ACCURACY' if all_pass else 'SOME SCENARIOS FAILED'}")
print("============================================================")
