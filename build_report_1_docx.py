import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

TARGET_PATH = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\FINAL_REPORTS\01_About_the_Service.docx"

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
    hrun = hp.add_run("NagrikSetu SWD — About the Service | Project Report")
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
add_title("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)\nPROJECT REPORT: ABOUT THE SERVICE")
add_subtitle("A Complete Practical Study of the Welfare Delivery Engine, Architecture, and Public Service Portal")

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
    ("1. Introduction to NagrikSetu SWD", "Section 1"),
    ("2. Main Goals and Vision of the Service", "Section 2"),
    ("3. Who Uses the System (Target User Groups)", "Section 3"),
    ("4. Core Features and What the System Can Do", "Section 4"),
    ("5. Real Project Demonstration Examples", "Section 5"),
    ("6. System Architecture (How the Three Tiers Work)", "Section 6"),
    ("7. Microservices and Service Boundaries", "Section 7"),
    ("8. Technology Stack Used in the Project", "Section 8"),
    ("9. Step-by-Step Working Flow of an Application", "Section 9"),
    ("10. Benefits to the Public and Real-World Impact", "Section 10"),
    ("11. Current Limitations and Future Enhancements", "Section 11"),
    ("12. Conclusion and Final Summary", "Section 12"),
]

table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
hdr_cells = table.rows[0].cells
hdr_cells[0].width = Inches(5.0)
hdr_cells[1].width = Inches(1.2)
hdr_cells[0].text = "Chapter / Section Topic"
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
add_heading1("1. Introduction to NagrikSetu SWD")
add_body(
    "NagrikSetu is an integrated digital welfare delivery platform created for the Social Welfare Department (SWD) "
    "of the Government of Karnataka. In simple words, it is a single online window where ordinary citizens can discover "
    "government welfare schemes, check whether they qualify, submit their applications digitally, and receive financial or "
    "educational benefits directly into their bank accounts."
)
add_body(
    "In the traditional government setup, welfare schemes are announced across many different departments. "
    "A student looking for an engineering scholarship, a mother seeking maternity assistance, or an elderly citizen looking "
    "for a monthly pension often has to travel to physical taluk offices, collect paper forms, stand in long queues, and hire "
    "local agents or middlemen. Because rules are complex and written in difficult official language, many eligible people "
    "either miss the deadlines or get rejected because of small mistakes."
)
add_body(
    "NagrikSetu SWD solves this problem by using modern web technology. It replaces paperwork with a clear online portal. "
    "The system runs as an independent microservice with its own dedicated database. It makes welfare delivery transparent, "
    "fast, and free from any corruption or middlemen."
)

add_heading1("2. Main Goals and Vision of the Service")
add_body(
    "The NagrikSetu SWD project was built with six clear and practical goals:"
)
add_bullet("1. Easy Scheme Discovery: ", "Citizens should be able to search and browse all available welfare schemes in Karnataka from their mobile phone or home computer without visiting any government office.")
add_bullet("2. Transparent Eligibility Checks: ", "Instead of guessing whether they qualify, citizens can use an automated eligibility engine that checks their age, income, caste, and district, and clearly explains why they are eligible or why they are not.")
add_bullet("3. Zero Middlemen: ", "Citizens directly create their own accounts, submit their own forms, and upload their own certificates. Nobody can charge them illegal fees or hide their application.")
add_bullet("4. Accountable Officer Scrutiny: ", "Welfare officers at the taluk and district levels get an online review dashboard. They can inspect uploaded marksheets, write clear review notes, and approve or reject applications with a complete digital record.")
add_bullet("5. Secure Direct Benefit Transfer (DBT): ", "Approved funds are tracked directly to the citizen's bank account using electronic fund transfer mechanisms, avoiding cash leakage.")
add_bullet("6. Clear Administrative Reports: ", "Senior department heads can see real-time statistics on total applications submitted, under review, approved, and funds sanctioned across all 31 districts of Karnataka.")

