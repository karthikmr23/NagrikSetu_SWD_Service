import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

old_import = """from app.schemas import (
    AdminDashboardStats, ApplicationResponse, 
    RequestInformationRequest, ApplicationDecisionRequest,
    BeneficiaryResponse
)"""
new_import = """from app.schemas import (
    AdminDashboardStats, ApplicationResponse, 
    RequestInformationRequest, ApplicationDecisionRequest,
    BeneficiaryResponse, DepartmentAnnouncementRequest
)"""

assert old_import in code, "old_import not found in admin.py"
code = code.replace(old_import, new_import)

endpoint_code = """

@router.post("/announcements")
def publish_department_announcement(
    req: DepartmentAnnouncementRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    \"\"\"Welfare Admin: Publish an official department announcement and dispatch notifications to citizens.\"\"\"
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
"""

code = code + endpoint_code

with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("admin.py updated with announcement endpoint!")
