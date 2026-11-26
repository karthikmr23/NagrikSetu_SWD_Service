import re

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\auth.py", "r", encoding="utf-8") as f:
    text = f.read()

endpoints = re.findall(r"@router\.(get|post|put|delete)\((.*?)\)\ndef\s+(\w+)\((.*?)\):", text, re.DOTALL)
for ep in endpoints:
    method = ep[0].upper()
    route = ep[1].split(',')[0].strip('"\' ')
    func_name = ep[2]
    role_match = re.search(r"require_role\(\[(.*?)\]\)", ep[3])
    role_str = role_match.group(1) if role_match else "None"
    print(f"{method} {route} -> {func_name} | Roles: {role_str}")
