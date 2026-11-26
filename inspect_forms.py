import pymysql

conn = pymysql.connect(host="127.0.0.1", user="swd_app", password="swd-secure-pass-2026", database="nagriksetu_swd", port=3306)
cursor = conn.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT count(*) as cnt FROM schemes WHERE status='PUBLISHED'")
print("Active schemes (PUBLISHED):", cursor.fetchone()["cnt"])

cursor.execute("""
    SELECT s.id, s.scheme_code, s.name, s.status, s.application_mode, s.official_url,
           df.id as form_id, df.version as form_ver, count(dfield.id) as field_cnt
    FROM schemes s
    LEFT JOIN dynamic_form_definitions df ON df.scheme_id = s.id AND df.is_active = 1
    LEFT JOIN dynamic_form_fields dfield ON dfield.form_id = df.id
    WHERE s.status = 'PUBLISHED'
    GROUP BY s.id, s.scheme_code, s.name, s.status, s.application_mode, s.official_url, df.id, df.version
    ORDER BY s.id
""")

rows = cursor.fetchall()
print(f"{'ID':2s} | {'Code':12s} | {'Mode':20s} | {'Fields':10s} | {'Name':35s} | {'Official URL'}")
print("-" * 115)
for r in rows:
    f_cnt = f"{r['field_cnt']} fields"
    s_code = r['scheme_code']
    s_name = r['name'][:35]
    mode = str(r['application_mode'])
    url = str(r['official_url'])[:35] if r['official_url'] else "None"
    print(f"{r['id']:2d} | {s_code:12s} | {mode:20s} | {f_cnt:10s} | {s_name:35s} | {url}")

print("\n--- SAMPLE SCHEME 1 (Post-Matric Scholarship) FIELDS ---")
cursor.execute("""
    SELECT dfield.field_name, dfield.field_label, dfield.field_type, dfield.is_required, dfield.options_json
    FROM dynamic_form_fields dfield
    JOIN dynamic_form_definitions df ON dfield.form_id = df.id
    WHERE df.scheme_id = 1
    ORDER BY dfield.display_order
""")
for f in cursor.fetchall():
    print(f"  * [{f['field_type']}] {f['field_name']}: {f['field_label']} (req={f['is_required']})")

print("\n--- SAMPLE SCHEME 5 (Gruha Lakshmi) FIELDS ---")
cursor.execute("""
    SELECT dfield.field_name, dfield.field_label, dfield.field_type, dfield.is_required, dfield.options_json
    FROM dynamic_form_fields dfield
    JOIN dynamic_form_definitions df ON dfield.form_id = df.id
    WHERE df.scheme_id = 5
    ORDER BY dfield.display_order
""")
for f in cursor.fetchall():
    print(f"  * [{f['field_type']}] {f['field_name']}: {f['field_label']} (req={f['is_required']})")

print("\n--- SAMPLE SCHEME 18 (Ganga Kalyana) FIELDS ---")
cursor.execute("""
    SELECT dfield.field_name, dfield.field_label, dfield.field_type, dfield.is_required, dfield.options_json
    FROM dynamic_form_fields dfield
    JOIN dynamic_form_definitions df ON dfield.form_id = df.id
    WHERE df.scheme_id = 18
    ORDER BY dfield.display_order
""")
for f in cursor.fetchall():
    print(f"  * [{f['field_type']}] {f['field_name']}: {f['field_label']} (req={f['is_required']})")

conn.close()
