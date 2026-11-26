import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

TARGET_PATH = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\FINAL_REPORTS\02_Functional_Requirements.docx"

doc = Document()

# Set A4 margins
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.different_first_page_header_footer = True
    
    # Header for later pages
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("NagrikSetu SWD — Functional Requirements | Project Report")
    hrun.font.name = "Arial"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)
    
    # Footer for later pages
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    frun1 = fp.add_run("Department of Social Welfare, Government of Karnataka\t\tPage ")
    frun1.font.name = "Arial"
    frun1.font.size = Pt(8.5)
    frun1.font.color.rgb = RGBColor(100, 116, 139)
    
    fldSimple1 = OxmlElement('w:fldSimple')
    fldSimple1.set(qn('w:instr'), 'PAGE')
    fp._p.append(fldSimple1)
    
    frun2 = fp.add_run(" of ")
    frun2.font.name = "Arial"
    frun2.font.size = Pt(8.5)
    frun2.font.color.rgb = RGBColor(100, 116, 139)
    
    fldSimple2 = OxmlElement('w:fldSimple')
    fldSimple2.set(qn('w:instr'), 'NUMPAGES')
    fp._p.append(fldSimple2)

navy = RGBColor(15, 36, 68)
slate = RGBColor(71, 85, 105)
charcoal = RGBColor(30, 41, 59)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = navy
    return p

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.italic = True
    run.font.color.rgb = slate
    return p

def add_heading1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = navy
    return p

def add_heading2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = slate
    return p

def add_body(text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.color.rgb = charcoal
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_bold = p.add_run(bold_prefix)
    r_bold.font.name = "Arial"
    r_bold.font.size = Pt(10.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = navy
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = charcoal
    return p

# ----------------- COVER PAGE -----------------
add_title("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)\nFUNCTIONAL REQUIREMENTS SPECIFICATION")
add_subtitle("Software Requirements Specification (SRS), User Role Specifications & Rule Traceability Matrix")

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.space_before = Pt(72)
p_meta.paragraph_format.space_after = Pt(12)
r_meta = p_meta.add_run(
    "Academic Project Report\n"
    "B.Tech in Computer Science & Engineering / Information Science\n"
    "Second Year Capstone / Systems Engineering Project\n\n"
    "Department of Social Welfare (SWD), Government of Karnataka\n"
    "Academic Year: 2025 – 2026\n"
    "Submission Status: Verified Final Submission"
)
r_meta.font.name = "Arial"
r_meta.font.size = Pt(11)
r_meta.font.color.rgb = slate

doc.add_page_break()

# ----------------- TABLE OF CONTENTS -----------------
add_heading1("Table of Contents")

toc_items = [
    ("1. Introduction to Requirements Specification", "Section 1"),
    ("2. System Users and Role Hierarchy", "Section 2"),
    ("3. Core Functional Requirements (FR-01 to FR-12)", "Section 3"),
    ("4. Detailed Workflow Scenarios & Edge Cases", "Section 4"),
    ("5. Practical Project Test Evidence (Sample Test Scenarios)", "Section 5"),
    ("6. Rule Traceability and Scheme Matching Matrix", "Section 6"),
    ("7. Verification of Mandatory Questions and Flags", "Section 7"),
    ("8. Non-Functional Requirements & Security Rules", "Section 8"),
    ("9. Requirement Traceability Summary & Verification", "Section 9"),
    ("10. Conclusion and Academic Sign-Off", "Section 10"),
]

table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
hdr_cells = table.rows[0].cells
hdr_cells[0].width = Inches(5.0)
hdr_cells[1].width = Inches(1.2)
hdr_cells[0].text = "Requirements Section"
hdr_cells[1].text = "Reference"
for cell in hdr_cells:
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F2444"/>')
    cell._tc.get_or_add_tcPr().append(shd)
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.name = "Arial"
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)

for title, pg in toc_items:
    row_cells = table.add_row().cells
    row_cells[0].width = Inches(5.0)
    row_cells[1].width = Inches(1.2)
    row_cells[0].text = title
    row_cells[1].text = pg
    for cell in row_cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9.5)
                run.font.color.rgb = charcoal

doc.add_page_break()

# ----------------- SECTION 1 & 2 -----------------
add_heading1("1. Introduction to Requirements Specification")
add_body(
    "This Software Requirements Specification (SRS) describes in clear and complete detail what the NagrikSetu "
    "Social Welfare Department (SWD) system must do. It defines the actions that citizens, welfare officers, and system "
    "administrators can perform, how data flows between the user interface and the database, and the exact rules used to "
    "approve or reject welfare applications."
)
add_body(
    "In software engineering, functional requirements define the specific behaviors and features of a software system. "
    "For NagrikSetu SWD, these requirements ensure that every state welfare scheme is delivered fairly, accurately, "
    "and without human bias. Every requirement described in this document has been fully implemented in the backend Python "
    "APIs and verified on the React web portal."
)

