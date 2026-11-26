import requests

BASE = 'http://localhost:8005/api/swd'
hidden_names = [
    'Post-Matric Scholarship',
    'Disability Maintenance',
    'Farmer Irrigation Assistance Scheme',
    'ELEVATE',
    'Rajiv Gandhi Entrepreneurship',
    'Ambedkar Karmika'
]

for name in hidden_names:
    r = requests.get(f'{BASE}/schemes?search={name}')
    data = r.json()
    print(f'Search for "{name}": {len(data)} results -> {[d["name"] for d in data]}')
