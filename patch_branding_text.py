path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Main Header Branding
old_header_brand = """            <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.25rem' }}>
              NagrikSetu &bull; Social Welfare Module
            </h1>"""

new_header_brand = """            <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.25rem' }}>
              NagrikSetu &bull; Social Welfare Department
            </h1>"""

# 2. Footer Branding
old_footer_brand = """            <h4 style={{ color: '#ffffff', fontSize: '1rem', marginBottom: '0.35rem' }}>
              Social Welfare Module &bull; NagrikSetu
            </h4>"""

new_footer_brand = """            <h4 style={{ color: '#ffffff', fontSize: '1rem', marginBottom: '0.35rem' }}>
              Social Welfare Department &bull; NagrikSetu
            </h4>"""

count = 0
if old_header_brand in content:
    content = content.replace(old_header_brand, new_header_brand, 1)
    count += 1
    print("Replaced main header branding text.")
else:
    print("Warning: old_header_brand not found exactly.")

if old_footer_brand in content:
    content = content.replace(old_footer_brand, new_footer_brand, 1)
    count += 1
    print("Replaced footer branding text.")
else:
    print("Warning: old_footer_brand not found exactly.")

# Also check for any loose "Social Welfare Module"
if "Social Welfare Module" in content:
    content = content.replace("Social Welfare Module", "Social Welfare Department")
    print("Replaced additional occurrences of Social Welfare Module in App.tsx")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"App.tsx updated successfully.")