add_heading1("2. System Users and Role Hierarchy")
add_body(
    "The NagrikSetu system models four distinct user roles, each protected by strict backend Role-Based Access Control (RBAC):"
)
add_bullet("1. Public Citizen (Actor: CITIZEN): ", "Any resident of Karnataka. A citizen can register an account, search schemes, check eligibility, submit applications, upload PDF documents, track application progress, and download official PDF acknowledgement receipts.")
add_bullet("2. Government Welfare Officer (Actor: GOVERNMENT_WELFARE_ADMIN / WELFARE_OFFICER): ", "Authorized department officers at taluk and district welfare offices. Officers can view the pending scrutiny queue, inspect applicant marksheets and certificates, change application status to UNDER_REVIEW, request missing information, and formally approve or reject applications.")
add_bullet("3. Platform Administrator (Actor: PLATFORM_ADMIN / SWD_ADMIN): ", "State-level system administrators. They oversee the complete user directory (39 registered accounts), manage scheme taxonomy (35 schemes in MySQL), inspect system health, and review immutable security audit logs.")
add_bullet("4. Automated System Engine (Actor: SYSTEM): ", "Background software services that generate unique application numbers, calculate eligibility rules in memory, and generate PDF receipts.")

# ----------------- SECTION 3 -----------------
add_heading1("3. Core Functional Requirements (FR-01 to FR-12)")
add_body(
    "The system implements 12 primary functional requirements. Each requirement has a clear purpose and verifiable outcome:"
)

add_bullet("FR-01 [Citizen Registration & Identity Management]: ", "The system shall allow citizens to create an account by providing their full name, email address, mobile phone number, and a secure password. The system must hash passwords using bcrypt before saving to MySQL and assign a unique citizen identifier.")

add_bullet("FR-02 [Secure Token Authentication & Role Guards]: ", "The system shall authenticate users via OAuth2 Password Bearer login (`POST /api/swd/auth/login`). Upon successful password verification, it issues a signed JSON Web Token (JWT) containing the user's ID, role, and expiration time. Backend endpoints must enforce role restrictions and reject unauthorized access with HTTP 403 Forbidden.")

add_bullet("FR-03 [Scheme Catalogue Management & Exclusions]: ", "The system shall maintain 35 scheme records in the MySQL database and publish 28 active welfare schemes through the public API (`GET /api/swd/schemes`). It shall enforce official policy exclusions (such as excluding Shakti free bus travel, which does not involve direct cash transfer) while preserving all records safely in the database.")

add_bullet("FR-04 [Smart Scheme Finder]: ", "The system shall provide an interactive search tool where citizens enter demographic attributes (age, district, taluk, gender, social category, annual income, occupation, and education). The finder must evaluate all matching schemes and return verified potential matches while eliminating false positives.")

add_bullet("FR-05 [Deterministic Rule-Based Eligibility Engine]: ", "The system shall evaluate citizen attributes against scheme-specific rules stored in MySQL (`eligibility_rules` table). It must support operators such as EQUALS, LESS_THAN_OR_EQUAL, and GREATER_THAN_OR_EQUAL. It must return SATISFIED, UNMET, or UNKNOWN and clearly list mandatory failed conditions.")

add_bullet("FR-06 [Dynamic Conditional Scheme Questions]: ", "When an applicant selects a scheme, the application form and eligibility checker must dynamically render scheme-specific mandatory questions (such as asking for domestic electricity connection status for Gruha Jyothi, or institutional delivery for Madilu Kit).")

add_bullet("FR-07 [Online Application Dossier Submission]: ", "The system shall allow authenticated citizens to submit online applications (`POST /api/swd/schemes/{scheme_id}/applications`). It must validate all required fields (Aadhaar, income, bank account, IFSC code), assign a permanent application number, set status to SUBMITTED, and save the record in MySQL.")

add_bullet("FR-08 [Secure Digital Document Upload & Storage]: ", "The system shall accept supporting document uploads (marksheets, income certificates, caste certificates) in PDF, PNG, or JPEG formats. It must enforce a 5 MB maximum file size limit, sanitize filenames, store files on disk, and link metadata to the application.")

add_bullet("FR-09 [Pure-Python PDF Receipt Generation]: ", "The system shall dynamically generate an official PDF 1.4 acknowledgement receipt (`GET /api/swd/applications/{application_id}/receipt`) with zero external binary dependencies. The receipt must display the Karnataka state seal header, application number, applicant name, scheme title, submission timestamp, and verification watermark.")

