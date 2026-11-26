import os
import io
import csv
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database.connection import get_db
from app.models import (
    Beneficiary, DbtTransaction, SchemeApplication, Scheme, AuditLog
)
from app.schemas import (
    BeneficiaryResponse, DbtTransactionResponse, DbtProcessRequest,
    DbtBatchProcessRequest, DbtBatchProcessResponse, DbtBatchProcessResultItem,
    DbtDashboardStats
)
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/swd", tags=["SWD Beneficiaries & Simulated Direct Benefit Transfer"])

@router.get("/dbt/dashboard-stats", response_model=DbtDashboardStats)
def get_dbt_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN"]))
):
    """Returns real-time aggregated metrics for the simulated DBT payment system."""
    total_approved = db.query(func.count(Beneficiary.id)).scalar() or 0
    total_tx = db.query(func.count(DbtTransaction.id)).scalar() or 0
    success_tx = db.query(func.count(DbtTransaction.id)).filter(DbtTransaction.status == "SUCCESSFUL").scalar() or 0
    failed_tx = db.query(func.count(DbtTransaction.id)).filter(DbtTransaction.status == "FAILED").scalar() or 0
    pending_tx = db.query(func.count(DbtTransaction.id)).filter(DbtTransaction.status == "PENDING").scalar() or 0
    
    total_disbursed_res = db.query(func.sum(DbtTransaction.amount)).filter(DbtTransaction.status == "SUCCESSFUL").scalar()
    total_disbursed = float(total_disbursed_res) if total_disbursed_res else 0.0

    allocated_budget = 10000000.00  # ₹1.00 Crore allocated welfare fund for academic demo
    remaining_budget = max(0.0, allocated_budget - total_disbursed)

    return DbtDashboardStats(
        total_approved_beneficiaries=total_approved,
        total_payments_processed=total_tx,
        successful_transactions=success_tx,
        failed_transactions=failed_tx,
        pending_transactions=pending_tx,
        total_simulated_disbursed=total_disbursed,
        allocated_budget=allocated_budget,
        remaining_budget=remaining_budget,
        notice="DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED."
    )

@router.get("/beneficiaries", response_model=List[BeneficiaryResponse])
def list_beneficiaries(
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}

    query = db.query(Beneficiary)
    if role not in admin_roles:
        # Citizen role: strictly restrict to their own citizen_id
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        query = query.filter(Beneficiary.citizen_id == citizen_id)
    
    if scheme_id:
        query = query.filter(Beneficiary.scheme_id == scheme_id)
    if status_filter:
        query = query.filter(Beneficiary.status == status_filter.upper())
    return query.order_by(Beneficiary.id.desc()).offset(skip).limit(limit).all()

@router.get("/beneficiaries/{beneficiary_id}", response_model=BeneficiaryResponse)
def get_beneficiary_details(
    beneficiary_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ben = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary record not found")

    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}
    if role not in admin_roles:
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        if ben.citizen_id != citizen_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You are not authorized to view another citizen's beneficiary record."
            )
    return ben

@router.get("/dbt/transactions", response_model=List[DbtTransactionResponse])
def list_dbt_transactions(
    beneficiary_id: Optional[int] = None,
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}
    query = db.query(DbtTransaction)
    if role not in admin_roles:
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        query = query.join(Beneficiary, DbtTransaction.beneficiary_id == Beneficiary.id).filter(Beneficiary.citizen_id == citizen_id)
    if beneficiary_id:
        query = query.filter(DbtTransaction.beneficiary_id == beneficiary_id)
    if scheme_id:
        query = query.filter(DbtTransaction.scheme_id == scheme_id)
    if status_filter:
        query = query.filter(DbtTransaction.status == status_filter.upper())

    records = query.order_by(DbtTransaction.id.desc()).offset(skip).limit(limit).all()

    # Enrich response with metadata for display
    enriched = []
    for tx in records:
        tx_dict = {
            "id": tx.id,
            "transaction_reference": tx.transaction_reference,
            "batch_reference": tx.batch_reference,
            "beneficiary_id": tx.beneficiary_id,
            "scheme_id": tx.scheme_id,
            "amount": float(tx.amount),
            "payment_mode": tx.payment_mode,
            "status": tx.status,
            "bank_account_last4": tx.bank_account_last4,
            "ifsc_code": tx.ifsc_code,
            "processed_at": tx.processed_at,
            "remarks": tx.remarks,
            "beneficiary_name": tx.beneficiary.citizen_name if tx.beneficiary else "Unknown Beneficiary",
            "scheme_name": tx.scheme.name if tx.scheme else "Welfare Scheme",
            "application_number": tx.beneficiary.application.application_number if (tx.beneficiary and tx.beneficiary.application) else "N/A"
        }
        enriched.append(DbtTransactionResponse(**tx_dict))

    return enriched

