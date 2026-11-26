import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.models import (
    Scheme, SchemeApplication, ApplicationHistory, 
    Beneficiary, AuditLog, DbtTransaction, Grievance, Notification
)
from app.schemas import (
    AdminDashboardStats, ApplicationResponse, 
    RequestInformationRequest, ApplicationDecisionRequest,
    BeneficiaryResponse, DepartmentAnnouncementRequest
)
from app.core.security import require_role
from app.events.rabbitmq_publisher import publish_event_to_broker

router = APIRouter(prefix="/api/swd/admin", tags=["SWD Administration"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]


@router.get("/dashboard", response_model=AdminDashboardStats)
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    # Exclude Shakti and temporarily hidden schemes from active catalogue metrics
    swd_schemes_q = db.query(Scheme).filter(
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    )
    total_schemes = swd_schemes_q.count()
    published_schemes = swd_schemes_q.filter(Scheme.status == "PUBLISHED").count()
    draft_schemes = swd_schemes_q.filter(Scheme.status == "DRAFT").count()
    closed_schemes = swd_schemes_q.filter(Scheme.status == "CLOSED").count()

    total_apps = db.query(SchemeApplication).count()
    submitted_apps = db.query(SchemeApplication).filter(SchemeApplication.status == "SUBMITTED").count()
    under_review_apps = db.query(SchemeApplication).filter(SchemeApplication.status == "UNDER_REVIEW").count()
    more_info_apps = db.query(SchemeApplication).filter(SchemeApplication.status.in_(["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED"])).count()
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
    category_id: Optional[int] = None,
    district: Optional[str] = None,
    search: Optional[str] = None,
    is_duplicate_only: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    query = db.query(SchemeApplication)

    if category_id:
        query = query.filter(SchemeApplication.scheme.has(Scheme.category_id == category_id))
    if status_filter:
        sf = status_filter.upper()
        if sf in ["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "ACTION_REQUIRED"]:
            query = query.filter(SchemeApplication.status.in_(["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED"]))
        elif sf in ["APPROVED", "BENEFIT_PROCESSED"]:
            query = query.filter(SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"]))
        else:
            query = query.filter(SchemeApplication.status == sf)
    if scheme_id:
        query = query.filter(SchemeApplication.scheme_id == scheme_id)
    if district:
        query = query.filter(SchemeApplication.residence_district.ilike(f"%{district}%"))
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (SchemeApplication.application_number.ilike(search_fmt)) |
            (SchemeApplication.citizen_name.ilike(search_fmt)) |
            (SchemeApplication.citizen_id.ilike(search_fmt))
        )
    if is_duplicate_only:
        query = query.filter(SchemeApplication.is_duplicate_suspect == True)

    return query.order_by(SchemeApplication.id.desc()).offset(skip).limit(limit).all()

@router.get("/officer/assigned-applications", response_model=List[ApplicationResponse])
def get_officer_assigned_applications(
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["WELFARE_OFFICER", "ADMINISTRATOR", "GOVERNMENT_WELFARE_ADMIN"]))
):
    """
    Dedicated endpoint for Welfare Officers to inspect applications under their jurisdiction/scrutiny.
    """
    query = db.query(SchemeApplication)
    if status_filter:
        sf = status_filter.upper()
        if sf in ["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "ACTION_REQUIRED"]:
            query = query.filter(SchemeApplication.status.in_(["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED"]))
        elif sf in ["APPROVED", "BENEFIT_PROCESSED"]:
            query = query.filter(SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"]))
        else:
            query = query.filter(SchemeApplication.status == sf)
    return query.order_by(SchemeApplication.id.desc()).offset(skip).limit(limit).all()

@router.post("/applications/{application_id}/request-information", response_model=ApplicationResponse)
def request_more_information(
    application_id: int,
    req_in: RequestInformationRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
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

    # Citizen Notification
    notif = Notification(
        user_id=app_record.citizen_id,
        title=f"Action Required: Application {app_record.application_number}",
        message=f"Additional documents or clarification requested: {req_in.remarks}",
        notification_type="WARNING"
    )
    db.add(notif)

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

@router.post("/applications/{application_id}/review", response_model=ApplicationResponse)
def review_application_status(
    application_id: int,
    status_update: ApplicationDecisionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    target_status = status_update.decision.upper()
    valid_statuses = ["UNDER_REVIEW", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED", "DOCUMENTS_REQUIRED", "APPROVED", "REJECTED"]
    if target_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{target_status}'. Must be one of: {', '.join(valid_statuses)}"
        )

    old_status = app_record.status
    app_record.status = target_status
    app_record.admin_remarks = status_update.remarks

    # Add history
    hist = ApplicationHistory(
        application_id=app_record.id,
        from_status=old_status,
        to_status=target_status,
        changed_by=current_user.get("name", current_user.get("sub", "SWD_OFFICER")),
        action_type="OFFICER_REVIEW",
        remarks=status_update.remarks
    )
    db.add(hist)

    # If APPROVED, execute duplicate entitlement verification and create beneficiary record
    if target_status == "APPROVED":
        scheme = app_record.scheme
        # Duplicate Entitlement Guard: Check if citizen already has an ACTIVE beneficiary entitlement for this scheme
        dup_entitlement = db.query(Beneficiary).filter(
            Beneficiary.citizen_id == app_record.citizen_id,
            Beneficiary.scheme_id == app_record.scheme_id,
            Beneficiary.status == "ACTIVE"
        ).first()

        # If scheme enforces single active entitlement and one already exists from another application
        is_dup_check_on = getattr(scheme, "is_duplicate_check_enabled", True)
        if dup_entitlement and is_dup_check_on and dup_entitlement.application_id != app_record.id:
            # Prevent multiple beneficiary entitlements for the same citizen & scheme
            # Log security & audit decision
            audit_dup = AuditLog(
                actor_id=current_user.get("name", current_user.get("sub", "SWD_OFFICER")),
                actor_role=current_user.get("role", "OFFICER"),
                action="DUPLICATE_ENTITLEMENT_PREVENTED",
                entity_type="APPLICATION",
                entity_id=str(app_record.id),
                details={
                    "citizen_id": app_record.citizen_id,
                    "scheme_id": app_record.scheme_id,
                    "existing_beneficiary_id": dup_entitlement.id,
                    "existing_application_id": dup_entitlement.application_id,
                    "remarks": "Beneficiary entitlement already exists for this citizen and scheme. Secondary payment mandate creation prevented."
                }
            )
            db.add(audit_dup)
        else:
            existing_ben = db.query(Beneficiary).filter(Beneficiary.application_id == app_record.id).first()
            if not existing_ben:
                sanction_amount = status_update.sanctioned_amount or float(scheme.benefit_amount or 10000.0) if scheme else 10000.0
                ben_code = f"BEN-{datetime.utcnow().year}-SWD-{os.urandom(3).hex().upper()}"

                beneficiary = Beneficiary(
                    beneficiary_code=ben_code,
                    application_id=app_record.id,
                    scheme_id=app_record.scheme_id,
                    citizen_id=app_record.citizen_id,
                    citizen_name=app_record.citizen_name,
                    sanctioned_amount=sanction_amount,
                    disbursement_mode=status_update.disbursement_mode or "DIRECT_BENEFIT_TRANSFER",
                    status="ACTIVE",
                    sanctioned_by=current_user.get("name", current_user.get("sub", "SWD_OFFICER"))
                )
                db.add(beneficiary)

    # Dispatch Citizen Notification
    notif_type = "SUCCESS" if target_status == "APPROVED" else ("ERROR" if target_status == "REJECTED" else "INFO")
    notif = Notification(
        user_id=app_record.citizen_id,
        title=f"Application {app_record.application_number} Updated: {target_status.replace('_', ' ')}",
        message=f"Remarks from Welfare Officer: {status_update.remarks}",
        notification_type=notif_type
    )
    db.add(notif)

    # Audit Log
    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_OFFICER"),
        actor_role=current_user.get("role", "OFFICER"),
        action=f"REVIEW_{target_status}",
        entity_type="APPLICATION",
        entity_id=str(app_record.id),
        details={"status": target_status, "remarks": status_update.remarks}
    )
    db.add(audit)

    db.commit()
    db.refresh(app_record)

    publish_event_to_broker(
        event_type="SCHEME_APPLICATION_UPDATED",
        correlation_id=app_record.application_number,
        payload={"application_id": app_record.id, "status": app_record.status, "decision": target_status}
    )

    return app_record

@router.post("/applications/{application_id}/decision", response_model=ApplicationResponse)
def record_application_decision(
    application_id: int,
    decision_in: ApplicationDecisionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    return review_application_status(application_id, decision_in, db, current_user)


# ------------------------------------------------------------------------------
# Category-Wise Live Application Metrics (Mandatory Requirement)
# ------------------------------------------------------------------------------
@router.get("/categories/stats")
def get_category_application_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    """
    Returns live application metrics for every scheme category from MySQL:
    - total_applications
    - new_submitted
    - under_review
    - documents_required
    - approved
    - rejected
    - list of schemes with scheme-wise application breakdown
    """
    from app.models import SchemeCategory
    categories = db.query(SchemeCategory).filter(SchemeCategory.is_active == True).all()

    result = []
    for cat in categories:
        # Applications in this category
        cat_apps = db.query(SchemeApplication).filter(
            SchemeApplication.scheme.has(Scheme.category_id == cat.id)
        )
        total_count = cat_apps.count()
        new_count = cat_apps.filter(SchemeApplication.status == "SUBMITTED").count()
        under_review_count = cat_apps.filter(SchemeApplication.status == "UNDER_REVIEW").count()
        docs_required_count = cat_apps.filter(SchemeApplication.status.in_(["DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED", "MORE_INFORMATION_REQUIRED"])).count()
        approved_count = cat_apps.filter(SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"])).count()
        rejected_count = cat_apps.filter(SchemeApplication.status == "REJECTED").count()

        # Scheme-wise breakdown in this category (excluding Shakti and hidden schemes)
        schemes_in_cat = db.query(Scheme).filter(
            Scheme.category_id == cat.id,
            ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
            ~Scheme.scheme_code.ilike("%SHAKTI%"),
            ~Scheme.name.ilike("%SHAKTI%")
        ).all()
        scheme_breakdown = []
        for sc in schemes_in_cat:
            sc_apps = db.query(SchemeApplication).filter(SchemeApplication.scheme_id == sc.id)
            scheme_breakdown.append({
                "scheme_id": sc.id,
                "scheme_code": sc.scheme_code,
                "scheme_name": sc.name,
                "application_mode": "ONLINE_FORM",
                "total_applications": sc_apps.count(),
                "submitted": sc_apps.filter(SchemeApplication.status == "SUBMITTED").count(),
                "under_review": sc_apps.filter(SchemeApplication.status == "UNDER_REVIEW").count(),
                "documents_required": sc_apps.filter(SchemeApplication.status.in_(["DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED", "MORE_INFORMATION_REQUIRED"])).count(),
                "approved": sc_apps.filter(SchemeApplication.status.in_(["APPROVED", "BENEFIT_PROCESSED"])).count(),
                "rejected": sc_apps.filter(SchemeApplication.status == "REJECTED").count()
            })

        result.append({
            "category_id": cat.id,
            "category_code": cat.code,
            "category_name": cat.name,
            "description": cat.description,
            "icon": cat.icon or "Shield",
            "total_applications": total_count,
            "new_applications": new_count,
            "under_review": under_review_count,
            "documents_required": docs_required_count,
            "approved": approved_count,
            "rejected": rejected_count,
            "schemes": scheme_breakdown
        })

    return result


# ------------------------------------------------------------------------------
# Platform Admin: User & Officer Management
# ------------------------------------------------------------------------------
@router.get("/users")
def list_platform_users(
    role_filter: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    from app.models import User
    query = db.query(User)
    if role_filter:
        query = query.filter(User.role == role_filter.upper())
    if search:
        s_fmt = f"%{search}%"
        query = query.filter((User.full_name.ilike(s_fmt)) | (User.email.ilike(s_fmt)) | (User.citizen_id.ilike(s_fmt)))
    
    users = query.order_by(User.id.desc()).all()
    return [
        {
            "id": u.id,
            "citizen_id": u.citizen_id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "phone": u.phone,
            "district": u.district,
            "taluk": u.taluk,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

@router.put("/users/{user_id}/status")
def toggle_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Platform Admin has view-only monitoring permissions. Managing citizen or user account status is disabled."
    )

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Platform Admin has view-only monitoring permissions. Modifying citizen or officer roles is disabled."
    )

@router.get("/audit-logs")
def get_audit_logs(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["SWD_ADMIN", "PLATFORM_ADMIN"]))
):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
    return logs



@router.post("/announcements")
def publish_department_announcement(
    req: DepartmentAnnouncementRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    """Welfare Admin: Publish an official department announcement and dispatch notifications to citizens."""
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Publishing announcements is disabled."
        )
    from app.models import User
    # Query target citizens
    target_role = (req.target_role or "CITIZEN").upper()
    citizens = db.query(User).filter(User.role == target_role, User.is_active == True).all()
    count = 0
    for c in citizens:
        notif = Notification(
            user_id=c.citizen_id,
            title=f"Official Announcement: {req.title}",
            message=req.message,
            notification_type=req.announcement_type or "INFO"
        )
        db.add(notif)
        count += 1
    
    # Audit log
    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_OFFICER"),
        actor_role=current_user.get("role", "OFFICER"),
        action="PUBLISH_ANNOUNCEMENT",
        entity_type="ANNOUNCEMENT",
        entity_id=str(count),
        details={"title": req.title, "target_role": target_role, "recipient_count": count}
    )
    db.add(audit)
    db.commit()
    
    return {
        "status": "success",
        "message": f"Official announcement published. Notifications dispatched to {count} registered citizens.",
        "recipients_count": count
    }
