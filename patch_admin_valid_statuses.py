path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = 'valid_statuses = ["UNDER_REVIEW", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED", "APPROVED", "REJECTED"]'
replacement = 'valid_statuses = ["UNDER_REVIEW", "AWAITING_DOCUMENTS", "CORRECTION_REQUIRED", "DOCUMENTS_REQUIRED", "APPROVED", "REJECTED"]'

if target in content:
    content = content.replace(target, replacement)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Updated valid_statuses in admin.py")
else:
    print("WARNING: target not found")
