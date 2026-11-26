import pymysql
import hashlib

def hash_pw(pw: str) -> str:
    return hashlib.sha256((pw + "nagriksetu_salt").encode('utf-8')).hexdigest()

conn = pymysql.connect(host='127.0.0.1', port=3308, user='swd_app', password='swd-secure-pass-2026', database='nagriksetu_swd')
cur = conn.cursor()

# 1. Seed Users
users = [
    ("CIT-KA-9901", "citizen@example.com", hash_pw("CitizenPass@2026"), "Ramesh Kumar Nayak", "CITIZEN", "9845012345", "Bengaluru Urban", "Karnataka", 180000.0, "SC", 0.0, "SBIN0040123991", "SBIN0040123"),
    ("OFF-SWD-501", "officer@nagriksetu.local", hash_pw("OfficerPass@2026"), "S. R. Patil (District Welfare Officer)", "WELFARE_OFFICER", "9845077777", "Bengaluru Urban", "Karnataka", 0.0, "General", 0.0, None, None),
    ("ADM-SWD-001", "admin@nagriksetu.local", hash_pw("AdminPass@2026"), "SWD Welfare Administrator", "ADMINISTRATOR", "9845099999", "State Directorate", "Karnataka", 0.0, "General", 0.0, None, None)
]

for u in users:
    cur.execute("SELECT id FROM users WHERE email=%s", (u[1],))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (citizen_id, email, password_hash, full_name, role, phone, district, state, annual_income, caste_category, disability_percentage, bank_account_number, bank_ifsc, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, NOW(), NOW())
        """, u)

# 2. Seed Scheme Categories (English only)
categories = [
    (1, "SCHOLARSHIPS", "Education & Scholarships", "Pre-matric and post-matric financial incentives and fee exemptions for students from scheduled castes, tribes, and backward classes.", "BookOpen"),
    (2, "DIVYANGJAN", "Disability & Divyangjan Welfare", "Monthly maintenance assistance, rehabilitation aid, and specialized prosthetic equipment for persons with benchmark disabilities.", "Shield"),
    (3, "SOCIAL_SECURITY", "Social Security & Senior Citizen Pension", "Monthly direct benefit transfer pensions for destitute senior citizens, widows, and vulnerable rural workers.", "Users"),
    (4, "HARMONY_INCENTIVES", "Social Integration & Harmony Grants", "Financial grants and wedding incentive endowments promoting social harmony and inter-caste marriages.", "HeartHandshake")
]

for c in categories:
    cur.execute("SELECT id FROM scheme_categories WHERE id=%s", (c[0],))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO scheme_categories (id, code, name, description, icon, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, 1, NOW(), NOW())
        """, c)

