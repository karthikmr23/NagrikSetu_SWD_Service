import io
import csv
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.database.connection import get_db
from app.models import (
    SchemeApplication, Beneficiary, DbtTransaction, Grievance, Scheme
)
from app.core.security import require_role

router = APIRouter(prefix="/api/swd/reports", tags=["SWD Reports & Analytics"])

AUTHORIZED_REPORT_ROLES = ["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"]

@router.get("/export/applications")
def export_applications_csv(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(AUTHORIZED_REPORT_ROLES))
):
    apps = db.query(SchemeApplication).order_by(SchemeApplication.id.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Application ID", "Dossier Number", "Citizen ID", "Citizen Name",
        "Phone", "District", "Income (INR)", "Category", "Status", "Submitted On"
    ])
    for a in apps:
        writer.writerow([
            a.id, a.application_number, a.citizen_id, a.citizen_name,
            a.citizen_phone, a.residence_district, float(a.annual_income),
            a.caste_category, a.status, a.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=swd_applications_report.csv"}
    )

@router.get("/export/beneficiaries")
def export_beneficiaries_csv(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(AUTHORIZED_REPORT_ROLES))
):
    bens = db.query(Beneficiary).order_by(Beneficiary.id.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Beneficiary ID", "Beneficiary Code", "Citizen ID", "Citizen Name",
        "Scheme Name", "Sanctioned Amount (INR)", "Disbursement Mode", "Status", "Sanctioned On"
    ])
    for b in bens:
        writer.writerow([
            b.id, b.beneficiary_code, b.citizen_id, b.citizen_name,
            b.scheme.name if b.scheme else "Welfare Scheme", float(b.sanctioned_amount),
            b.disbursement_mode, b.status, b.sanctioned_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=swd_beneficiaries_report.csv"}
    )

@router.get("/analytics/districts")
def get_district_analytics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(AUTHORIZED_REPORT_ROLES))
):
    """District-wise application and sanction volume distribution."""
    results = db.query(
        SchemeApplication.residence_district,
        func.count(SchemeApplication.id).label("total_applications"),
        func.sum(case((SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"]), 1), else_=0)).label("approved_applications")
    ).group_by(SchemeApplication.residence_district).all()

    data = []
    for r in results:
        data.append({
            "district": r.residence_district,
            "total_applications": r.total_applications,
            "approved_applications": int(r.approved_applications or 0)
        })
    return {"districts": data}

@router.get("/export/dbt")
def export_dbt_csv(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(AUTHORIZED_REPORT_ROLES))
):
    txs = db.query(DbtTransaction).order_by(DbtTransaction.id.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Transaction ID", "Reference Number", "Beneficiary ID", "Amount (INR)",
        "Payment Mode", "Status", "Account Last4", "IFSC", "Processed At"
    ])
    for t in txs:
        writer.writerow([
            t.id, t.transaction_reference, t.beneficiary_id, float(t.amount),
            t.payment_mode, t.status, t.bank_account_last4, t.ifsc_code,
            t.processed_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=swd_dbt_transactions_report.csv"}
    )
