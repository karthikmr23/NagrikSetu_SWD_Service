with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\grievances.py", "r", encoding="utf-8") as f:
    text = f.read()

# Add verify_citizen_ownership to imports
old_import = "from app.core.security import get_current_user, require_role"
new_import = "from app.core.security import get_current_user, require_role, verify_citizen_ownership"

if old_import in text:
    text = text.replace(old_import, new_import)

old_list_g = """@router.get("/grievances", response_model=List[GrievanceResponse])
def list_grievances(
    citizen_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):"""

new_list_g = """@router.get("/grievances", response_model=List[GrievanceResponse])
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
        citizen_id = current_cit_id"""

if old_list_g in text:
    text = text.replace(old_list_g, new_list_g)
    print("Replaced list_grievances in grievances.py")

old_submit_g = """@router.post("/grievances", response_model=GrievanceResponse)
def submit_grievance(
    req: GrievanceCreateRequest,
    db: Session = Depends(get_db)
):"""

new_submit_g = """@router.post("/grievances", response_model=GrievanceResponse)
def submit_grievance(
    req: GrievanceCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verify citizen identity
    verify_citizen_ownership(req.citizen_id, current_user)"""

if old_submit_g in text:
    text = text.replace(old_submit_g, new_submit_g)
    print("Replaced submit_grievance in grievances.py")

old_notifs = """@router.get("/notifications/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(user_id: str, db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.id.desc()).limit(50).all()"""

new_notifs = """@router.get("/notifications/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(
    user_id: str, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    verify_citizen_ownership(user_id, current_user)
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.id.desc()).limit(50).all()"""

if old_notifs in text:
    text = text.replace(old_notifs, new_notifs)
    print("Replaced get_user_notifications in grievances.py")

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\grievances.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated grievances.py successfully")
