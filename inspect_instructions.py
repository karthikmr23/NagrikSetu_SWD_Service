import pymysql

conn = pymysql.connect(host="127.0.0.1", user="swd_app", password="swd-secure-pass-2026", database="nagriksetu_swd", port=3306)
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("""
    SELECT s.id, s.scheme_code, s.name, s.application_mode, s.official_url, s.application_instructions
    FROM schemes s
    ORDER BY s.id
""")
for r in cursor.fetchall():
    print(f"ID {r['id']:2d}: {r['name']} | Mode: {r['application_mode']} | URL: {r['official_url']}")
    if r['application_instructions']:
        print(f"   Instructions: {r['application_instructions'][:100]}...")
conn.close()