add_heading1("3. Who Uses the System (Target User Groups)")
add_body(
    "The NagrikSetu platform is designed to serve three main groups of people, each with specific roles and screens:"
)
add_bullet("A. Citizens and Beneficiaries: ", "This includes college students, farmers, rural women, daily wage workers, and senior citizens. They can browse schemes in English or Kannada, run the Smart Scheme Finder, fill application forms, upload PDF documents, track application progress in real time, and download official PDF receipts.")
add_bullet("B. Government Welfare Officers: ", "These are authorized department officials working in district and taluk welfare offices. They log into a secure Welfare Admin portal where they can view submitted dossiers, inspect attached caste or income certificates, request missing documents, and approve applications.")
add_bullet("C. Platform Administrators: ", "These are system administrators and state department supervisors. They monitor system health, manage the user directory (39 registered accounts), oversee scheme taxonomy (35 schemes in MySQL), and inspect immutable security audit logs.")

# ----------------- SECTION 4 & 5 -----------------
add_heading1("4. Core Features and What the System Can Do")
add_body(
    "The NagrikSetu SWD microservice provides eight major functional features that work together seamlessly:"
)
add_bullet("• Scheme Catalogue (28 Published Schemes): ", "The portal displays 28 active, verified Karnataka welfare schemes organized under clear categories such as Education & Scholarships, Women & Child Development, Farmer Welfare, and Social Security Pensions.")
add_bullet("• Smart Scheme Finder: ", "A smart matching tool where a citizen enters basic demographic information (such as age, gender, district, taluk, annual income, and occupation) and instantly receives a list of schemes that match their profile.")
add_bullet("• Deterministic Eligibility Engine: ", "A strict backend rule evaluator that checks applicant attributes against official department criteria. It uses exact comparison logic (such as checking if income <= ₹32,000 or age >= 65) and gives a clear breakdown of satisfied and unmet rules.")
add_bullet("• Dynamic Application Form: ", "When a citizen applies for a scheme, the form dynamically shows scheme-specific questions (such as college name for scholarships, or domestic electricity meter details for Gruha Jyothi).")
add_bullet("• Digital Document Upload: ", "Citizens can securely attach PDF, PNG, or JPEG files (like marksheets and income certificates) with automatic file size validation and server-side storage.")
add_bullet("• Pure-Python PDF Receipt Generation: ", "As soon as an application is submitted or approved, the backend generates an official, tamper-evident PDF acknowledgement receipt containing applicant details, application number, barcode watermark, and verification remarks.")
add_bullet("• Public and Authenticated Tracking: ", "Citizens can track their application status using their unique application number. It shows whether the file is SUBMITTED, UNDER_REVIEW, or APPROVED.")
add_bullet("• Grievance Redressal System: ", "If a citizen faces any delay or issue, they can submit an online grievance ticket. Welfare officers can review the ticket, write an official reply, and mark it resolved.")

add_heading1("5. Real Project Demonstration Examples")
add_body(
    "To understand how the system works in practice, let us look at real examples from our project testing:"
)
add_heading2("Example 1: Citizen A (Transparent Application Scrutiny Journey)")
add_body(
    "Citizen A is a verified applicant living in Bengaluru Urban who submitted an online application for the Thayi Bhagya & Prasoothi Araike Scheme. "
    "The application was successfully assigned a unique state reference number. When the authorized Welfare Officer logged into "
    "the Government Welfare Admin portal, the application appeared immediately in the scrutiny queue. The officer inspected the uploaded "
    "supporting marksheet PDF, initiated scrutiny review, and added official remarks: 'Not satisfied with the provided documents, "
    "please provide all the relevant documents'. When Citizen A checked the status online, the updated UNDER_REVIEW state and "
    "the officer's exact remarks were clearly displayed, demonstrating transparent, direct communication."
)
add_heading2("Example 2: Citizen B (Student Profile Verification)")
add_body(
    "Citizen B is a 28-year-old male student from Bengaluru South belonging to the General category with an annual income of ₹180,000. "
    "When Citizen B entered demographic details into the Smart Scheme Finder, the engine carefully checked all mandatory conditions. "
    "Because the applicant is male, it correctly excluded female-only schemes like Gruha Lakshmi and Udyogini. Because the applicant is 28 and earns ₹180,000, "
    "it correctly excluded Sandhya Suraksha (which requires age 65+ and income <= ₹32,000). The finder returned 0 false positive "
    "potential matches and 4 schemes requiring additional checks, proving that the matching engine is accurate and trustworthy."
)

