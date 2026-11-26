import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL\FINAL_REPORTS"
os.makedirs(BASE_DIR, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 800, "NagrikSetu SWD — Academic Project Report: Functional Requirements")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            self.line(54, 45, 541, 45)
            self.drawRightString(541, 32, f"Page {self._pageNumber} of {page_count}")
            self.drawString(54, 32, "Department of Social Welfare, Government of Karnataka")
            self.restoreState()

def create_report_2_docx():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    navy = RGBColor(15, 36, 68)
    slate = RGBColor(71, 85, 105)

    # Cover Page
    p_title_space = doc.add_paragraph()
    p_title_space.paragraph_format.space_before = Pt(72)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)\nFUNCTIONAL REQUIREMENTS SPECIFICATION")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Software Engineering SRS, Actor Specifications & Rule Traceability Matrix")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = slate

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(120)
    run_div = p_div.add_run("____________________________________________________")
    run_div.font.color.rgb = RGBColor(203, 213, 225)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("Course: B.Tech Software Engineering / Software Architecture Project\nAcademic Year: 2026\nSystem Specification Standard: IEEE 830-1998 (Adapted)\nDepartment: Social Welfare Department (SWD), Govt of Karnataka")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(11)
    run_meta.font.color.rgb = slate

    doc.add_page_break()

    # Table of Contents
    h_toc = doc.add_heading("Table of Contents", level=1)
    h_toc.style.font.color.rgb = navy
    toc_items = [
        ("1. System Actors & Role Hierarchy", "3"),
        ("2. Functional Requirements Matrix (FR-01 to FR-12)", "3"),
        ("3. Citizen User Requirements & Interactions", "4"),
        ("4. Welfare Officer & Administrative Requirements", "5"),
        ("5. API & Relational Database Requirements", "6"),
        ("6. Input Validation & Data Integrity Rules", "6"),
        ("7. Role-Based Access Control (RBAC) Specification", "7"),
        ("8. Core Use Cases & Scenario Walkthroughs", "7"),
        ("9. Formal Acceptance Criteria & Verification", "8"),
        ("10. Conclusion & Architectural Summary", "9")
    ]
    t_toc = doc.add_table(rows=1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_toc.rows[0].cells
    hdr_cells[0].text = "Requirement Section"
    hdr_cells[1].text = "Page"
    for title, pg in toc_items:
        row_cells = t_toc.add_row().cells
        row_cells[0].text = title
        row_cells[1].text = pg

    doc.add_page_break()

    # Sections
    sections_data = [
        ("1. System Actors & Role Hierarchy", [
            "The NagrikSetu SWD system models four primary system actors with clearly separated security boundaries:",
            "• Public Citizen (Actor: CITIZEN): An unregistered or registered resident of Karnataka seeking information on state welfare schemes, submitting online scheme dossiers, uploading supporting certificates, downloading acknowledgement receipts, and raising grievance tickets.",
            "• Government Welfare Officer (Actor: GOVERNMENT_WELFARE_ADMIN / WELFARE_OFFICER): District or taluk administrative officer responsible for application scrutiny. Officers review citizen dossiers, inspect attached certificates, verify eligibility, record official remarks, and update application statuses.",
            "• Platform Administrator (Actor: PLATFORM_ADMIN / SWD_ADMIN): State-level IT administrator overseeing platform health, monitoring user accounts, inspecting immutable security audit trails, managing scheme categories, and addressing unresolved citizen grievances.",
            "• Automated System Background Processes (Actor: SYSTEM): Background scheduled jobs that calculate dashboard statistics, expire stale tokens, and coordinate event publications."
        ]),
        ("2. Functional Requirements Matrix (FR-01 to FR-12)", [
            "The system implements 12 core functional requirements, each assigned a formal requirement identifier:",
            "FR-01 [Citizen Registration & Identity Management]: The system shall allow citizens to create accounts using mobile number, email, and password. The system shall assign a unique, permanent Citizen ID (e.g. CIT-KA-2026-DE2B4F).",
            "FR-02 [Secure Token-Based Authentication]: The system shall authenticate citizens and administrators using OAuth2 Password Bearer flow, validating hashed passwords (bcrypt) and issuing stateless JSON Web Tokens (HS256) with a 24-hour expiration window.",
            "FR-03 [Scheme Catalogue Management & Filtering]: The system shall maintain an active catalogue of 28 verified Karnataka welfare schemes across 9 categories. The system shall support non-destructive catalogue exclusions (e.g. Shakti Scheme) while preserving historical database records.",
            "FR-04 [Multidimensional Smart Scheme Finder]: The system shall provide an interactive questionnaire evaluating age, district, caste category, income, occupation, education level, gender, and marital status to compute personalized recommendations classified into Potential Match, Check Requirements, and Not Matched.",
            "FR-05 [Deterministic Rule-Based Eligibility Engine]: The system shall evaluate applicant attributes against scheme-specific rules in MySQL using supported operators (EQUALS, RANGE, LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL, IN) and return explainable criteria breakdowns without generic domicile shortcuts.",
            "FR-06 [Dynamic Scheme Application Submission]: The system shall allow authenticated citizens to submit digital dossiers for active schemes. The system shall validate all required inputs, verify duplicate application constraints, and generate a unique Application Number (e.g. SWD-APP-2026-98E64D).",
            "FR-07 [Secure Digital Document Storage]: The system shall support uploading supporting documents (marksheets, caste certificates, hospital discharge cards) in PDF or JPEG format up to 5MB, storing physical files in secure directories and indexing metadata in the database.",
            "FR-08 [Pure-Python PDF Acknowledgement Receipt]: The system shall dynamically generate downloadable official PDF 1.4 acknowledgement receipts containing department seals, applicant details, unique reference IDs, and verification hashes without external C-library dependencies.",
            "FR-09 [End-to-End Application Tracking]: The system shall provide citizens with real-time tracking of their submitted applications, displaying current status badges, assigned officer remarks, uploaded document links, and historical state transition timelines.",
            "FR-10 [Official Welfare Officer Scrutiny Workflow]: The system shall provide authorized welfare officers with a dedicated scrutiny interface to inspect applicant dossiers, review attached files, record formal justifications, and execute state transitions (UNDER_REVIEW, APPROVED, RETURNED, REJECTED).",
            "FR-11 [Direct Benefit Transfer (DBT) & Beneficiary Register]: The system shall maintain a verified beneficiary registry for approved applications and record DBT batch transactions including transaction IDs, disbursement amounts, and bank account numbers.",
            "FR-12 [Grievance Redressal & Security Audit Trails]: The system shall enable citizens to lodge grievance tickets and officers to provide resolutions. The system shall maintain an immutable audit trail capturing user logins, administrative decisions, and profile updates with timestamps."
        ]),
        ("3. Citizen User Requirements & Interactions", [
            "Citizen-facing workflows prioritize clarity, speed, and ease of use:",
            "• Profile Management: Citizens can view and update their profile details (district, taluk, annual family income, social category, educational qualification). Profile values automatically prefill subsequent scheme applications and finder questionnaires.",
            "• Scheme Finder Questionnaire: Citizens can quickly answer questions regarding their household situation. The interface dynamically updates results without requiring full page refreshes.",
            "• Application Submission & Tracking: The citizen interface displays active applications with clear, color-coded status badges: SUBMITTED (Blue), UNDER_REVIEW (Amber), APPROVED (Green), RETURNED (Purple), and REJECTED (Red). If an officer returns an application, the citizen can read the officer's exact instructions and re-submit corrected documents."
        ]),
        ("4. Welfare Officer & Administrative Requirements", [
            "Administrative workflows are strictly role-gated and auditable:",
            "• Welfare Officer Queue: Displays pending applications organized by submission date and district. Officers can view complete applicant profiles side-by-side with uploaded certificates.",
            "• Decision Interface: Before executing any status change, officers must enter mandatory administrative remarks explaining the basis of approval or rejection. State transitions are committed within an ACID relational transaction that writes simultaneously to scheme_applications and application_history.",
            "• Platform Admin Oversight: Platform administrators have read-only monitoring access to all welfare applications and citizen accounts to maintain separation of duties. Administrators can configure scheme categories, view real-time system metrics, and audit administrative event logs."
        ]),
        ("5. API & Relational Database Requirements", [
            "The service exposes RESTful JSON APIs adhering to standard HTTP status conventions:",
            "• Authentication: POST /api/swd/auth/register, POST /api/swd/auth/login, GET /api/swd/auth/me",
            "• Scheme Catalogue: GET /api/swd/schemes, GET /api/swd/schemes/{id}, GET /api/swd/categories",
            "• Smart Finder: GET /api/swd/finder/options, POST /api/swd/finder/match",
            "• Eligibility Engine: POST /api/swd/schemes/{id}/eligibility-check",
            "• Applications: POST /api/swd/applications, GET /api/swd/applications/{citizen_id}, GET /api/swd/applications/{id}/receipt, GET /api/swd/applications/{id}/documents/{doc_id}/download",
            "• Admin Scrutiny: GET /api/swd/admin/dashboard, GET /api/swd/admin/applications, PUT /api/swd/admin/applications/{id}/status, GET /api/swd/admin/users, GET /api/swd/admin/audit-logs",
            "• Database Schema: 19 relational tables in MySQL (InnoDB) with foreign keys enforcing referential integrity across users, scheme_applications, application_documents, application_history, beneficiaries, dbt_transactions, grievances, and audit_logs."
        ]),
        ("6. Input Validation & Data Integrity Rules", [
            "All data ingested by the platform undergoes multi-tier validation:",
            "• Pydantic v2 Schema Enforcement: Incoming JSON payloads are validated against strict type annotations. Missing required fields trigger HTTP 422 Unprocessable Entity responses with exact error descriptions.",
            "• Income & Age Constraints: Income fields are strictly validated as non-negative floats. Age values are bounded between 0 and 120 years.",
            "• Phone & Identity Validation: Phone numbers require 10 digits adhering to Indian telecommunication conventions. Citizen IDs follow structured prefixes (e.g. CIT-KA-2026-XXXXXX).",
            "• File Upload Safety: Uploaded documents are verified for MIME type (PDF, JPEG, PNG) and file size constraints (max 5MB). Files are assigned cryptographically random UUID filenames to prevent path traversal attacks."
        ]),
        ("7. Role-Based Access Control (RBAC) Specification", [
            "The platform enforces strict role-based permission boundaries:",
            "• CITIZEN: Authorized only to access own profile, submit applications, view own tracking history, and create personal grievances. Access to /api/swd/admin/* endpoints strictly returns HTTP 403 Forbidden.",
            "• GOVERNMENT_WELFARE_ADMIN: Authorized to view all department applications, review uploaded documents, execute status transitions, manage beneficiary lists, and schedule DBT batches.",
            "• PLATFORM_ADMIN: Authorized for system oversight, monitoring user accounts, inspecting audit trails, managing scheme taxonomies, and resolving cross-departmental grievances."
        ]),
        ("8. Core Use Cases & Scenario Walkthroughs", [
            "Use Case 1: Citizen Discovers and Checks Scheme Eligibility\nActor: Citizen (Mahesh, Age 28, Male, Student, General Category)\nPrecondition: User is registered and logged in.\nFlow: Citizen opens Eligibility Assessment, selects Scheme, fills profile attributes. Backend evaluates mandatory criteria. For Bhagyalakshmi Scheme, engine returns NOT_ELIGIBLE (violates girl-child rule). For Gruha Jyothi, engine returns INSUFFICIENT_INFORMATION (domestic meter unconfirmed).",
            "Use Case 2: Citizen Submits Welfare Application with Marksheet Upload\nActor: Citizen (Mukesh, Student)\nPrecondition: Citizen authenticated.\nFlow: Citizen selects Thayi Bhagya Scheme, enters delivery hospital details, uploads marksheet PDF. Backend validates inputs, stores file, creates application record ID 36 (SWD-APP-2026-98E64D), commits history step, and returns confirmation. Citizen downloads PDF receipt.",
            "Use Case 3: Welfare Officer Scrutinizes and Transitions Application\nActor: Welfare Officer (welfareadmin@example.com)\nPrecondition: Officer authenticated with Welfare Admin credentials.\nFlow: Officer opens Scrutiny Queue, locates application SWD-APP-2026-98E64D, views marksheet PDF, identifies missing discharge summary, enters remarks: 'Not satisfied with provided documents, please provide relevant documents', and selects UNDER_REVIEW. System commits transition to MySQL, adds history record, and updates dashboard metrics."
        ]),
        ("9. Formal Acceptance Criteria & Verification", [
            "Each functional requirement is mapped to verifiable acceptance criteria:",
            "AC-01 [Catalogue Integrity]: Must return exactly 28 Karnataka welfare schemes; Shakti Scheme must not appear in any public listing.",
            "AC-02 [Traceability of Application SWD-APP-2026-98E64D]: Must be retrievable via citizen tracking, appear in admin scrutiny queue, link to document ID 10, and reflect status UNDER_REVIEW.",
            "AC-03 [Zero False Positives in Eligibility]: Male applicants must never be marked eligible for girl-child (Bhagyalakshmi) or maternal welfare schemes.",
            "AC-04 [Receipt Generation Without Crashes]: PDF receipt endpoint must return valid PDF 1.4 stream starting with %PDF-1.4 header without missing library errors.",
            "AC-05 [Dynamic Administrative Counters]: Dashboard must query live MySQL tables; total applications must match COUNT(*) from scheme_applications."
        ]),
        ("10. Conclusion & Architectural Summary", [
            "The NagrikSetu SWD functional specification provides a complete, unambiguous blueprint of the implemented welfare management platform. Every requirement described herein is backed by live code in FastAPI, React, and MySQL.",
            "The system completely satisfies academic requirements for software architecture, separation of concerns, data integrity, and verifiable acceptance testing."
        ])
    ]

    for title, paras in sections_data:
        h = doc.add_heading(title, level=1)
        h.style.font.color.rgb = navy
        for p_text in paras:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(p_text)
            run.font.name = "Arial"
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(30, 41, 59)

    docx_path = os.path.join(BASE_DIR, "02_Functional_Requirements.docx")
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def create_report_2_pdf():
    pdf_path = os.path.join(BASE_DIR, "02_Functional_Requirements.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor('#0f2444'),
        alignment=1,
        spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=40
    )
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        alignment=1
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0f2444'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 100))
    story.append(Paragraph("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)<br/>FUNCTIONAL REQUIREMENTS SPECIFICATION", title_style))
    story.append(Paragraph("Software Engineering SRS, Actor Specifications & Rule Traceability Matrix", subtitle_style))
    story.append(Spacer(1, 80))
    story.append(Paragraph("<b>Course:</b> B.Tech Software Engineering / Software Architecture Project<br/><b>Academic Year:</b> 2026<br/><b>System Specification Standard:</b> IEEE 830-1998 (Adapted)<br/><b>Department:</b> Social Welfare Department (SWD), Government of Karnataka", meta_style))
    story.append(PageBreak())

    sections_text = [
        ("1. System Actors & Role Hierarchy", [
            "The NagrikSetu SWD system models four primary system actors with clearly separated security boundaries:",
            "<b>• Public Citizen (Actor: CITIZEN):</b> An unregistered or registered resident of Karnataka seeking information on state welfare schemes, submitting online scheme dossiers, uploading supporting certificates, downloading acknowledgement receipts, and raising grievance tickets.",
            "<b>• Government Welfare Officer (Actor: GOVERNMENT_WELFARE_ADMIN / WELFARE_OFFICER):</b> District or taluk administrative officer responsible for application scrutiny. Officers review citizen dossiers, inspect attached certificates, verify eligibility, record official remarks, and update application statuses.",
            "<b>• Platform Administrator (Actor: PLATFORM_ADMIN / SWD_ADMIN):</b> State-level IT administrator overseeing platform health, monitoring user accounts, inspecting immutable security audit trails, managing scheme categories, and addressing unresolved citizen grievances.",
            "<b>• Automated System Background Processes (Actor: SYSTEM):</b> Background scheduled jobs that calculate dashboard statistics, expire stale tokens, and coordinate event publications."
        ]),
        ("2. Functional Requirements Matrix (FR-01 to FR-12)", [
            "The system implements 12 core functional requirements, each assigned a formal requirement identifier:",
            "<b>FR-01 [Citizen Registration & Identity Management]:</b> The system shall allow citizens to create accounts using mobile number, email, and password. The system shall assign a unique, permanent Citizen ID (e.g. CIT-KA-2026-DE2B4F).",
            "<b>FR-02 [Secure Token-Based Authentication]:</b> The system shall authenticate citizens and administrators using OAuth2 Password Bearer flow, validating hashed passwords (bcrypt) and issuing stateless JSON Web Tokens (HS256) with a 24-hour expiration window.",
            "<b>FR-03 [Scheme Catalogue Management & Filtering]:</b> The system shall maintain an active catalogue of 28 verified Karnataka welfare schemes across 9 categories. The system shall support non-destructive catalogue exclusions (e.g. Shakti Scheme) while preserving historical database records.",
            "<b>FR-04 [Multidimensional Smart Scheme Finder]:</b> The system shall provide an interactive questionnaire evaluating age, district, caste category, income, occupation, education level, gender, and marital status to compute personalized recommendations classified into Potential Match, Check Requirements, and Not Matched.",
            "<b>FR-05 [Deterministic Rule-Based Eligibility Engine]:</b> The system shall evaluate applicant attributes against scheme-specific rules in MySQL using supported operators (EQUALS, RANGE, LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL, IN) and return explainable criteria breakdowns without generic domicile shortcuts.",
            "<b>FR-06 [Dynamic Scheme Application Submission]:</b> The system shall allow authenticated citizens to submit digital dossiers for active schemes. The system shall validate all required inputs, verify duplicate application constraints, and generate a unique Application Number (e.g. SWD-APP-2026-98E64D).",
            "<b>FR-07 [Secure Digital Document Storage]:</b> The system shall support uploading supporting documents (marksheets, caste certificates, hospital discharge cards) in PDF or JPEG format up to 5MB, storing physical files in secure directories and indexing metadata in the database.",
            "<b>FR-08 [Pure-Python PDF Acknowledgement Receipt]:</b> The system shall dynamically generate downloadable official PDF 1.4 acknowledgement receipts containing department seals, applicant details, unique reference IDs, and verification hashes without external C-library dependencies.",
            "<b>FR-09 [End-to-End Application Tracking]:</b> The system shall provide citizens with real-time tracking of their submitted applications, displaying current status badges, assigned officer remarks, uploaded document links, and historical state transition timelines.",
            "<b>FR-10 [Official Welfare Officer Scrutiny Workflow]:</b> The system shall provide authorized welfare officers with a dedicated scrutiny interface to inspect applicant dossiers, review attached files, record formal justifications, and execute state transitions (UNDER_REVIEW, APPROVED, RETURNED, REJECTED).",
            "<b>FR-11 [Direct Benefit Transfer (DBT) & Beneficiary Register]:</b> The system shall maintain a verified beneficiary registry for approved applications and record DBT batch transactions including transaction IDs, disbursement amounts, and bank account numbers.",
            "<b>FR-12 [Grievance Redressal & Security Audit Trails]:</b> The system shall enable citizens to lodge grievance tickets and officers to provide resolutions. The system shall maintain an immutable audit trail capturing user logins, administrative decisions, and profile updates with timestamps."
        ]),
        ("3. Citizen User Requirements & Interactions", [
            "Citizen-facing workflows prioritize clarity, speed, and ease of use:",
            "<b>• Profile Management:</b> Citizens can view and update their profile details (district, taluk, annual family income, social category, educational qualification). Profile values automatically prefill subsequent scheme applications and finder questionnaires.",
            "<b>• Scheme Finder Questionnaire:</b> Citizens can quickly answer questions regarding their household situation. The interface dynamically updates results without requiring full page refreshes.",
            "<b>• Application Submission & Tracking:</b> The citizen interface displays active applications with clear, color-coded status badges: SUBMITTED (Blue), UNDER_REVIEW (Amber), APPROVED (Green), RETURNED (Purple), and REJECTED (Red). If an officer returns an application, the citizen can read the officer's exact instructions and re-submit corrected documents."
        ]),
        ("4. Welfare Officer & Administrative Requirements", [
            "Administrative workflows are strictly role-gated and auditable:",
            "<b>• Welfare Officer Queue:</b> Displays pending applications organized by submission date and district. Officers can view complete applicant profiles side-by-side with uploaded certificates.",
            "<b>• Decision Interface:</b> Before executing any status change, officers must enter mandatory administrative remarks explaining the basis of approval or rejection. State transitions are committed within an ACID relational transaction that writes simultaneously to scheme_applications and application_history.",
            "<b>• Platform Admin Oversight:</b> Platform administrators have read-only monitoring access to all welfare applications and citizen accounts to maintain separation of duties. Administrators can configure scheme categories, view real-time system metrics, and audit administrative event logs."
        ]),
        ("5. API & Relational Database Requirements", [
            "The service exposes RESTful JSON APIs adhering to standard HTTP status conventions:",
            "<b>• Authentication:</b> POST /api/swd/auth/register, POST /api/swd/auth/login, GET /api/swd/auth/me",
            "<b>• Scheme Catalogue:</b> GET /api/swd/schemes, GET /api/swd/schemes/{id}, GET /api/swd/categories",
            "<b>• Smart Finder:</b> GET /api/swd/finder/options, POST /api/swd/finder/match",
            "<b>• Eligibility Engine:</b> POST /api/swd/schemes/{id}/eligibility-check",
            "<b>• Applications:</b> POST /api/swd/applications, GET /api/swd/applications/{citizen_id}, GET /api/swd/applications/{id}/receipt, GET /api/swd/applications/{id}/documents/{doc_id}/download",
            "<b>• Admin Scrutiny:</b> GET /api/swd/admin/dashboard, GET /api/swd/admin/applications, PUT /api/swd/admin/applications/{id}/status, GET /api/swd/admin/users, GET /api/swd/admin/audit-logs",
            "<b>• Database Schema:</b> 19 relational tables in MySQL (InnoDB) with foreign keys enforcing referential integrity across users, scheme_applications, application_documents, application_history, beneficiaries, dbt_transactions, grievances, and audit_logs."
        ]),
        ("6. Input Validation & Data Integrity Rules", [
            "All data ingested by the platform undergoes multi-tier validation:",
            "<b>• Pydantic v2 Schema Enforcement:</b> Incoming JSON payloads are validated against strict type annotations. Missing required fields trigger HTTP 422 Unprocessable Entity responses with exact error descriptions.",
            "<b>• Income & Age Constraints:</b> Income fields are strictly validated as non-negative floats. Age values are bounded between 0 and 120 years.",
            "<b>• Phone & Identity Validation:</b> Phone numbers require 10 digits adhering to Indian telecommunication conventions. Citizen IDs follow structured prefixes (e.g. CIT-KA-2026-XXXXXX).",
            "<b>• File Upload Safety:</b> Uploaded documents are verified for MIME type (PDF, JPEG, PNG) and file size constraints (max 5MB). Files are assigned cryptographically random UUID filenames to prevent path traversal attacks."
        ]),
        ("7. Role-Based Access Control (RBAC) Specification", [
            "The platform enforces strict role-based permission boundaries:",
            "<b>• CITIZEN:</b> Authorized only to access own profile, submit applications, view own tracking history, and create personal grievances. Access to /api/swd/admin/* endpoints strictly returns HTTP 403 Forbidden.",
            "<b>• GOVERNMENT_WELFARE_ADMIN:</b> Authorized to view all department applications, review uploaded documents, execute status transitions, manage beneficiary lists, and schedule DBT batches.",
            "<b>• PLATFORM_ADMIN:</b> Authorized for system oversight, monitoring user accounts, inspecting audit trails, managing scheme taxonomies, and resolving cross-departmental grievances."
        ]),
        ("8. Core Use Cases & Scenario Walkthroughs", [
            "<b>Use Case 1: Citizen Discovers and Checks Scheme Eligibility</b><br/>Actor: Citizen (Mahesh, Age 28, Male, Student, General Category)<br/>Precondition: User is registered and logged in.<br/>Flow: Citizen opens Eligibility Assessment, selects Scheme, fills profile attributes. Backend evaluates mandatory criteria. For Bhagyalakshmi Scheme, engine returns NOT_ELIGIBLE (violates girl-child rule). For Gruha Jyothi, engine returns INSUFFICIENT_INFORMATION (domestic meter unconfirmed).",
            "<b>Use Case 2: Citizen Submits Welfare Application with Marksheet Upload</b><br/>Actor: Citizen (Mukesh, Student)<br/>Precondition: Citizen authenticated.<br/>Flow: Citizen selects Thayi Bhagya Scheme, enters delivery hospital details, uploads marksheet PDF. Backend validates inputs, stores file, creates application record ID 36 (SWD-APP-2026-98E64D), commits history step, and returns confirmation. Citizen downloads PDF receipt.",
            "<b>Use Case 3: Welfare Officer Scrutinizes and Transitions Application</b><br/>Actor: Welfare Officer (welfareadmin@example.com)<br/>Precondition: Officer authenticated with Welfare Admin credentials.<br/>Flow: Officer opens Scrutiny Queue, locates application SWD-APP-2026-98E64D, views marksheet PDF, identifies missing discharge summary, enters remarks: 'Not satisfied with provided documents, please provide relevant documents', and selects UNDER_REVIEW. System commits transition to MySQL, adds history record, and updates dashboard metrics."
        ]),
        ("9. Formal Acceptance Criteria & Verification", [
            "Each functional requirement is mapped to verifiable acceptance criteria:",
            "<b>AC-01 [Catalogue Integrity]:</b> Must return exactly 28 Karnataka welfare schemes; Shakti Scheme must not appear in any public listing.",
            "<b>AC-02 [Traceability of Application SWD-APP-2026-98E64D]:</b> Must be retrievable via citizen tracking, appear in admin scrutiny queue, link to document ID 10, and reflect status UNDER_REVIEW.",
            "<b>AC-03 [Zero False Positives in Eligibility]:</b> Male applicants must never be marked eligible for girl-child (Bhagyalakshmi) or maternal welfare schemes.",
            "<b>AC-04 [Receipt Generation Without Crashes]:</b> PDF receipt endpoint must return valid PDF 1.4 stream starting with %PDF-1.4 header without missing library errors.",
            "<b>AC-05 [Dynamic Administrative Counters]:</b> Dashboard must query live MySQL tables; total applications must match COUNT(*) from scheme_applications."
        ]),
        ("10. Conclusion & Architectural Summary", [
            "The NagrikSetu SWD functional specification provides a complete, unambiguous blueprint of the implemented welfare management platform. Every requirement described herein is backed by live code in FastAPI, React, and MySQL.",
            "The system completely satisfies academic requirements for software architecture, separation of concerns, data integrity, and verifiable acceptance testing."
        ])
    ]

    for title, paras in sections_text:
        story.append(Paragraph(title, h1_style))
        for p in paras:
            story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {pdf_path}")

create_report_2_docx()
create_report_2_pdf()
print("Report 2 (Functional Requirements) Generation Complete!")
