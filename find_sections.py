import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find key lines
for idx, line in enumerate(lines):
    if "async function handleDedicatedLogin" in line:
        print(f"handleDedicatedLogin at line {idx+1}")
    if "async function handlePortalLogin" in line:
        print(f"handlePortalLogin at line {idx+1}")
    if "async function handleLogin" in line:
        print(f"handleLogin at line {idx+1}")
    if "userRole === 'CITIZEN' ? (" in line:
        print(f"userRole === CITIZEN nav at line {idx+1}")
    if "VIEW: CITIZEN GRIEVANCE" in line:
        print(f"VIEW: CITIZEN GRIEVANCE at line {idx+1}")
    if "VIEW: CITIZEN MY GRIEVANCES" in line:
        print(f"VIEW: CITIZEN MY GRIEVANCES at line {idx+1}")
    if "VIEW: CITIZEN NOTIFICATIONS" in line:
        print(f"VIEW: CITIZEN NOTIFICATIONS at line {idx+1}")