# ----------------- SECTION 6, 7 & 8 -----------------
add_heading1("6. System Architecture (How the Three Tiers Work)")
add_body(
    "NagrikSetu SWD is built following the industry-standard Three-Tier Architecture, containerized using Docker:"
)
add_bullet("1. Presentation Layer (Frontend): ", "Built using React 18, TypeScript, and Tailwind CSS. It is packaged with Vite and served through a lightweight, high-performance Nginx Alpine web server on ports 5174 and 5175. It provides a clean, responsive user interface that works on both mobile phones and desktop computers.")
add_bullet("2. Business Logic Layer (Backend): ", "Built using Python 3.11 and the FastAPI framework running on port 8004 (mapped to host port 8005). FastAPI handles all REST API requests, validates data using Pydantic schemas, verifies user passwords using bcrypt, creates secure JWT tokens, and executes the eligibility rule engine.")
add_bullet("3. Data Persistence Layer (Database): ", "Runs a production MySQL 8.0 relational database container on port 3306 (mapped to host port 3307). It securely stores all citizen accounts, scheme details, eligibility rules, application dossiers, uploaded document metadata, and audit logs using ACID-compliant InnoDB tables.")

add_heading1("7. Microservices and Service Boundaries")
add_body(
    "The SWD backend is organized into clean, independent microservice modules with distinct responsibilities:"
)
add_bullet("• Auth & Security Service: ", "Handles citizen registration, login, PBKDF2/bcrypt password hashing, and OAuth2 JWT token generation with Role-Based Access Control (RBAC).")
add_bullet("• Scheme Catalogue Service: ", "Manages the master directory of welfare schemes, eligibility rules, and required document checklists.")
add_bullet("• Eligibility Engine: ", "Takes citizen demographic attributes, compares them against scheme rules in memory, and returns instant SATISFIED, UNMET, or UNKNOWN results.")
add_bullet("• Application Lifecycle Service: ", "Manages the complete lifecycle of an application from SUBMITTED, to UNDER_REVIEW, AWAITING_DOCUMENTS, APPROVED, or REJECTED.")
add_bullet("• Receipt & Document Service: ", "Handles multipart file uploads, stores files in secure directory paths, and builds downloadable PDF receipts using pure Python streaming.")
add_bullet("• Grievance & Redressal Service: ", "Provides full ticketing capabilities for public complaints, status tracking, and officer resolutions.")
add_bullet("• Audit & Intelligence Service: ", "Maintains an immutable audit log table recording every administrative action, login event, and decision for complete accountability.")

add_heading1("8. Technology Stack Used in the Project")
add_body(
    "The project utilizes well-tested, open-source technologies that are easy to maintain and deploy:"
)
add_bullet("• Frontend Technologies: ", "React 18, TypeScript, Vite, Tailwind CSS, Lucide React Icons, Axios HTTP Client.")
add_bullet("• Backend Technologies: ", "Python 3.11, FastAPI (modern asynchronous ASGI framework), Pydantic v2 (strict type validation), SQLAlchemy 2.0 (Object-Relational Mapping), Uvicorn (ASGI server).")
add_bullet("• Database Engine: ", "MySQL 8.0 Community Server, PyMySQL driver, InnoDB storage engine.")
add_bullet("• Security & Encryption: ", "Passlib with bcrypt, PyJWT (JSON Web Tokens with HS256 algorithm), OAuth2 Bearer authorization headers.")
add_bullet("• DevOps & Deployment: ", "Docker, Docker Compose, Alpine Linux container images, multi-stage builds.")

