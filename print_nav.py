path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Lines 1055-1250 preview:")
for i in range(1054, 1255):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end="")
