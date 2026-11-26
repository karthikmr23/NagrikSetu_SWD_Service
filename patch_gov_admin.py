import re

file_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\GovernmentWelfareAdminPortal.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # Top banner
    ("Government of Karnataka &bull; Social Welfare Department", "Government of Karnataka &bull; Social Welfare"),
    ("Government Welfare Admin Portal", "Welfare Admin Portal"),
    # Nav tabs
    ("Administrative Overview", "Overview"),
    ("Welfare Scheme Categories ({categoryStats.length})", "Categories ({categoryStats.length})"),
    ("All Applications ({totalApps})", "Applications ({totalApps})"),
    # Dashboard KPI cards
    ("Total Applications", "Applications"),
    ("Across {categoryStats.length} welfare categories", "{categoryStats.length} categories"),
    ("New Dossiers (Submitted)", "New Submissions"),
    ("Awaiting initial officer review", "Awaiting review"),
    ("Under Scrutiny", "In Review"),
    ("Active investigation in progress", "Under scrutiny"),
    ("Correction Requested", "Action Required"),
    ("Pending citizen resubmission", "Pending citizen action"),
    ("Approved & Sanctioned", "Approved"),
    ("Beneficiary ledger recorded", "Sanctioned"),
    ("Rejected Dossiers", "Rejected"),
    ("Ineligible or non-compliant", "Not approved"),
    # Category heading
    ("Welfare Scheme Categories & Automatic Routing Desks", "Welfare Scheme Categories"),
    ("Click any category to inspect scheme-wise applications", "Select a category to view schemes"),
    # Application scrutiny desk
    ("Application Scrutiny & Verification Desk", "Application Scrutiny"),
    ("Showing {applications.length} applications matching current administrative filters.", "{applications.length} applications"),
    # Scrutiny Action Modal / Buttons
    ("Commit Administrative Decision & Notify Citizen", "Save Decision"),
    ("Recording Decision in MySQL...", "Saving..."),
    ("Filter Applications for this Scheme ({sc.total_applications}) &rarr;", "View Applications ({sc.total_applications}) &rarr;"),
    ("View All {selectedCategory.total_applications} Applications in this Category &rarr;", "View Applications ({selectedCategory.total_applications}) &rarr;"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"NOT FOUND: {old[:40]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated GovernmentWelfareAdminPortal.tsx")
