# Update backend_full_audit.py and other test scripts to expect 34 SWD schemes (since Shakti is excluded)

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend_full_audit.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Update T02 expectation from 35 to 34
code = code.replace(
    "# 2. Scheme Catalogue (All 35 schemes)\n    status, data = get_json(\"/api/swd/schemes\")\n    passed = (status == 200 and len(data) == 35)",
    "# 2. Scheme Catalogue (All 34 valid SWD schemes, non-SWD Shakti excluded)\n    status, data = get_json(\"/api/swd/schemes\")\n    passed = (status == 200 and len(data) == 34)"
)

# Update T11 queue expectation from 35 to 34 or 35 apps (35 applications exist in DB)
with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("Updated backend_full_audit.py")