# 3. Seed Schemes (English only)
schemes = [
    (
        1, "KAR-SSP-POSTMATRIC", "Post-Matric Scholarship for SC/ST and Backward Classes Students", 1,
        "Social Welfare Department, Government of Karnataka", "State Scholarship Directorate",
        "Comprehensive educational scholarship providing 100% course fee reimbursement and monthly maintenance allowances for students pursuing higher education.",
        "100% Course Fee Reimbursement + INR 1,200 to INR 3,500 Monthly Allowance directly credited via Aadhaar Bridge.",
        "SCHOLARSHIP", 25000.0,
        "Resident of Karnataka; Family annual income <= INR 2,50,000 for SC/ST or <= INR 1,00,000 for OBC; Enrolled in recognized university or college.",
        "Apply online with college bonafide certificate, verified revenue income certificate, and Aadhaar-seeded bank account.",
        "https://sw.karnataka.gov.in/schemes/postmatric", "2026-01-01", "2026-12-31", "PUBLISHED"
    ),
    (
        2, "KAR-DIVYANGJAN-PENSION", "Disability Maintenance & Assistive Aid Grant", 2,
        "Social Welfare Department, Government of Karnataka", "Directorate for Empowerment of Differently Abled",
        "Monthly pension and financial aid for citizens with physical or sensory disabilities ensuring dignified livelihood and social protection.",
        "INR 2,000 per month direct credit to bank account plus free assistive aids and mobility equipment.",
        "DIRECT_BENEFIT_TRANSFER", 24000.0,
        "Permanent resident of Karnataka; Certified disability percentage of 40% or above from authorized medical board; Family income <= INR 1,50,000.",
        "Upload Unique Disability ID (UDID) certificate, Aadhaar card, and residential proof.",
        "https://sw.karnataka.gov.in/schemes/disability", "2026-01-01", "2026-12-31", "PUBLISHED"
    ),
    (
        3, "KAR-SANDHYA-SURAKSHA", "Sandhya Suraksha Senior Citizen Pension Scheme", 3,
        "Social Welfare Department, Government of Karnataka", "Social Security and Pensions Directorate",
        "Social safety net pension for destitute senior citizens, agricultural laborers, and unorganized sector workers.",
        "INR 1,200 per month direct benefit credit plus concessional state bus transport pass.",
        "DIRECT_BENEFIT_TRANSFER", 14400.0,
        "Age 65 years or above; Resident of Karnataka for at least 3 years; Combined family income <= INR 32,000 per year.",
        "Submit age verification certificate, domicile certificate, and bank account details.",
        "https://sw.karnataka.gov.in/schemes/sandhya-suraksha", "2026-01-01", "2026-12-31", "PUBLISHED"
    ),
    (
        4, "KAR-INTERCASTE-MARRIAGE", "Financial Incentive Scheme for Inter-Caste Marriages", 4,
        "Social Welfare Department, Government of Karnataka", "Social Welfare Directorate",
        "One-time financial grant offered to newly wed couples where one spouse belongs to Scheduled Castes to foster social inclusion.",
        "INR 2,50,000 incentive (INR 1,00,000 upfront cash transfer via DBT and INR 1,50,000 in government fixed deposit bonds).",
        "FINANCIAL_ASSISTANCE", 250000.0,
        "Either bride or groom must belong to Scheduled Caste; Marriage registered under Hindu Marriage Act; Annual income <= INR 5,00,000.",
        "Submit registered marriage certificate, caste certificate of both partners, and joint bank account details.",
        "https://sw.karnataka.gov.in/schemes/harmony", "2026-01-01", "2026-12-31", "PUBLISHED"
    )
]

for s in schemes:
    cur.execute("SELECT id FROM schemes WHERE id=%s", (s[0],))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO schemes (id, scheme_code, name, category_id, department, administering_authority, description, benefit_summary, benefit_type, benefit_amount, eligibility_summary, application_instructions, official_url, application_start_date, application_end_date, status, is_duplicate_check_enabled, created_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 'SYSTEM_ADMIN', NOW(), NOW())
        """, s)

# 4. Seed Eligibility Rules
rules = [
    # Scheme 1: Post-Matric
    (1, "residence_state", "EQUALS", "Karnataka", "STRING", 1, "Permanent resident of Karnataka state"),
    (1, "annual_income", "LESS_THAN_OR_EQUAL", "250000", "FLOAT", 1, "Annual family income must not exceed INR 2,50,000"),
    (1, "caste_category", "IN", "SC,ST,OBC,Cat-1,2A,2B,3A,3B", "LIST", 1, "Must belong to SC, ST or recognized backward social category"),
    (1, "education_level", "IN", "Post-Matric,Undergraduate,Postgraduate,Diploma,Professional", "LIST", 1, "Enrolled in post-matric or higher education degree"),

    # Scheme 2: Disability Pension
    (2, "residence_state", "EQUALS", "Karnataka", "STRING", 1, "Permanent resident of Karnataka"),
    (2, "disability_percentage", "GREATER_THAN_OR_EQUAL", "40", "FLOAT", 1, "Disability percentage must be 40% or higher"),
    (2, "annual_income", "LESS_THAN_OR_EQUAL", "150000", "FLOAT", 1, "Annual family income must not exceed INR 1,50,000"),

    # Scheme 3: Sandhya Suraksha
    (3, "residence_state", "EQUALS", "Karnataka", "STRING", 1, "Resident of Karnataka for at least 3 years"),
    (3, "age", "GREATER_THAN_OR_EQUAL", "65", "INTEGER", 1, "Applicant age must be 65 years or above"),
    (3, "annual_income", "LESS_THAN_OR_EQUAL", "32000", "FLOAT", 1, "Combined household income must not exceed INR 32,000 per annum")
]

for r in rules:
    cur.execute("SELECT id FROM eligibility_rules WHERE scheme_id=%s AND field_name=%s", (r[0], r[1]))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO eligibility_rules (scheme_id, field_name, operator, expected_value, value_type, is_mandatory, description, rule_version, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 1, NOW(), NOW())
        """, r)

