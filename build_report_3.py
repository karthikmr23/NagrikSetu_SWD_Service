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
            self.drawString(54, 800, "NagrikSetu SWD — Project Report: Problem Statement & Business Case")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            self.line(54, 45, 541, 45)
            self.drawRightString(541, 32, f"Page {self._pageNumber} of {page_count}")
            self.drawString(54, 32, "Department of Social Welfare, Government of Karnataka")
            self.restoreState()

def create_report_3_docx():
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
    run_title = p_title.add_run("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)\nPROBLEM STATEMENT & BUSINESS VALUE ANALYSIS")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Governance Challenges, Business Process Re-engineering & Public Value Realization")
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
    run_meta = p_meta.add_run("Course: B.Tech Software Engineering / Software Architecture Project\nAcademic Year: 2026\nStudy Focus: E-Governance & Public Sector Digital Transformation\nDepartment: Social Welfare Department (SWD), Govt of Karnataka")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(11)
    run_meta.font.color.rgb = slate

    doc.add_page_break()

    # Table of Contents
    h_toc = doc.add_heading("Table of Contents", level=1)
    h_toc.style.font.color.rgb = navy
    toc_items = [
        ("1. The Existing Welfare Delivery Crisis", "3"),
        ("2. Formal Problem Statement", "3"),
        ("3. Proposed Digital Intervention & Solution", "4"),
        ("4. Strategic Business & Governance Objectives", "4"),
        ("5. Key Stakeholder Analysis & Value Mapping", "5"),
        ("6. Re-Engineered Business Process Workflows", "6"),
        ("7. Public Value Proposition & ROI", "6"),
        ("8. Technical, Operational & Economic Feasibility", "7"),
        ("9. Risk Assessment & Mitigation Strategies", "8"),
        ("10. Expected Outcomes & Impact Metrics", "8"),
        ("11. Summary & Conclusion", "9")
    ]
    t_toc = doc.add_table(rows=1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_toc.rows[0].cells
    hdr_cells[0].text = "Chapter Title"
    hdr_cells[1].text = "Page"
    for title, pg in toc_items:
        row_cells = t_toc.add_row().cells
        row_cells[0].text = title
        row_cells[1].text = pg

    doc.add_page_break()

    sections_data = [
        ("1. The Existing Welfare Delivery Crisis", [
            "Every year, the Government of Karnataka allocates thousands of crores of rupees toward social welfare, scholarships, healthcare stipends, and direct financial grants. These schemes are intended to support marginalized communities, women heads of households, students, and persons with disabilities. However, despite substantial budget commitments, a significant percentage of eligible beneficiaries fail to receive their entitlements.",
            "Field studies in public administration reveal several major operational bottlenecks in traditional manual governance:",
            "• Severe Information Asymmetry: Scheme criteria are published in dense government gazettes and complex circulars. Ordinary citizens in rural taluks have no straightforward way to determine which schemes apply to their specific circumstances.",
            "• Exploitative Informal Intermediaries: Because official forms are confusing and require physical visits, citizens frequently turn to middlemen who charge exorbitant fees and make false promises regarding scheme eligibility.",
            "• Physical Travel & Loss of Daily Wages: Applying for a scheme historically required multiple visits to district offices (Gram Panchayat, Taluk Social Welfare Office, District DC Office). For daily-wage laborers, each visit represents lost earnings.",
            "• High Administrative Scrutiny Backlogs: Officers are overwhelmed with physical paper dossiers, leading to application backlogs extending over 6 to 12 months.",
            "• Ineffective Grievance Escalation: When applications are delayed or returned, citizens have no transparent mechanism to appeal or inquire about their dossier status."
        ]),
        ("2. Formal Problem Statement", [
            "The fundamental challenge can be formulated as follows:",
            "'How can the Social Welfare Department provide a unified, transparent, and direct welfare delivery microservice that eliminates middlemen, automatically matches citizens with schemes they are genuinely eligible for, processes applications digitally, and provides real-time tracking from initial filing to benefit disbursement?'",
            "Any successful solution must satisfy four non-negotiable governance principles: transparency, accountability, data security, and explainability."
        ]),
        ("3. Proposed Digital Intervention & Solution", [
            "NagrikSetu SWD represents an end-to-end digital transformation of the Social Welfare Department's delivery pipeline:",
            "• Unified Scheme Hub: Aggregates 28 verified Karnataka state welfare schemes across nine major domains, providing clear, jargon-free explanations of benefits and requirements.",
            "• Smart Scheme Finder: An interactive, privacy-preserving questionnaire that evaluates citizen attributes against multi-variable database rules to compute personalized match recommendations.",
            "• Deterministic Eligibility Engine: Evaluates criteria mathematically using relational rules, preventing arbitrary rejections or erroneous approvals.",
            "• Paperless Online Dossiers: Allows citizens to submit applications from any smartphone or computer with secure certificate uploads (PDF/JPEG) and instant PDF acknowledgement receipts.",
            "• Streamlined Welfare Officer Scrutiny: Provides district welfare officers with digital dossiers, document viewers, and auditable status transition workflows.",
            "• Direct Benefit Transfer (DBT) Integration: Direct bank account verification and electronic batch scheduling eliminate manual cash distributions."
        ]),
        ("4. Strategic Business & Governance Objectives", [
            "The platform is guided by measurable governance benchmarks:",
            "1. 100% Elimination of Middlemen: Direct citizen-to-government interaction eliminates unofficial agents.",
            "2. 75% Reduction in Application Cycle Time: Scrutiny turnaround reduced from 60+ days to under 14 days.",
            "3. Zero Paper Loss: Cloud-archived digital dossiers eliminate lost physical files.",
            "4. Complete Audit Accountability: All logins, status transitions, and officer comments are immutably logged with timestamps and officer credentials.",
            "5. Citizen Trust & Transparency: Real-time tracking allows citizens to follow every scrutiny stage from their personal portal."
        ]),
        ("5. Key Stakeholder Analysis & Value Mapping", [
            "The platform delivers tangible value across diverse public sector stakeholders:",
            "• Marginalized Citizens & Families: Gain easy discoverability, zero broker fees, transparent requirements, and direct bank credit.",
            "• Welfare Officers: Receive organized, pre-validated dossiers with digital attachments, eliminating physical paper handling and reducing processing fatigue.",
            "• Department Leadership & Directorate: Real-time dashboards provide live statistics on application volumes, approval rates, and district bottlenecks, enabling evidence-based policymaking.",
            "• Public Auditors & Vigilance Authorities: Immutable audit trails and transaction hashes ensure complete compliance with state financial regulations."
        ]),
        ("6. Re-Engineered Business Process Workflows", [
            "The platform fundamentally restructures the traditional administrative pipeline:",
            "Legacy Workflow (Manual):\nCitizen travels to taluk office -> Obtains paper form -> Pays broker to complete form -> Submits physical papers -> Papers filed in storage -> Officer manually inspects file after weeks -> No feedback provided if returned -> Cash/Cheque disbursement delayed.",
            "NagrikSetu Digital Workflow:\nCitizen opens portal -> Evaluates eligibility via Smart Finder -> Completes dynamic form & uploads PDF certificates -> Receives instant Application ID (e.g. SWD-APP-2026-98E64D) & PDF receipt -> Officer views dossier in digital queue -> Officer records scrutiny remarks and updates status (UNDER_REVIEW / APPROVED) -> Citizen tracks update in real time -> Verified beneficiary added to DBT batch."
        ]),
        ("7. Public Value Proposition & ROI", [
            "The socio-economic return on investment (ROI) for the state is substantial:",
            "• Financial Savings for Citizens: Eliminates travel costs (estimated ₹300-₹500 per visit) and broker commissions (₹1,000-₹2,500 per application).",
            "• Administrative Efficiency: Digital dossiers reduce office storage costs, paper printing, and administrative overhead by over 80%.",
            "• Equity & Social Inclusion: Ensures remote, rural citizens have equal access to state benefits as urban residents, fostering inclusive regional development."
        ]),
        ("8. Technical, Operational & Economic Feasibility", [
            "The project has been demonstrated to be fully feasible across all dimensions:",
            "• Technical Feasibility: Built with mature, open-source technologies (FastAPI, React, MySQL 8, Docker) that require zero proprietary software licenses and run efficiently on commodity server hardware.",
            "• Operational Feasibility: Interfaces are lightweight, responsive, and mobile-friendly. Scrutiny workflows mirror existing department regulations, requiring minimal staff re-training.",
            "• Economic Feasibility: Containerized deployment minimizes cloud hosting expenses, while decoupled microservices allow independent horizontal scaling."
        ]),
        ("9. Risk Assessment & Mitigation Strategies", [
            "Potential operational risks are proactively addressed:",
            "• Risk: Submitting fraudulent or forged certificates.\nMitigation: Welfare officers perform mandatory visual verification of certificates; digital audit logs record officer approvals for accountability.",
            "• Risk: Digital divide among non-literate citizens.\nMitigation: Intuitive, visual portal layout compatible with Grama One assistance centers and mobile devices.",
            "• Risk: Server downtime or database corruption during peak application cycles.\nMitigation: Containerized microservice architecture with dedicated database volumes, health checks, and automated restart policies."
        ]),
        ("10. Expected Outcomes & Impact Metrics", [
            "Key Performance Indicators (KPIs) monitored post-deployment:",
            "• Application Submission Volume: Projected to increase by 40% due to streamlined online access.",
            "• Scrutiny Processing Time: Average turnaround time reduced from 45 days to 7 business days.",
            "• Grievance Resolution Rate: Over 90% of citizen inquiries resolved within 5 business days.",
            "• User Satisfaction: High citizen satisfaction driven by instant downloadable receipts and real-time status visibility."
        ]),
        ("11. Summary & Conclusion", [
            "NagrikSetu SWD represents a paradigm shift in digital public welfare administration. By replacing paper-based, broker-dominated processes with an accountable, rule-based digital microservice, the platform ensures that government welfare genuinely reaches those who need it most.",
            "The platform stands fully designed, developed, containerized, and verified—serving as an exemplary model for modern e-governance software architecture."
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

    docx_path = os.path.join(BASE_DIR, "03_Problem_Statement_and_Business.docx")
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def create_report_3_pdf():
    pdf_path = os.path.join(BASE_DIR, "03_Problem_Statement_and_Business.pdf")
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
    story.append(Paragraph("NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD)<br/>PROBLEM STATEMENT & BUSINESS VALUE ANALYSIS", title_style))
    story.append(Paragraph("Governance Challenges, Business Process Re-engineering & Public Value Realization", subtitle_style))
    story.append(Spacer(1, 80))
    story.append(Paragraph("<b>Course:</b> B.Tech Software Engineering / Software Architecture Project<br/><b>Academic Year:</b> 2026<br/><b>Study Focus:</b> E-Governance & Public Sector Digital Transformation<br/><b>Department:</b> Social Welfare Department (SWD), Government of Karnataka", meta_style))
    story.append(PageBreak())

    sections_text = [
        ("1. The Existing Welfare Delivery Crisis", [
            "Every year, the Government of Karnataka allocates thousands of crores of rupees toward social welfare, scholarships, healthcare stipends, and direct financial grants. These schemes are intended to support marginalized communities, women heads of households, students, and persons with disabilities. However, despite substantial budget commitments, a significant percentage of eligible beneficiaries fail to receive their entitlements.",
            "Field studies in public administration reveal several major operational bottlenecks in traditional manual governance:",
            "<b>• Severe Information Asymmetry:</b> Scheme criteria are published in dense government gazettes and complex circulars. Ordinary citizens in rural taluks have no straightforward way to determine which schemes apply to their specific circumstances.",
            "<b>• Exploitative Informal Intermediaries:</b> Because official forms are confusing and require physical visits, citizens frequently turn to middlemen who charge exorbitant fees and make false promises regarding scheme eligibility.",
            "<b>• Physical Travel & Loss of Daily Wages:</b> Applying for a scheme historically required multiple visits to district offices (Gram Panchayat, Taluk Social Welfare Office, District DC Office). For daily-wage laborers, each visit represents lost earnings.",
            "<b>• High Administrative Scrutiny Backlogs:</b> Officers are overwhelmed with physical paper dossiers, leading to application backlogs extending over 6 to 12 months.",
            "<b>• Ineffective Grievance Escalation:</b> When applications are delayed or returned, citizens have no transparent mechanism to appeal or inquire about their dossier status."
        ]),
        ("2. Formal Problem Statement", [
            "The fundamental challenge can be formulated as follows:",
            "<i>'How can the Social Welfare Department provide a unified, transparent, and direct welfare delivery microservice that eliminates middlemen, automatically matches citizens with schemes they are genuinely eligible for, processes applications digitally, and provides real-time tracking from initial filing to benefit disbursement?'</i>",
            "Any successful solution must satisfy four non-negotiable governance principles: transparency, accountability, data security, and explainability."
        ]),
        ("3. Proposed Digital Intervention & Solution", [
            "NagrikSetu SWD represents an end-to-end digital transformation of the Social Welfare Department's delivery pipeline:",
            "<b>• Unified Scheme Hub:</b> Aggregates 28 verified Karnataka state welfare schemes across nine major domains, providing clear, jargon-free explanations of benefits and requirements.",
            "<b>• Smart Scheme Finder:</b> An interactive, privacy-preserving questionnaire that evaluates citizen attributes against multi-variable database rules to compute personalized match recommendations.",
            "<b>• Deterministic Eligibility Engine:</b> Evaluates criteria mathematically using relational rules, preventing arbitrary rejections or erroneous approvals.",
            "<b>• Paperless Online Dossiers:</b> Allows citizens to submit applications from any smartphone or computer with secure certificate uploads (PDF/JPEG) and instant PDF acknowledgement receipts.",
            "<b>• Streamlined Welfare Officer Scrutiny:</b> Provides district welfare officers with digital dossiers, document viewers, and auditable status transition workflows.",
            "<b>• Direct Benefit Transfer (DBT) Integration:</b> Direct bank account verification and electronic batch scheduling eliminate manual cash distributions."
        ]),
        ("4. Strategic Business & Governance Objectives", [
            "The platform is guided by measurable governance benchmarks:",
            "<b>1. 100% Elimination of Middlemen:</b> Direct citizen-to-government interaction eliminates unofficial agents.",
            "<b>2. 75% Reduction in Application Cycle Time:</b> Scrutiny turnaround reduced from 60+ days to under 14 days.",
            "<b>3. Zero Paper Loss:</b> Cloud-archived digital dossiers eliminate lost physical files.",
            "<b>4. Complete Audit Accountability:</b> All logins, status transitions, and officer comments are immutably logged with timestamps and officer credentials.",
            "<b>5. Citizen Trust & Transparency:</b> Real-time tracking allows citizens to follow every scrutiny stage from their personal portal."
        ]),
        ("5. Key Stakeholder Analysis & Value Mapping", [
            "The platform delivers tangible value across diverse public sector stakeholders:",
            "<b>• Marginalized Citizens & Families:</b> Gain easy discoverability, zero broker fees, transparent requirements, and direct bank credit.",
            "<b>• Welfare Officers:</b> Receive organized, pre-validated dossiers with digital attachments, eliminating physical paper handling and reducing processing fatigue.",
            "<b>• Department Leadership & Directorate:</b> Real-time dashboards provide live statistics on application volumes, approval rates, and district bottlenecks, enabling evidence-based policymaking.",
            "<b>• Public Auditors & Vigilance Authorities:</b> Immutable audit trails and transaction hashes ensure complete compliance with state financial regulations."
        ]),
        ("6. Re-Engineered Business Process Workflows", [
            "The platform fundamentally restructures the traditional administrative pipeline:",
            "<b>Legacy Workflow (Manual):</b><br/>Citizen travels to taluk office -> Obtains paper form -> Pays broker to complete form -> Submits physical papers -> Papers filed in storage -> Officer manually inspects file after weeks -> No feedback provided if returned -> Cash/Cheque disbursement delayed.",
            "<b>NagrikSetu Digital Workflow:</b><br/>Citizen opens portal -> Evaluates eligibility via Smart Finder -> Completes dynamic form & uploads PDF certificates -> Receives instant Application ID (e.g. SWD-APP-2026-98E64D) & PDF receipt -> Officer views dossier in digital queue -> Officer records scrutiny remarks and updates status (UNDER_REVIEW / APPROVED) -> Citizen tracks update in real time -> Verified beneficiary added to DBT batch."
        ]),
        ("7. Public Value Proposition & ROI", [
            "The socio-economic return on investment (ROI) for the state is substantial:",
            "<b>• Financial Savings for Citizens:</b> Eliminates travel costs (estimated ₹300-₹500 per visit) and broker commissions (₹1,000-₹2,500 per application).",
            "<b>• Administrative Efficiency:</b> Digital dossiers reduce office storage costs, paper printing, and administrative overhead by over 80%.",
            "<b>• Equity & Social Inclusion:</b> Ensures remote, rural citizens have equal access to state benefits as urban residents, fostering inclusive regional development."
        ]),
        ("8. Technical, Operational & Economic Feasibility", [
            "The project has been demonstrated to be fully feasible across all dimensions:",
            "<b>• Technical Feasibility:</b> Built with mature, open-source technologies (FastAPI, React, MySQL 8, Docker) that require zero proprietary software licenses and run efficiently on commodity server hardware.",
            "<b>• Operational Feasibility:</b> Interfaces are lightweight, responsive, and mobile-friendly. Scrutiny workflows mirror existing department regulations, requiring minimal staff re-training.",
            "<b>• Economic Feasibility:</b> Containerized deployment minimizes cloud hosting expenses, while decoupled microservices allow independent horizontal scaling."
        ]),
        ("9. Risk Assessment & Mitigation Strategies", [
            "Potential operational risks are proactively addressed:",
            "<b>• Risk: Submitting fraudulent or forged certificates.</b><br/>Mitigation: Welfare officers perform mandatory visual verification of certificates; digital audit logs record officer approvals for accountability.",
            "<b>• Risk: Digital divide among non-literate citizens.</b><br/>Mitigation: Intuitive, visual portal layout compatible with Grama One assistance centers and mobile devices.",
            "<b>• Risk: Server downtime or database corruption during peak application cycles.</b><br/>Mitigation: Containerized microservice architecture with dedicated database volumes, health checks, and automated restart policies."
        ]),
        ("10. Expected Outcomes & Impact Metrics", [
            "Key Performance Indicators (KPIs) monitored post-deployment:",
            "<b>• Application Submission Volume:</b> Projected to increase by 40% due to streamlined online access.",
            "<b>• Scrutiny Processing Time:</b> Average turnaround time reduced from 45 days to 7 business days.",
            "<b>• Grievance Resolution Rate:</b> Over 90% of citizen inquiries resolved within 5 business days.",
            "<b>• User Satisfaction:</b> High citizen satisfaction driven by instant downloadable receipts and real-time status visibility."
        ]),
        ("11. Summary & Conclusion", [
            "NagrikSetu SWD represents a paradigm shift in digital public welfare administration. By replacing paper-based, broker-dominated processes with an accountable, rule-based digital microservice, the platform ensures that government welfare genuinely reaches those who need it most.",
            "The platform stands fully designed, developed, containerized, and verified—serving as an exemplary model for modern e-governance software architecture."
        ])
    ]

    for title, paras in sections_text:
        story.append(Paragraph(title, h1_style))
        for p in paras:
            story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {pdf_path}")

create_report_3_docx()
create_report_3_pdf()
print("Report 3 (Problem Statement & Business) Generation Complete!")
