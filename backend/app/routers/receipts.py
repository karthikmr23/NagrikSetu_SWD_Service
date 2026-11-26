import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import SchemeApplication, Scheme
from app.core.security import get_current_user, verify_citizen_ownership

router = APIRouter(prefix="/api/swd", tags=["SWD Receipts"])

def mask_text(text: str, visible_start: int = 2, visible_end: int = 2) -> str:
    if not text:
        return "N/A"
    s = str(text).strip()
    if len(s) <= (visible_start + visible_end):
        return s[:visible_start] + "***"
    return s[:visible_start] + ("*" * (len(s) - visible_start - visible_end)) + s[-visible_end:]

def generate_minimal_pdf(app_record, scheme_title, dept_name, formatted_date):
    """
    Lightweight, dependency-free pure Python PDF generation following PDF 1.4 specification.
    Produces a valid, high-fidelity PDF without external C-extensions or reportlab.
    """
    app_num = app_record.application_number or f"SWD-APP-2026-{app_record.id}"
    applicant = app_record.citizen_name or "Applicant"
    status_str = (app_record.status or "SUBMITTED").replace("_", " ")
    income_str = f"INR {float(app_record.annual_income):,.2f}" if app_record.annual_income else "N/A"
    district_str = app_record.residence_district or "Karnataka"
    category_str = app_record.caste_category or "General"
    bank_acc = mask_text(app_record.bank_account_number)
    bank_ifsc = app_record.bank_ifsc or "N/A"
    
    # Text stream elements
    stream_lines = [
        "BT",
        "/F1 16 Tf",
        "50 780 Td",
        "(GOVERNMENT OF KARNATAKA) Tj",
        "/F1 12 Tf",
        "0 -24 Td",
        "(Department of Social Welfare - NagrikSetu SWD Portal) Tj",
        "/F1 10 Tf",
        "0 -18 Td",
        "(OFFICIAL WELFARE APPLICATION ACKNOWLEDGEMENT RECEIPT) Tj",
        "0 -25 Td",
        f"(Generated On: {formatted_date}) Tj",
        "0 -20 Td",
        f"(Application Number: {app_num}) Tj",
        "0 -16 Td",
        f"(Scheme: {scheme_title[:60]}) Tj",
        "0 -16 Td",
        f"(Department: {dept_name[:60]}) Tj",
        "0 -22 Td",
        "(APPLICANT & VERIFICATION PARTICULARS:) Tj",
        "0 -16 Td",
        f"(  Applicant Name: {applicant}) Tj",
        "0 -14 Td",
        f"(  Citizen ID: {app_record.citizen_id}) Tj",
        "0 -14 Td",
        f"(  Social Category: {category_str}) Tj",
        "0 -14 Td",
        f"(  Residence District: {district_str}) Tj",
        "0 -14 Td",
        f"(  Annual Family Income: {income_str}) Tj",
        "0 -14 Td",
        f"(  Aadhaar-Seeded Bank Account: {bank_acc}) Tj",
        "0 -14 Td",
        f"(  Bank IFSC: {bank_ifsc}) Tj",
        "0 -14 Td",
        f"(  Current Scrutiny Status: {status_str}) Tj",
        "0 -25 Td",
        "(STATUTORY DIRECT BENEFIT TRANSFER (DBT) NOTICE:) Tj",
        "0 -14 Td",
        "(This receipt confirms official submission into the Karnataka State Welfare Repository.) Tj",
        "0 -12 Td",
        "(Direct Benefit Transfers are disbursed via Aadhaar Payment Bridge (APB) to authenticated accounts.) Tj",
        "0 -30 Td",
        "(Digitally certified by NagrikSetu SWD Microservice Engine - 2026) Tj",
        "ET"
    ]
    stream_content = "\n".join(stream_lines).encode("latin-1")
    stream_len = len(stream_content)

    pdf_parts = [
        b"%PDF-1.4\n",
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("latin-1") + stream_content + b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    ]
    
    body = b"".join(pdf_parts)
    # xref table
    offsets = [0]
    curr = len(b"%PDF-1.4\n")
    offsets.append(curr)
    curr += len(pdf_parts[1])
    offsets.append(curr)
    curr += len(pdf_parts[2])
    offsets.append(curr)
    curr += len(pdf_parts[3])
    offsets.append(curr)
    curr += len(pdf_parts[4])
    offsets.append(curr)

    xref = f"xref\n0 6\n0000000000 65535 f \n"
    for o in offsets[1:]:
        xref += f"{o:010d} 00000 n \n"
    trailer = f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{len(body)}\n%%EOF\n"
    return body + xref.encode("latin-1") + trailer.encode("latin-1")

@router.get("/applications/{application_id}/receipt")
def generate_application_receipt(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Scheme application record not found")

    user_role = current_user.get("role", "")
    if user_role == "CITIZEN":
        verify_citizen_ownership(app_record.citizen_id, current_user)
    elif user_role not in ["GOVERNMENT_WELFARE_ADMIN", "WELFARE_OFFICER", "ADMINISTRATOR", "PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(status_code=403, detail="Access denied")

    scheme = db.query(Scheme).filter(Scheme.id == app_record.scheme_id).first()
    scheme_title = scheme.name if scheme else "Karnataka Social Welfare Department Welfare Scheme"
    dept_name = scheme.department if scheme and scheme.department else "Department of Social Welfare, Government of Karnataka"
    formatted_date = datetime.now().strftime("%d-%b-%Y %H:%M IST")

    try:
        # Check if reportlab is available
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("<b>GOVERNMENT OF KARNATAKA</b>", styles["Heading1"]),
            Paragraph(dept_name, styles["Normal"]),
            Paragraph("Official Scheme Acknowledgement", styles["Heading2"]),
            Spacer(1, 12),
            Paragraph(f"Application Number: {app_record.application_number}", styles["Normal"]),
            Paragraph(f"Applicant: {app_record.citizen_name}", styles["Normal"]),
            Paragraph(f"Status: {app_record.status}", styles["Normal"])
        ]
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
    except ImportError:
        # High-fidelity native PDF generation fallback
        pdf_bytes = generate_minimal_pdf(app_record, scheme_title, dept_name, formatted_date)

    filename = f"Receipt_{app_record.application_number}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff"
        }
    )
