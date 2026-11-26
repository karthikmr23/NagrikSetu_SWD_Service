import urllib.request
import json

def post(url, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, json.loads(r.read().decode('utf-8'))

def get(url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, json.loads(r.read().decode('utf-8'))

def run_trace():
    lines = []
    lines.append("=== TRACE FOR APPLICATION SWD-APP-2026-98E64D ===\n")

    # 1. Citizen Mukesh login
    s_m, tok_m = post('http://localhost:8005/api/swd/auth/login', {'email': 'mukesh2345@gmail.com', 'password': 'CitizenPass@2026'})
    lines.append(f"1. Citizen Login (mukesh2345@gmail.com) -> HTTP {s_m}")
    cid = tok_m['citizen_id']
    m_token = tok_m['access_token']

    # 2. Citizen application list & tracking response
    s_c, apps_c = get(f'http://localhost:8005/api/swd/applications/{cid}', m_token)
    mukesh_app = [a for a in apps_c if a['application_number'] == 'SWD-APP-2026-98E64D'][0]
    lines.append(f"2. Citizen Tracking API (GET /api/swd/applications/{cid}) -> HTTP {s_c}")
    lines.append(f"   App Number: {mukesh_app['application_number']}")
    lines.append(f"   Scheme: {mukesh_app['scheme']['name']}")
    lines.append(f"   Status: {mukesh_app['status']}")
    lines.append(f"   Admin Remarks: {mukesh_app['admin_remarks']}")
    lines.append(f"   History Steps: {len(mukesh_app['history'])}")
    for h in mukesh_app['history']:
        lines.append(f"     - Action: {h['action_type']} | From: {h['from_status']} | To: {h['to_status']} | By: {h['changed_by']} | Remarks: {h['remarks']}")

    # 3. Government Welfare Admin login
    s_w, tok_w = post('http://localhost:8005/api/swd/auth/login', {'email': 'welfareadmin@example.com', 'password': 'AdminPass@2026'})
    lines.append(f"\n3. Welfare Admin Login (welfareadmin@example.com) -> HTTP {s_w}, Role: {tok_w['role']}")
    w_token = tok_w['access_token']

    # 4. Welfare Admin Scrutiny Queue
    s_q, apps_q = get('http://localhost:8005/api/swd/admin/applications', w_token)
    admin_mukesh = [a for a in apps_q if a['application_number'] == 'SWD-APP-2026-98E64D'][0]
    lines.append(f"4. Welfare Admin Scrutiny Queue API (GET /api/swd/admin/applications) -> HTTP {s_q}")
    lines.append(f"   Found Mukesh Application in Queue: {admin_mukesh['application_number']}")
    lines.append(f"   Applicant: {admin_mukesh['citizen_name']}")
    lines.append(f"   Primary Key ID: {admin_mukesh['id']}")
    lines.append(f"   Scheme ID: {admin_mukesh['scheme_id']}")
    lines.append(f"   Status: {admin_mukesh['status']}")
    lines.append(f"   Uploaded Documents Count: {len(admin_mukesh.get('documents', []))}")
    for d in admin_mukesh.get('documents', []):
        lines.append(f"     - Doc ID: {d['id']} | Code: {d['document_code']} | Name: {d['file_name']}")

    output = "\n".join(lines)
    print(output)
    with open(r'C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\AUDIT_EVIDENCE\api_responses\mukesh_exact_application_trace.txt', 'w', encoding='utf-8') as f:
        f.write(output)

if __name__ == '__main__':
    run_trace()
