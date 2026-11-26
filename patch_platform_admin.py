import re

file_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\PlatformAdminPortal.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # Top banner
    ("System Governance & Platform Administration", "Governance & Administration"),
    ("NagrikSetu Platform Admin Command Center", "Platform Admin Center"),
    # Nav tabs
    ("Platform Overview", "Overview"),
    ("User & Officer Access Management ({users.length})", "Users ({users.length})"),
    ("Welfare Categories Management ({categories.length})", "Categories ({categories.length})"),
    ("Administrative Audit Logs", "Audit Logs"),
    # Overview KPI cards
    ("Registered Users", "Users"),
    ("Citizens, Officers & Admins", "Citizens & Officers"),
    ("Welfare Categories", "Categories"),
    ("Routing departments", "Active departments"),
    ("Total Audit Entries", "Audit Entries"),
    ("Recorded security actions", "Security events"),
    # Users section
    ("User Accounts & Role Permissions", "Users & Roles"),
    ("Search user name or email...", "Search users..."),
    # Categories section
    ("Welfare Categories Management", "Welfare Categories"),
    # Audit log section
    ("Administrative Security Audit Trail", "Audit Log"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"NOT FOUND: {old[:40]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated PlatformAdminPortal.tsx")