add_bullet("FR-10 [Administrative Scrutiny & Status Transition]: ", "The system shall provide authorized welfare officers with an administrative scrutiny dashboard (`GET /api/swd/admin/applications`). Officers can inspect uploaded marksheets and transition status from SUBMITTED to UNDER_REVIEW, AWAITING_DOCUMENTS, APPROVED, or REJECTED with mandatory remarks.")

add_bullet("FR-11 [Public & Authenticated Status Tracking]: ", "The system shall provide both a public status lookup endpoint (`GET /api/swd/public/track-status/{application_number}`) and an authenticated citizen tracking timeline. Citizens can see real-time updates and officer remarks without visiting physical offices.")

add_bullet("FR-12 [Citizen Grievance Submission & Resolution]: ", "The system shall allow citizens to log grievance tickets regarding DBT delays or portal issues. Welfare officers can review tickets, write formal replies, and mark them as RESOLVED.")

# ----------------- SECTION 4 & 5 -----------------
add_heading1("4. Detailed Workflow Scenarios & Edge Cases")
add_body(
    "To ensure high reliability, the system handles several practical edge cases and boundary conditions:"
)
add_bullet("• Duplicate Application Prevention: ", "If duplicate check is enabled for a scheme, the backend checks whether the citizen already has an active application for that scheme in the same financial year. If found, it flags the record to prevent duplicate benefit claims.")
add_bullet("• Income & Age Boundary Testing: ", "For Sandhya Suraksha Pension, the income ceiling is ₹32,000 per year and minimum age is 65. If an applicant earns ₹32,001 or is 64 years and 11 months old, the eligibility engine strictly marks the criterion UNMET and rejects the application.")
add_bullet("• Gender & Relationship Validation: ", "Schemes like Gruha Lakshmi and Udyogini are exclusively for women. The engine performs bidirectional normalization between gender ('Female') and the boolean flag `is_woman=True` to prevent incorrect rejections.")
add_bullet("• Missing Information Handling: ", "If an applicant leaves a mandatory question unanswered, the engine returns INSUFFICIENT_INFORMATION rather than incorrectly marking them eligible or not eligible.")

add_heading1("5. Practical Project Test Evidence (Sample Test Scenarios)")
add_body(
    "During our final verification audit, all functional requirements were verified against actual project test records:"
)
add_heading2("Test Case 1: Citizen A — Administrative Scrutiny & Status Lifecycle")
add_body(
    "Profile: Citizen A (Registered resident of Bengaluru Urban)\n"
    "Target Scheme: Thayi Bhagya & Prasoothi Araike Scheme\n"
    "Initial Status: SUBMITTED (Assigned permanent unique reference)\n"
    "Scrutiny Transition: Status moved to UNDER_REVIEW by Welfare Officer Patil.\n"
    "Officer Scrutiny Notes: 'Not satisfied with the provided documents, please provide all the relevant documents'\n"
    "Supporting Document: Academic / educational marksheet PDF attached and inspected via the Welfare Admin dashboard.\n"
    "Outcome: Verified that the application dossier persists correctly in MySQL, is fully visible to the authorized officer, and immediately reflects status updates on the citizen portal."
)
add_heading2("Test Case 2: Citizen B — Smart Scheme Finder & Eligibility Validation")
add_body(
    "Profile: Citizen B (Age: 28, District: Bengaluru Urban, Taluk: Bengaluru South, Gender: Male, Category: General, Income: ₹180,000, Occupation: Student)\n"
    "Test Action: Profile entered into the Smart Scheme Finder.\n"
    "Engine Result: Potential Matches: 0; Check Requirements: 4; Excluded / Not Matched: 24.\n"
    "Outcome: Confirmed zero false positives. Schemes requiring SC/ST category, low income (<= ₹32,000), or female gender were strictly excluded, validating rule accuracy."
)

# ----------------- SECTION 6, 7 & 8 -----------------
add_heading1("6. Rule Traceability and Scheme Matching Matrix")
add_body(
    "The table below illustrates how the backend rule engine evaluates key Karnataka welfare schemes against citizen attributes:"
)

scheme_table = doc.add_table(rows=1, cols=4)
scheme_table.alignment = WD_TABLE_ALIGNMENT.CENTER
st_hdrs = scheme_table.rows[0].cells
st_hdrs[0].width = Inches(2.2)
st_hdrs[1].width = Inches(1.5)
st_hdrs[2].width = Inches(1.5)
st_hdrs[3].width = Inches(1.0)
st_hdrs[0].text = "Scheme Name"
st_hdrs[1].text = "Mandatory Rules"
st_hdrs[2].text = "Required Inputs"
st_hdrs[3].text = "Benefit"
for cell in st_hdrs:
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F2444"/>')
    cell._tc.get_or_add_tcPr().append(shd)
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.name = "Arial"
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