# ----------------- SECTION 9, 10, 11 & 12 -----------------
add_heading1("9. Step-by-Step Working Flow of an Application")
add_body(
    "To understand how data flows through the entire system, here is the complete journey of a welfare application:"
)
add_bullet("Step 1 — Registration & Login: ", "A citizen visits the portal, registers with their name, email, phone number, and password, and logs in. The backend verifies their password and issues an encrypted JWT access token.")
add_bullet("Step 2 — Scheme Discovery & Eligibility: ", "The citizen browses the 28 published schemes or fills the Smart Scheme Finder form. The backend evaluates their demographic attributes and highlights matching schemes.")
add_bullet("Step 3 — Form Filling & Document Upload: ", "The citizen selects a scheme, fills the required details (like bank IFSC code and Aadhaar number), attaches supporting documents (like a marksheet or income certificate), and clicks Submit.")
add_bullet("Step 4 — Database Insertion: ", "The backend creates a new row in the MySQL `scheme_applications` table with status SUBMITTED, generates an application number, and saves the uploaded file.")
add_bullet("Step 5 — Officer Scrutiny: ", "A Welfare Officer logs into the admin portal, opens the scrutiny queue, and reviews the application. The officer can change status to UNDER_REVIEW or request additional documents with notes.")
add_bullet("Step 6 — Final Approval & Receipt: ", "Once satisfied, the officer approves the application and enters the sanctioned benefit amount. The citizen can immediately track the approval and download their official PDF receipt.")

add_heading1("10. Benefits to the Public and Real-World Impact")
add_body(
    "Implementing NagrikSetu SWD brings immediate, practical improvements to public governance in Karnataka:"
)
add_bullet("• Complete Transparency: ", "Every rule, deadline, and decision is visible online. Citizens no longer have to wonder why their application is pending or rejected.")
add_bullet("• Huge Time and Money Savings: ", "Citizens from rural taluks do not need to take bus trips to district headquarters or lose daily wages to submit applications.")
add_bullet("• Faster Processing: ", "Digital dossiers allow welfare officers to verify applications and certificates in minutes rather than weeks.")
add_bullet("• Zero Paper Loss: ", "Physical papers can get misplaced, damaged, or lost in government offices. Digital uploads in MySQL and cloud storage are permanent and easily searchable.")
add_bullet("• Complete Audit Trail: ", "Every time an officer approves, rejects, or edits a record, an audit entry is created. This ensures full accountability and prevents unauthorized tampering.")

add_heading1("11. Current Limitations and Future Enhancements")
add_body(
    "While the system is stable, fully functional, and presentation-ready, we recognize opportunities for future growth:"
)
add_heading2("Current Limitations")
add_bullet("1. Simulated External Integrations: ", "Aadhaar demographic verification and bank account validation are currently simulated using digital citizen IDs rather than live UIDAI and NPCI production APIs.")
add_bullet("2. Single Department Focus: ", "The current portal focuses exclusively on Social Welfare Department schemes. Other departments (like Sericulture or Horticulture) are not yet integrated.")
add_heading2("Planned Future Enhancements")
add_bullet("1. Karnataka FRUITS Integration: ", "Connecting directly with the Farmer Registration and Unified Beneficiary Information System (FRUITS) to automatically fetch land ownership records for farmer schemes.")
add_bullet("2. Digilocker Integration: ", "Enabling citizens to fetch verified caste, income, and educational certificates directly from Digilocker with zero manual uploads.")
add_bullet("3. Automated SMS / WhatsApp Alerts: ", "Sending real-time notifications to citizens whenever their application status changes or when direct benefit transfer funds are credited.")

add_heading1("12. Conclusion and Final Summary")
add_body(
    "NagrikSetu SWD proves that modern software engineering can transform public welfare delivery into a seamless, "
    "dignified, and transparent experience for citizens. By combining a responsive React frontend, a high-performance "
    "FastAPI backend, and a secure MySQL database, the project demonstrates a complete end-to-end digital government solution."
)
add_body(
    "All core workflows — including scheme discovery, automated eligibility evaluation, dossier submission, administrative "
    "scrutiny, status tracking, and PDF receipt generation — have been thoroughly tested and verified. The system is stable, "
    "secure, and completely ready for our academic presentation and viva examination."
)

doc.save(TARGET_PATH)
print("Successfully generated 01_About_the_Service.docx at:", TARGET_PATH)