@router.post("/dbt/process", response_model=DbtTransactionResponse)
def process_dbt_payment(
    req: DbtProcessRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN"]))
):
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == req.beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")

    app = beneficiary.application

    # Duplicate check: check if already successfully paid for this beneficiary
    existing_success = db.query(DbtTransaction).filter(
        DbtTransaction.beneficiary_id == beneficiary.id,
        DbtTransaction.status == "SUCCESSFUL"
    ).first()
    if existing_success:
        raise HTTPException(
            status_code=400,
            detail=f"Duplicate payment prevented: Beneficiary already received simulated payment under reference {existing_success.transaction_reference}."
        )

    tx_ref = f"SIM-DBT-{datetime.utcnow().year}-{os.urandom(4).hex().upper()}"
    bank_last4 = app.bank_account_number[-4:] if (app and app.bank_account_number) else "9999"
    ifsc = app.bank_ifsc if (app and app.bank_ifsc) else "SBIN0040123"

    is_failure = bool(req.simulate_failure)
    tx_status = "FAILED" if is_failure else "SUCCESSFUL"
    remarks_text = "Simulated Payment Failed: Bank CBS timeout simulation" if is_failure else (req.remarks or "Simulated Payment Successful")

    tx = DbtTransaction(
        transaction_reference=tx_ref,
        batch_reference=None,
        beneficiary_id=beneficiary.id,
        scheme_id=beneficiary.scheme_id,
        amount=beneficiary.sanctioned_amount,
        payment_mode="SIMULATED_AADHAAR_BRIDGE",
        status=tx_status,
        bank_account_last4=bank_last4,
        ifsc_code=ifsc,
        processed_at=datetime.utcnow(),
        initiated_by=current_user.get("sub", "SWD_ADMIN"),
        remarks=remarks_text
    )
    db.add(tx)

    if not is_failure and app:
        app.status = "BENEFIT_PROCESSED"

    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "ADMINISTRATOR"),
        action="SIMULATED_DBT_SINGLE",
        entity_type="BENEFICIARY",
        entity_id=str(beneficiary.id),
        details={"transaction_reference": tx_ref, "status": tx_status, "amount": float(beneficiary.sanctioned_amount)}
    )
    db.add(audit)

    db.commit()
    db.refresh(tx)

    return DbtTransactionResponse(
        id=tx.id,
        transaction_reference=tx.transaction_reference,
        batch_reference=tx.batch_reference,
        beneficiary_id=tx.beneficiary_id,
        scheme_id=tx.scheme_id,
        amount=float(tx.amount),
        payment_mode=tx.payment_mode,
        status=tx.status,
        bank_account_last4=tx.bank_account_last4,
        ifsc_code=tx.ifsc_code,
        processed_at=tx.processed_at,
        remarks=tx.remarks,
        beneficiary_name=beneficiary.citizen_name,
        scheme_name=beneficiary.scheme.name if beneficiary.scheme else "Welfare Scheme",
        application_number=app.application_number if app else "N/A"
    )

