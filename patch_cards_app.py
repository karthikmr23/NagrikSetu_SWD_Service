import re

file_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

card_replacements = [
    # Card 2
    ("SWD Officers & Scrutiny Desk", "Welfare Officers"),
    ("Category-wise and scheme-wise application scrutiny, verification desk, eligibility approval/rejection decisions, and DBT payment batch processing.",
     "Review applications, verify documents, request information, and sanction benefits."),
    ("Welfare Admin Officer Sign In", "Welfare Admin Sign In"),
    ("Default Officer: <strong>welfareadmin</strong>", "Officer Account: <strong>welfareadmin</strong>"),
    ("Access restricted to authorized District & Taluk SWD staff.", "Access restricted to authorized SWD staff."),
    
    # Card 3
    ("Super-Admin Command Center", "Super-Admin"),
    ("Full platform administration: user account management, role assignments, category and dynamic form definitions, and system-wide security audit trails.",
     "User management, role assignments, category configuration, and security audit logs."),
    ("Platform Admin Sign In", "Platform Admin Sign In"),
    ("Super-Admin Account: <strong>platformadmin</strong>", "Super-Admin: <strong>platformadmin</strong>"),
    ("Super-admin governance for NagrikSetu SWD.", "System governance and security administration.")
]

for old, new in card_replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"NOT FOUND: {old[:40]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Cards in App.tsx")
