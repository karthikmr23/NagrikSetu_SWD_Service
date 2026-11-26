import requests

BASE = "http://localhost:8005/api/swd"
r_auth = requests.post(f"{BASE}/auth/login", json={"email": "citizen@example.com", "password": "CitizenPass@2026"})
cit_token = r_auth.json().get("access_token")
headers = {"Authorization": f"Bearer {cit_token}"}

r_apply = requests.post(f"{BASE}/schemes/7/applications", json={
    "citizen_id": "CIT-KA-9901",
    "citizen_name": "Ramesh Kumar Nayak",
    "citizen_phone": "9876543210",
    "residence_district": "Bengaluru Urban",
    "annual_income": 120000,
    "caste_category": "SC",
    "bank_account_number": "123456789012",
    "bank_ifsc": "SBIN0001234",
    "form_data": {}
}, headers=headers)

print(f"Status: {r_apply.status_code}")
print(f"Response: {r_apply.json()}")
