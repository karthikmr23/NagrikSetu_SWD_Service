import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.models import (
    Scheme, SchemeApplication, ApplicationHistory, 
    Beneficiary, AuditLog, DbtTransaction, Grievance
)
from app.schemas import (
    AdminDashboardStats, ApplicationResponse, 
    RequestInformationRequest, ApplicationDecisionRequest,
    BeneficiaryResponse
)
from app.core.security import require_role
from app.events.rabbitmq_publisher import publish_event_to_broker

router = APIRouter(prefix="/api/swd/admin", tags=["SWD Administration"])

@router.get("/dashboard", response_model=AdminDashboardStats)
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    total_schemes = db.query(Scheme).count()
    published_schemes = db.query(Scheme).filter(Scheme.status == "PUBLISHED").count()
    draft_schemes = db.query(Scheme).filter(Scheme.status == "DRAFT").count()
    closed_schemes = db.query(Scheme).filter(Scheme.status == "CLOSED").count()

    total_apps = db.query(SchemeApplication).count()
    submitted_apps = db.query(SchemeApplication).filter(SchemeApplication.status == "SUBMITTED").count()
    under_review_apps = db.query(SchemeApplication).filter(SchemeApplication.status == "UNDER_REVIEW").count()
    more_info_apps = db.query(SchemeApplication).filter(SchemeApplication.status.in_(["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED"])).count()
    approved_apps = db.query(SchemeApplication).filter(SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"])).count()
    rejected_apps = db.query(SchemeApplication).filter(SchemeApplication.status == "REJECTED").count()

    total_bens = db.query(Beneficiary).count()
    total_amount = db.query(func.sum(Beneficiary.sanctioned_amount)).scalar() or 0.0
    total_dbt = db.query(func.sum(DbtTransaction.amount)).filter(DbtTransaction.status == "SUCCESSFUL").scalar() or 0.0

    total_grievances = db.query(Grievance).count()
    pending_grievances = db.query(Grievance).filter(Grievance.status.in_(["SUBMITTED", "UNDER_INVESTIGATION"])).count()

    recent_applications = db.query(SchemeApplication).order_by(SchemeApplication.id.desc()).limit(10).all()

    return AdminDashboardStats(
        total_schemes=total_schemes,
        published_schemes=published_schemes,
        draft_schemes=draft_schemes,
        closed_schemes=closed_schemes,
        total_applications=total_apps,
        submitted_applications=submitted_apps,
        under_review_applications=under_review_apps,
        more_info_required_applications=more_info_apps,
        approved_applications=approved_apps,
        rejected_applications=rejected_apps,
        total_beneficiaries=total_bens,
        total_sanctioned_amount=float(total_amount),
        total_dbt_disbursed=float(total_dbt),
        total_grievances=total_grievances,
        pending_grievances=pending_grievances,
        recent_applications=recent_applications
    )

@router.get("/applications", response_model=List[ApplicationResponse])
def list_admin_applications(
    status_filter: Optional[str] = None,
    scheme_id: Optional[int] = None,
    is_duplicate_only: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    query = db.query(SchemeApplication)

    if status_filter:
        query = query.filter(SchemeApplication.status == status_filter.upper())
    if scheme_id:
        query = query.filter(SchemeApplication.scheme_id == scheme_id)
    if is_duplicate_only:
        query = query.filter(SchemeApplication.is_duplicate_suspect == True)

@router.get("/officer/assigned-applications", response_model=List[ApplicationResponse])
def get_officer_assigned_applications(
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["WELFARE_OFFICER", "ADMINISTRATOR", "SWD_ADMIN"]))
):
    """
    Dedicated endpoint for Welfare Officers to inspect applications under their jurisdiction/scrutiny.
    """
    query = db.query(SchemeApplication)
    if status_filter:
        query = query.filter(SchemeApplication.status == status_filter.upper())
    return query.order_by(SchemeApplication.id.desc()).offset(skip).limit(limit).all()

@router.post("/applications/{application_id}/request-information", response_model=ApplicationResponse)
def request_more_information(
    application_id: int,
    req_in: RequestInformationRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    old_status = app_record.status
    app_record.status = "DOCUMENTS_REQUIRED"
    app_record.admin_remarks = req_in.remarks

    # Create history entry
    hist = ApplicationHistory(
        application_id=app_record.id,
        from_status=old_status,
        to_status="DOCUMENTS_REQUIRED",
        changed_by=current_user.get("name", current_user.get("sub", "SWD_OFFICER")),
        action_type="REQUEST_INFORMATION",
        remarks=req_in.remarks
    )
    db.add(hist)

    # Audit
    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_OFFICER"),
        actor_role=current_user.get("role", "OFFICER"),
        action="REQUEST_INFO",
        entity_type="APPLICATION",
        entity_id=str(app_record.id),
        details={"remarks": req_in.remarks}
    )
    db.add(audit)

    db.commit()
    db.refresh(app_record)

    publish_event_to_broker(
        event_type="SCHEME_APPLICATION_UPDATED",
        correlation_id=app_record.application_number,
        payload={"application_id": app_record.id, "status": app_record.status, "action": "MORE_INFO_REQUESTED"}
    )

    return app_record

@router.post("/applications/{application_id}/decision", response_model=ApplicationResponse)
def record_application_decision(
    application_id: int,
    decision_in: ApplicationDecisionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    decision = decision_in.decision.upper()
    if decision not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Decision must be either 'APPROVED' or 'REJECTED'")

    old_status = app_record.status
    app_record.status = decision
    app_record.admin_remarks = decision_in.remarks

    # Add history
    hist = ApplicationHistory(
        application_id=app_record.id,
        from_status=old_status,
        to_status=decision,
        changed_by=current_user.get("name", current_user.get("sub", "SWD_OFFICER")),
        action_type="OFFICER_DECISION",
        remarks=decision_in.remarks
    )
    db.add(hist)

    # If APPROVED, create or update beneficiary record
    if decision == "APPROVED":
        existing_ben = db.query(Beneficiary).filter(Beneficiary.application_id == app_record.id).first()
        if not existing_ben:
            scheme = app_record.scheme
            sanction_amount = decision_in.sanctioned_amount or float(scheme.benefit_amount or 10000.0)
            ben_code = f"BEN-{datetime.utcnow().year}-SWD-{os.urandom(3).hex().upper()}"

            beneficiary = Beneficiary(
                beneficiary_code=ben_code,
                application_id=app_record.id,
                scheme_id=app_record.scheme_id,
                citizen_id=app_record.citizen_id,
                citizen_name=app_record.citizen_name,
                sanctioned_amount=sanction_amount,
                disbursement_mode=decision_in.disbursement_mode or "DIRECT_BENEFIT_TRANSFER",
                status="ACTIVE",
                sanctioned_by=current_user.get("name", current_user.get("sub", "SWD_OFFICER"))
            )
            db.add(beneficiary)

    # Audit
    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_OFFICER"),
        actor_role=current_user.get("role", "OFFICER"),
        action=f"DECISION_{decision}",
        entity_type="APPLICATION",
        entity_id=str(app_record.id),
        details={"decision": decision, "remarks": decision_in.remarks}
    )
    db.add(audit)

    db.commit()
    db.refresh(app_record)

    publish_event_to_broker(
        event_type="SCHEME_APPLICATION_UPDATED",
        correlation_id=app_record.application_number,
        payload={"application_id": app_record.id, "status": app_record.status, "decision": decision}
    )

    return app_record
