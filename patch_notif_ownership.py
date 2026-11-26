import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\grievances.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

target = """@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

@router.post("/notifications/{user_id}/mark-all-read")
def mark_all_notifications_read(user_id: str, db: Session = Depends(get_db)):
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({Notification.is_read: True})
    db.commit()
    return {"status": "success", "message": f"All notifications for {user_id} marked as read"}"""

replacement = """@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
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
    return {"status": "success", "message": f"All notifications for {user_id} marked as read"}"""

assert target in code, "Target not found in grievances.py"
code = code.replace(target, replacement)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("grievances.py updated with ownership validation!")
