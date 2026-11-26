import json

with open(r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\all_35_forms_audit.json', encoding='utf-8') as f:
    schemes = json.load(f)

print(f"TOTAL SCHEMES AUDITED: {len(schemes)}")
print("-" * 120)
print(f"{'ID':2} | {'Scheme Name':38} | {'Form Title':35} | {'Fields':6} | {'Docs':4} | {'Status'}")
print("-" * 120)

for s in schemes:
    s_id = s['scheme_id']
    s_name = s['scheme_name'][:38]
    f_title = (s['form_title'] or 'NO FORM')[:35]
    f_cnt = s['fields_count']
    d_cnt = len(s['documents'])
    status = "SCHEME_SPECIFIC_PUBLISHED" if f_cnt > 0 else "NO_FORM"
    print(f"{s_id:02d} | {s_name:38} | {f_title:35} | {f_cnt:6d} | {d_cnt:4d} | {status}")