# 5. Seed Demo Applications & Beneficiaries
cur.execute("SELECT id FROM scheme_applications WHERE citizen_id='CIT-KA-9901'")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO scheme_applications (id, application_number, scheme_id, citizen_id, citizen_name, citizen_email, citizen_phone, annual_income, caste_category, residence_district, disability_percentage, bank_account_number, bank_ifsc, status, is_duplicate_suspect, admin_remarks, created_at, updated_at)
        VALUES (1, 'SWD-APP-2026-99A101', 1, 'CIT-KA-9901', 'Ramesh Kumar Nayak', 'citizen@example.com', '9845012345', 180000.0, 'SC', 'Bengaluru Urban', 0.0, 'SBIN0040123991', 'SBIN0040123', 'APPROVED', 0, 'Dossier verified and approved by District Welfare Officer.', NOW(), NOW())
    """)
    cur.execute("""
        INSERT INTO application_history (application_id, from_status, to_status, changed_by, action_type, remarks, created_at)
        VALUES (1, 'SUBMITTED', 'APPROVED', 'S. R. Patil (District Welfare Officer)', 'OFFICER_DECISION', 'Verified revenue income certificate and college enrollment bonafide.', NOW())
    """)
    cur.execute("""
        INSERT INTO beneficiaries (id, beneficiary_code, application_id, scheme_id, citizen_id, citizen_name, sanctioned_amount, disbursement_mode, status, sanctioned_by, sanctioned_at)
        VALUES (1, 'BEN-2026-SWD-4412', 1, 1, 'CIT-KA-9901', 'Ramesh Kumar Nayak', 25000.0, 'DIRECT_BENEFIT_TRANSFER', 'ACTIVE', 'S. R. Patil (District Welfare Officer)', NOW())
    """)
    cur.execute("""
        INSERT INTO dbt_transactions (id, transaction_reference, beneficiary_id, scheme_id, amount, payment_mode, status, bank_account_last4, ifsc_code, processed_at, remarks)
        VALUES (1, 'DBT-SWD-2026-A101B2', 1, 1, 25000.0, 'AADHAAR_BRIDGE_PAYMENT', 'SUCCESSFUL', '3991', 'SBIN0040123', NOW(), 'Academic Scholarship DBT Sanction Credit')
    """)

# 6. Seed Grievances
cur.execute("SELECT id FROM grievances WHERE citizen_id='CIT-KA-9901'")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO grievances (grievance_number, citizen_id, citizen_name, category, subject, description, status, officer_response, resolved_by, resolved_at, created_at, updated_at)
        VALUES ('GRV-SWD-2026-001', 'CIT-KA-9901', 'Ramesh Kumar Nayak', 'SCHOLARSHIP_DISBURSEMENT', 'Inquiry on Maintenance Allowance Credit Date', 'Kindly inform the expected date for the disbursement of the hostel maintenance allowance for the current term.', 'RESOLVED', 'The DBT payment has been successfully queued and credited to your Aadhaar-linked State Bank account.', 'S. R. Patil (District Welfare Officer)', NOW(), NOW(), NOW())
    """)

# 7. Seed Notifications
cur.execute("SELECT id FROM notifications WHERE user_id='CIT-KA-9901'")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO notifications (user_id, title, message, is_read, notification_type, created_at)
        VALUES ('CIT-KA-9901', 'Application Approved', 'Your Post-Matric Scholarship dossier SWD-APP-2026-99A101 has been approved and INR 25,000 DBT sanctioned.', 0, 'SUCCESS', NOW())
    """)

conn.commit()
conn.close()
print("Seeding completed successfully into nagriksetu_swd!")
