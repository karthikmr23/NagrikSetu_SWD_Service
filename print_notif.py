path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Line 4500 to 4565:")
for i in range(4499, 4565):
    print(f"{i+1}: {lines[i]}", end="")
