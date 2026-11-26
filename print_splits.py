path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Line 4425 to 4435:")
for i in range(4424, 4435):
    print(f"{i+1}: {lines[i]}", end="")

print("\nLine 4492 to 4505:")
for i in range(4491, 4505):
    print(f"{i+1}: {lines[i]}", end="")