st_data = [
    ("Gruha Lakshmi Scheme", "Gender=Female, Head of Family", "Ration Card, Bank Passbook", "₹2,000 / mo"),
    ("Gruha Jyothi Scheme", "Karnataka Resident, Domestic Meter", "Avg consumption <= 200 units", "Free Power"),
    ("Sandhya Suraksha Pension", "Age >= 65, Income <= ₹32,000", "Age Proof, Income Certificate", "₹1,200 / mo"),
    ("Inter-Caste Marriage Incentive", "One spouse SC, State Resident", "Marriage Cert, Caste Cert", "₹2.50 Lakh"),
    ("Free Laptop for Students", "Enrolled in Degree/Engg, SC/ST/OBC", "College Registration, Marksheet", "Free Laptop"),
    ("Madilu Kit Scheme", "Institutional Delivery in Govt Hospital", "Delivery Certificate, Domicile", "Postnatal Kit"),
]

for name, rules, inputs, bft in st_data:
    row = scheme_table.add_row().cells
    row[0].width = Inches(2.2)
    row[1].width = Inches(1.5)
    row[2].width = Inches(1.5)
    row[3].width = Inches(1.0)
    row[0].text = name
    row[1].text = rules
    row[2].text = inputs
    row[3].text = bft
    for cell in row:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9)
                run.font.color.rgb = charcoal

add_heading1("7. Verification of Mandatory Questions and Flags")
add_body(
    "To eliminate incorrect eligibility classifications, our team audited and verified five scheme-specific dynamic questions:"
)
add_bullet("1. Gruha Jyothi: ", "The system dynamically displays: 'Domestic Electricity Connection (Avg <= 200 units/month)? *'. If the user selects 'No / Commercial / Over 200 units', the scheme is immediately classified as NOT ELIGIBLE.")
add_bullet("2. Inter-Caste Marriage Scheme: ", "The system dynamically displays: 'Does either spouse belong to Scheduled Caste (SC)? *'. If 'No' is selected, the applicant is marked NOT ELIGIBLE because SC inter-caste status is legally mandatory.")
add_bullet("3. Madilu Kit: ", "The system asks whether childbirth occurred in a recognized public healthcare institution (`institutional_delivery`). Without a confirmed 'Yes', the application cannot proceed.")
add_bullet("4. Anna Bhagya: ", "The system verifies whether the family holds a valid BPL or Antyodaya Anna Yojana (AAY) ration card.")
add_bullet("5. Yeshasvini Health Insurance: ", "The system verifies whether the rural applicant is a registered member of a cooperative society.")

add_heading1("8. Non-Functional Requirements & Security Rules")
add_body(
    "In addition to functional features, NagrikSetu SWD enforces critical non-functional software standards:"
)
add_bullet("• High Performance & Low Latency: ", "FastAPI asynchronous endpoints respond in under 150 milliseconds for catalogue searches and eligibility evaluations.")
add_bullet("• Strict RBAC Enforcement: ", "If a citizen attempts to call an admin endpoint (e.g., `GET /api/swd/admin/dashboard`), the backend immediately rejects the request with HTTP 403 Forbidden.")
add_bullet("• Tamper-Proof Audit Logging: ", "Every administrative status change, document download, and decision is written to MySQL table `audit_logs` with actor ID, timestamp, and client IP address.")
add_bullet("• Data Integrity: ", "Foreign key constraints between `schemes`, `scheme_applications`, `uploaded_documents`, and `application_history` prevent orphaned records.")

# ----------------- SECTION 9 & 10 -----------------
add_heading1("9. Requirement Traceability Summary & Verification")
add_body(
    "Every requirement from FR-01 to FR-12 has been mapped to its implementation code and verified with automated test suites:"
)
add_bullet("• Automated Test Suite 1 (`test_8_schemes_eligibility.py`): ", "Executed 24 / 24 test cases covering 8 major schemes across Satisfied, Failed Mandatory, and Missing Mandatory scenarios (100% PASS).")
add_bullet("• Automated Test Suite 2 (`test_mahesh_current.py`): ", "Executed demographic evaluation for Student profile (Male, General, Student) -> 0 Potential Matches, 0 False Positives (100% PASS).")
add_bullet("• End-to-End System Test Suite (`run_project_functional_tests.py`): ", "Executed 12 / 12 functional test cases verifying token issuance, application submission, document upload, scrutiny transitions, and PDF receipt rendering (100% PASS).")

add_heading1("10. Conclusion and Academic Sign-Off")
add_body(
    "The Functional Requirements Specification for NagrikSetu SWD represents a complete, professional, and rigorous "
    "engineering specification. All functional requirements have been designed, coded, tested, and demonstrated in the live "
    "software environment. The platform satisfies all academic criteria for second-year B.Tech software architecture and "
    "is certified ready for presentation."
)

doc.save(TARGET_PATH)
print("Successfully generated 02_Functional_Requirements.docx at:", TARGET_PATH)
