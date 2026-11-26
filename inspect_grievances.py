import jwt
import datetime
import requests

JWT_SECRET = "nagriksetu-swd-super-secret-key-2026-xyz-min32chars"

def create_token(payload: dict) -> str:
    p = payload.copy()
    p["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    p["iat"] = datetime.datetime.now(datetime.timezone.utc)
    return jwt.encode(p, JWT_SECRET, algorithm="HS256")

token = create_token({
    "sub": "ADM-SWD-001",
    "email": "swd.superadmin@karnataka.gov.in",
    "name": "SWD Platform Super Admin",
    "role": "PLATFORM_ADMIN",
    "citizen_id": "ADM-SWD-001"
})

BASE = 'http://localhost:8005/api/swd'
headers = {'Authorization': f'Bearer {token}'}

g_resp = requests.get(f'{BASE}/grievances?limit=100', headers=headers)
data = g_resp.json()

print(f"Total grievances: {len(data)}")
for g in data:
    cid = g.get('citizen_id')
    gid = g.get('id')
    num = g.get('grievance_number')
    subj = g.get('subject')
    desc = g.get('description')
    created = g.get('created_at')
    print(f"[{gid}] {cid} | {num} | {subj} | {created} | {desc[:40]}")
