target_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\applications.py"

with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update form_version_id lookup from active form definition
old_form_version = """    # Generate unique application number
    app_num = f"SWD-APP-{datetime.utcnow().year}-{os.urandom(3).hex().upper()}"

    new_app = SchemeApplication(
        application_number=app_num,
        scheme_id=scheme_id,
        category_id=scheme.category_id,
        form_version_id=1,"""

new_form_version = """    # Find active form definition version if available
    active_form = db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id,
        DynamicFormDefinition.is_active == True
    ).first()
    active_version_id = active_form.version if active_form else 1

    # Generate unique application number
    app_num = f"SWD-APP-{datetime.utcnow().year}-{os.urandom(3).hex().upper()}"

    new_app = SchemeApplication(
        application_number=app_num,
        scheme_id=scheme_id,
        category_id=scheme.category_id,
        form_version_id=active_version_id,"""

# 2. Add DynamicFormDefinition to models import
old_import = """from app.models import (
    Scheme, SchemeApplication, ApplicationDocument,
    ApplicationHistory, Beneficiary, AuditLog
)"""

new_import = """from app.models import (
    Scheme, SchemeApplication, ApplicationDocument,
    ApplicationHistory, Beneficiary, AuditLog, DynamicFormDefinition
)"""

# 3. Allow status in ["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS"] to transition to UNDER_REVIEW
old_upload_trans = """    # If application was awaiting info, append remark in history
    if app_record.status == "MORE_INFORMATION_REQUIRED":
        hist = ApplicationHistory(
            application_id=app_record.id,
            from_status="MORE_INFORMATION_REQUIRED",
            to_status="UNDER_REVIEW",
            changed_by=app_record.citizen_id,
            action_type="DOCUMENT_UPLOAD",
            remarks=f"Citizen uploaded requested supplementary document: {doc_record.file_name}"
        )
        app_record.status = "UNDER_REVIEW"
        db.add(hist)"""

new_upload_trans = """    # If application was awaiting info/documents, transition back to UNDER_REVIEW and append history
    if app_record.status in ["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS"]:
        old_st = app_record.status
        hist = ApplicationHistory(
            application_id=app_record.id,
            from_status=old_st,
            to_status="UNDER_REVIEW",
            changed_by=app_record.citizen_id,
            action_type="DOCUMENT_UPLOAD",
            remarks=f"Citizen uploaded requested supplementary document: {doc_record.file_name}"
        )
        app_record.status = "UNDER_REVIEW"
        db.add(hist)"""

code = code.replace(old_import, new_import)
code = code.replace(old_form_version, new_form_version)
code = code.replace(old_upload_trans, new_upload_trans)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated applications.py successfully!")
