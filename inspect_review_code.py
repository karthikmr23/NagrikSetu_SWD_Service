# Check backend notification mechanisms for decisions (REJECTED, DOCUMENTS_REQUIRED)
with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def review_application_status" in line:
        for j in range(i, min(i+110, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
        break