@router.post("/dbt/batch-process", response_model=DbtBatchProcessResponse)
def process_batch_dbt_payments(
    req: DbtBatchProcessRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN"]))
):
    """
    Simulated Batch Direct Benefit Transfer (DBT) payment engine.
    Processes selected approved beneficiaries with atomic safeguards and per-item status tracking.
    """
    if not req.beneficiary_ids:
        raise HTTPException(status_code=400, detail="No beneficiaries selected for batch DBT processing")

    batch_ref = f"BATCH-DBT-{datetime.utcnow().year}-{os.urandom(3).hex().upper()}"
    results: List[DbtBatchProcessResultItem] = []
    successful_count = 0
    failed_count = 0
    total_amount_disbursed = 0.0

    fail_set = set(req.fail_beneficiary_ids or [])

    for b_id in req.beneficiary_ids:
        beneficiary = db.query(Beneficiary).filter(Beneficiary.id == b_id).first()
        if not beneficiary:
            continue

        app = beneficiary.application
        app_num = app.application_number if app else "N/A"
        scheme_title = beneficiary.scheme.name if beneficiary.scheme else "Welfare Scheme"
        amt = float(beneficiary.sanctioned_amount)

        # Check duplicate payment for this cycle
        existing_paid = db.query(DbtTransaction).filter(
            DbtTransaction.beneficiary_id == beneficiary.id,
            DbtTransaction.status == "SUCCESSFUL"
        ).first()

        if existing_paid:
            results.append(DbtBatchProcessResultItem(
                beneficiary_id=beneficiary.id,
                beneficiary_name=beneficiary.citizen_name,
                application_number=app_num,
                scheme_name=scheme_title,
                amount=amt,
                transaction_reference=existing_paid.transaction_reference,
                status="FAILED",
                remarks=f"Simulated Payment Failed: Duplicate payment blocked. Already disbursed under {existing_paid.transaction_reference}."
            ))
            failed_count += 1
            continue

        # Simulate intentional failure if requested, or process success
        is_sim_fail = (beneficiary.id in fail_set)
        tx_ref = f"SIM-DBT-{datetime.utcnow().year}-{os.urandom(4).hex().upper()}"
        bank_last4 = app.bank_account_number[-4:] if (app and app.bank_account_number) else "8888"
        ifsc = app.bank_ifsc if (app and app.bank_ifsc) else "SBIN0040123"

        if is_sim_fail:
            tx_status = "FAILED"
            tx_remark = "Simulated Payment Failed: Beneficiary bank account unseeded with Aadhaar"
            failed_count += 1
        else:
            tx_status = "SUCCESSFUL"
            tx_remark = "Simulated Payment Successful: Aadhaar Payment Bridge cleared"
            successful_count += 1
            total_amount_disbursed += amt

            if app:
                app.status = "BENEFIT_PROCESSED"

        tx = DbtTransaction(
            transaction_reference=tx_ref,
            batch_reference=batch_ref,
            beneficiary_id=beneficiary.id,
            scheme_id=beneficiary.scheme_id,
            amount=amt,
            payment_mode="SIMULATED_AADHAAR_BRIDGE",
            status=tx_status,
            bank_account_last4=bank_last4,
            ifsc_code=ifsc,
            processed_at=datetime.utcnow(),
            initiated_by=current_user.get("sub", "SWD_ADMIN"),
            remarks=tx_remark
        )
        db.add(tx)

        results.append(DbtBatchProcessResultItem(
            beneficiary_id=beneficiary.id,
            beneficiary_name=beneficiary.citizen_name,
            application_number=app_num,
            scheme_name=scheme_title,
            amount=amt,
            transaction_reference=tx_ref,
            status=tx_status,
            remarks=tx_remark
        ))

    # Commit all ledger entries
    db.commit()

    return DbtBatchProcessResponse(
        batch_reference=batch_ref,
        total_processed=len(results),
        successful_count=successful_count,
        failed_count=failed_count,
        total_amount_disbursed=total_amount_disbursed,
        processed_at=datetime.utcnow(),
        notice="DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED.",
        results=results
    )

@router.get("/dbt/batch-report")
def export_batch_dbt_report(
    batch_reference: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN"]))
):
    """Generates downloadable CSV report for simulated DBT transactions."""
    query = db.query(DbtTransaction)
    if batch_reference:
        query = query.filter(DbtTransaction.batch_reference == batch_reference)

    records = query.order_by(DbtTransaction.id.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Batch Reference",
        "Transaction Reference",
        "Application Number",
        "Beneficiary Name",
        "Scheme Name",
        "Amount (INR)",
        "Processing Date & Time (UTC)",
        "Transaction Status",
        "Bank Last 4",
        "IFSC",
        "Remarks / Failure Reason",
        "Notice"
    ])

    for tx in records:
        app_num = tx.beneficiary.application.application_number if (tx.beneficiary and tx.beneficiary.application) else "N/A"
        ben_name = tx.beneficiary.citizen_name if tx.beneficiary else "Unknown"
        scheme_name = tx.scheme.name if tx.scheme else "Welfare Scheme"

        writer.writerow([
            tx.batch_reference or "INDIVIDUAL_TX",
            tx.transaction_reference,
            app_num,
            ben_name,
            scheme_name,
            f"{float(tx.amount):.2f}",
            tx.processed_at.strftime("%Y-%m-%d %H:%M:%S"),
            tx.status,
            tx.bank_account_last4 or "",
            tx.ifsc_code or "",
            tx.remarks or "",
            "DEMO MODE — SIMULATED DBT TRANSACTION. NO REAL MONEY TRANSFERRED."
        ])

    csv_data = output.getvalue()
    filename = f"simulated_dbt_report_{batch_reference or 'all'}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
