path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Lines 4300-4560 preview:")
for i in range(4299, 4565):
    if i < len(lines):
        if "activeTab === 'grievance'" in lines[i] or "activeTab === 'my-grievances'" in lines[i] or "activeTab === 'notifications-view'" in lines[i] or "VIEW:" in lines[i]:
            print(f"Line {i+1}: {lines[i].strip()}")
