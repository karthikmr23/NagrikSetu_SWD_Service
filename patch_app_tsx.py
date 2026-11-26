import re

file_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # Top banner & Nav
    ("Social Welfare Department (SWD) Portal", "Social Welfare Department"),
    ("Social Welfare Services and Scheme Management &bull; NagrikSetu Platform", "Karnataka Social Welfare & Direct Benefit Transfer"),
    ("Dedicated digital civic gateway for social security pensions, post-matric education scholarships, Divyangjan disability assistance, and inter-caste marital incentives. Check preliminary eligibility against official government criteria and submit your application online.",
     "Access social pensions, student scholarships, disability assistance, and welfare schemes. Check eligibility and apply online."),
    ("Smart Scheme Finder &rarr;", "Scheme Finder"),
    ("Browse Welfare Schemes &rarr;", "Browse Schemes"),
    ("Check Scheme Eligibility", "Check Eligibility"),
    ("Go to My Dashboard", "My Dashboard"),
    
    # Pillars Section
    ("&bull; SOCIAL WELFARE SERVICE PILLARS &bull;", "&bull; SCHEME CATEGORIES &bull;"),
    ("Core Citizen Welfare Categories", "Welfare Categories"),
    ("Access social welfare schemes, check eligibility, submit applications and track your application status in one place.",
     "Explore government welfare schemes by category."),
    
    # Category stream cards
    ("Explore 5 Schemes", "View Schemes"),
    ("Explore 7 Schemes", "View Schemes"),
    ("Explore 6 Schemes", "View Schemes"),
    ("Administered Schemes:", "Featured Schemes:"),
    
    # Citizen Portal View
    ("Citizen Welfare Dashboard", "Citizen Dashboard"),
    ("Verified citizen parameters used for automated welfare eligibility evaluation and DBT transactions.",
     "Your verified profile for scheme eligibility and DBT."),
    ("My Welfare Applications Portfolio", "My Applications"),
    ("Submitted Applications", "Total Applications"),
    ("Approved Sanctions", "Approved"),
    ("Under Review / Action Required", "In Progress"),
    ("Direct Benefit Mandates", "Sanctioned"),
    ("Track Dossier &rarr;", "Track &rarr;"),
    ("Download Application Receipt (PDF)", "Download Receipt"),
    ("Download Official Application Receipt", "Download Receipt"),
    ("Citizen Registry Profile (SWD)", "Citizen Profile"),
    ("Edit Citizen Demographics & Banking Details", "Edit Profile"),
    ("Cancel Editing", "Cancel"),
    ("&larr; Back to Dashboard", "&larr; Back"),
    ("&larr; Back to Home", "&larr; Back"),
    ("&larr; Back to Portfolio", "&larr; Back"),
    
    # 3-Card Authentication Gateway
    ("Public Citizen Access", "Citizen Access"),
    ("Apply for welfare schemes, check eligibility, track application status, download PDF acknowledgement receipts, and update registry profile.",
     "Apply for welfare schemes, check eligibility, track applications, and download receipts."),
    ("Register as New Citizen", "Register as Citizen"),
    ("Citizen registration is completely free & open to all Karnataka residents.",
     "Open to all residents of Karnataka."),
    ("Official Department Scrutiny Desk", "Welfare Officers"),
    ("Category-wise and scheme-wise application scrutiny, verification desk, eligibility approval/rejection decisions, and DBT sanctioning.",
     "Review applications, verify documents, request information, and sanction welfare benefits."),
    ("Central System Governance Command", "Platform Super-Admin"),
    ("Full platform administration: user account management, role assignments, category and dynamic form definitions, and system security audit trail.",
     "User management, role assignments, category configuration, and security audit logs."),
    ("Highest administrative privilege level for NagrikSetu SWD.",
     "Super-admin governance for NagrikSetu SWD."),
    ("Officer Account:", "Officer:"),
    ("Super-Admin Account:", "Super-Admin:"),
    ("Sign In as Citizen", "Sign In"),
    ("Sign In as Welfare Admin", "Sign In"),
    ("Sign In as Platform Admin", "Sign In"),
    ("Welfare Officer Login &rarr;", "Welfare Officer Login"),
    ("Platform Admin Login &rarr;", "Platform Admin Login"),
    ("Citizen Welfare Account Registration", "Citizen Registration"),
    ("Register for the NagrikSetu Social Welfare Department (SWD) Portal to apply for welfare schemes, track DBT disbursements, and maintain your citizen registry profile.",
     "Create your citizen account to apply for schemes and track benefits."),
    ("1. Mandatory Account Credentials", "1. Account Credentials"),
    ("2. Residential Location Details (Karnataka)", "2. Residential Details"),
    ("3. Socio-Economic Background (Indicative)", "3. Socio-Economic Details"),
    ("4. Security & Compliance Acknowledgment", "4. Confirmation"),
    ("Your citizen registration automatically assigns the default <strong>CITIZEN</strong> role. Administrative roles are never assignable through public registration. All passwords are encrypted with strong cryptographic hashing (bcrypt/PBKDF2).",
     "Citizen accounts are secured with strong cryptographic password encryption. Official administrative roles cannot be created via public registration."),
     
    # Scheme Catalogue
    ("Karnataka Social Welfare Scheme Catalogue", "Scheme Catalogue"),
    ("Explore official government welfare programs, eligibility rules, and benefit structures.",
     "Explore government welfare schemes, rules, and benefits."),
    ("Launch Eligibility Checker &rarr;", "Eligibility Checker"),
    ("Search schemes by name, keyword, or department...", "Search schemes..."),
    ("Check Eligibility &rarr;", "Check Eligibility"),
    ("Apply Now &rarr;", "Apply Now"),
    
    # Eligibility Checker View
    ("SWD Preliminary Eligibility Assessment Engine", "Eligibility Assessment"),
    ("Assess your preliminary eligibility against official government criteria before submitting an application.",
     "Check preliminary eligibility against official criteria before applying."),
    ("Applicant Profile Input", "Your Profile"),
    ("Assess Eligibility Now", "Check Eligibility"),
    ("Detailed Rule Evaluation Breakdown", "Rule Evaluation Breakdown"),
    ("Proceed to Application Form &rarr;", "Apply for Scheme &rarr;"),
    
    # Application Form
    ("Apply for Welfare Scheme:", "Apply:"),
    ("Step 1: Scheme Guidelines & Benefit Summary", "1. Scheme Guidelines"),
    ("Step 2: Basic Applicant Demographics", "2. Applicant Information"),
    ("Step 3: Scheme-Specific Specialized Questions", "3. Scheme Details"),
    ("Step 4: Bank Account Details for DBT Payment", "4. Bank Account for DBT"),
    ("Step 5: Official Declaration & Consent", "5. Declaration & Consent"),
    ("Submit Application Dossier &rarr;", "Submit Application"),
    
    # Application Tracking
    ("Upload Supplementary Document to Dossier", "Upload Document"),
    ("Audit Trail & Lifecycle History", "Application History"),
    ("Upload Supplementary Document", "Upload Document"),
    ("Upload valid PDF or image file (max 5MB). Extensions: PDF, JPG, JPEG, PNG.",
     "Max file size: 5 MB (PDF, JPG, PNG)."),
     
    # Admin Views in App.tsx
    ("Social Welfare Department Administrative Command Center", "Admin Command Center"),
    ("Real-time scheme statistics and application processing workflows.",
     "Scheme metrics and application review workflows."),
    ("Review Application Queue", "Review Queue"),
    ("Beneficiary Registry", "Beneficiaries"),
    ("Manage Schemes", "Schemes"),
    ("SWD Application Review Queue", "Application Review Queue"),
    ("State Welfare Beneficiary Ledger", "Beneficiary Ledger"),
    ("Permanent records of authorized grant sanctions and Aadhaar DBT credits.",
     "Approved beneficiaries and DBT records."),
    ("Simulated Direct Benefit Transfer (DBT) Console", "DBT Console"),
    ("Individual and atomic batch disbursements with duplicate payment prevention.",
     "Simulated batch disbursements with duplicate payment checks."),
    ("Download DBT Report (CSV)", "Download CSV Report"),
    ("Find Nearby Welfare Centres", "Welfare Centres"),
    ("Find verified Social Welfare Department Welfare Centres within 25 km of your current location.",
     "Find Social Welfare Department centres within 25 km."),
    ("Search Constraint: <strong style={{ color: '#0f172a' }}>Strict 25 km Haversine Radius</strong>",
     "Radius: <strong style={{ color: '#0f172a' }}>25 km</strong>"),
    ("Citizen Grievance & Welfare Helpdesk", "Grievance Helpdesk"),
    ("Register complaints, request verification escalations, and track redressal by Social Welfare Officers.",
     "Submit complaints and track resolution by welfare officers."),
     
    # Footer
    ("Social Welfare Department (SWD) &bull; NagrikSetu Platform", "Social Welfare Department &bull; NagrikSetu"),
    ("Standalone Department Microservice developed for the NagrikSetu Platform. Responsible for social security pensions, post-matric scholarships, Divyangjan assistance, and Direct Benefit Transfer (DBT) welfare governance.",
     "Official social welfare and Direct Benefit Transfer portal for Karnataka."),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Replaced ({count}): {old[:40]} -> {new[:40]}")
    else:
        print(f"NOT FOUND: {old[:40]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Updated App.tsx with {count} replacements.")
