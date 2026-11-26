import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Grievance, Notification, AuditLog
from app.schemas import (
    GrievanceCreateRequest, GrievanceUpdateRequest, GrievanceResponse,
    NotificationResponse
)
from app.core.security import get_current_user, require_role, verify_citizen_ownership

router = APIRouter(prefix="/api/swd", tags=["SWD Grievance & Citizen Services"])

@router.get("/grievances", response_model=List[GrievanceResponse])
def list_grievances(
    citizen_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}

    if role not in admin_roles:
        # Citizen role: strictly force citizen_id to current_user
        current_cit_id = current_user.get("citizen_id") or current_user.get("sub")
        citizen_id = current_cit_id
    query = db.query(Grievance)
    if citizen_id:
        query = query.filter(Grievance.citizen_id == citizen_id)
    if status_filter:
        query = query.filter(Grievance.status == status_filter.upper())
    return query.order_by(Grievance.id.desc()).offset(skip).limit(limit).all()

@router.post("/grievances", response_model=GrievanceResponse)
def submit_grievance(
    req: GrievanceCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verify citizen identity
    verify_citizen_ownership(req.citizen_id, current_user)
    g_num = f"GRV-SWD-{datetime.utcnow().year}-{os.urandom(3).hex().upper()}"
    new_g = Grievance(
        grievance_number=g_num,
        citizen_id=req.citizen_id,
        citizen_name=req.citizen_name,
        category=req.category,
        subject=req.subject,
        description=req.description,
        status="SUBMITTED"
    )
    db.add(new_g)

    # Add notification for the citizen
    notif = Notification(
        user_id=req.citizen_id,
        title="Grievance Registered",
        message=f"Your grievance {g_num} ({req.subject}) has been logged and assigned to the Social Welfare Department grievance cell.",
        notification_type="INFO"
    )
    db.add(notif)

    db.commit()
    db.refresh(new_g)
    return new_g

@router.put("/grievances/{grievance_id}/resolve", response_model=GrievanceResponse)
def resolve_grievance(
    grievance_id: int,
    req: GrievanceUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    g = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")

    g.status = req.status.upper()
    g.officer_response = req.officer_response
    g.resolved_by = current_user.get("name", current_user.get("sub", "SWD_OFFICER"))
    g.resolved_at = datetime.utcnow()

    # Citizen notification
    notif = Notification(
        user_id=g.citizen_id,
        title=f"Grievance {g.grievance_number} Status Updated",
        message=f"Official Welfare Officer Response: {req.officer_response} (Status: {g.status})",
        notification_type="SUCCESS"
    )
    db.add(notif)

    db.commit()
    db.refresh(g)
    return g

# ----------------- Notifications Management -----------------

@router.get("/notifications/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(
    user_id: str, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    verify_citizen_ownership(user_id, current_user)
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.id.desc()).limit(50).all()

@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    verify_citizen_ownership(notif.user_id, current_user)
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

@router.post("/notifications/{user_id}/mark-all-read")
def mark_all_notifications_read(
    user_id: str, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    verify_citizen_ownership(user_id, current_user)
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({Notification.is_read: True})
    db.commit()
    return {"status": "success", "message": f"All notifications for {user_id} marked as read"}
