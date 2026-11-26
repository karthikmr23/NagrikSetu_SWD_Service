import requests
import json

BASE = "http://localhost:8005/api/swd"

def check():
    r = requests.get(f"{BASE}/schemes")
    schemes = r.json()
    print(f"Total schemes returned by API: {len(schemes)}")
    shakti = [s for s in schemes if "shakti" in s.get("name", "").lower() or "shakti" in s.get("code", "").lower()]
    print(f"Shakti in API response: {shakti}")
    
    print("\nAll 35 Scheme Names:")
    for s in schemes:
        print(f"ID {s['id']}: {s['code']} - {s['name']} (Cat: {s.get('category')})")

if __name__ == "__main__":
    check()
