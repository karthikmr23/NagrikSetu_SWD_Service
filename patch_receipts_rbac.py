with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\receipts.py", "r", encoding="utf-8") as f:
    text = f.read()

# Add get_current_user and verify_citizen_ownership to imports
old_import = "from app.models import SchemeApplication, Scheme"
new_import = """from app.models import SchemeApplication, Scheme
from app.core.security import get_current_user, verify_citizen_ownership"""

old_endpoint = """@router.get("/applications/{application_id}/receipt")
def generate_application_receipt(application_id: int, db: Session = Depends(get_db)):
    # 1. Fetch application and scheme
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Scheme application record not found")"""

new_endpoint = """@router.get("/applications/{application_id}/receipt")
def generate_application_receipt(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. Fetch application and scheme
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Scheme application record not found")

    # Strictly verify that citizens can only download their own receipts
    verify_citizen_ownership(app_record.citizen_id, current_user)"""

if old_import in text:
    text = text.replace(old_import, new_import)
    print("Replaced import in receipts.py")

if old_endpoint in text:
    text = text.replace(old_endpoint, new_endpoint)
    print("Replaced endpoint in receipts.py")

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\receipts.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated receipts.py successfully")
