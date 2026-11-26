with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py", "r", encoding="utf-8") as f:
    text = f.read()

old_str = 'current_user: dict = Depends(require_role(["WELFARE_OFFICER", "ADMINISTRATOR", "SWD_ADMIN"]))'
new_str = 'current_user: dict = Depends(require_role(["WELFARE_OFFICER", "ADMINISTRATOR", "GOVERNMENT_WELFARE_ADMIN"]))'

if old_str in text:
    text = text.replace(old_str, new_str)
    with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully updated admin.py")
else:
    print("Could not find old_str in admin.py")
