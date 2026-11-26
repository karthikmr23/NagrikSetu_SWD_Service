import requests
import json

BASE = "http://localhost:8005/api/swd"

def inspect():
    # 1. Check scheme 7 details
    r = requests.get(f"{BASE}/schemes/7")
    print(f"Scheme 7 Status Code: {r.status_code}")
    if r.status_code == 200:
        s = r.json()
        print(f"Scheme 7: ID={s.get('id')}, Code={s.get('scheme_code')}, Name={s.get('name')}, Dept={s.get('department')}")
    
    # 2. Check if any applications exist for scheme 7
    # Login as Welfare Admin to check applications queue
    login_payload = {
        "email": "welfareadmin@example.com",
        "password": "Welfare@123"
    }
    r_auth = requests.post(f"{BASE}/auth/login", json=login_payload)
    if r_auth.status_code == 200:
        token = r_auth.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Check applications
        r_apps = requests.get(f"{BASE}/applications", headers=headers)
        if r_apps.status_code == 200:
            apps = r_apps.json()
            shakti_apps = [a for a in apps if a.get("scheme_id") == 7 or "shakti" in str(a).lower()]
            print(f"Total applications in system: {len(apps)}")
            print(f"Applications for Shakti Scheme (ID 7): {len(shakti_apps)}")
            for a in shakti_apps:
                print(f"  App: ID={a.get('id')}, Num={a.get('application_number')}, Status={a.get('status')}, Citizen={a.get('citizen_id')}")
        
        # Check beneficiaries
        r_bens = requests.get(f"{BASE}/beneficiaries", headers=headers)
        if r_bens.status_code == 200:
            bens = r_bens.json()
            shakti_bens = [b for b in bens if b.get("scheme_id") == 7 or "shakti" in str(b).lower()]
            print(f"Total beneficiaries: {len(bens)}")
            print(f"Beneficiaries for Shakti Scheme: {len(shakti_bens)}")
            for b in shakti_bens:
                print(f"  Beneficiary: ID={b.get('id')}, Code={b.get('beneficiary_code')}, Status={b.get('status')}")

        # Check dynamic form for scheme 7
        r_form = requests.get(f"{BASE}/schemes/7/form", headers=headers)
        print(f"Dynamic form for Scheme 7: Status={r_form.status_code}, Has Form={r_form.json() is not None}")
        if r_form.status_code == 200 and r_form.json():
            print(f"  Form fields count: {len(r_form.json().get('fields', []))}")

if __name__ == "__main__":
    inspect()
