import os

search_terms = [
    'Design Guidelines',
    'Safe Mode',
    'Ramesh Kumar Nayak',
    'Social Welfare Development (SWD) Microservice',
    'Public Portal Guidelines',
    'Web Accessibility Standards',
    'svg'
]

src_dir = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src'

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.tsx', '.ts', '.jsx', '.js', '.html', '.css')):
            full_path = os.path.join(root, file)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for term in search_terms:
                    if term in content:
                        print(f"Found '{term}' in {file}")
