import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    cursor.execute("SELECT id, citizen_id, grievance_number, subject, description, status, created_at, updated_at, resolved_at, resolved_by FROM grievances ORDER BY id ASC")
    rows = cursor.fetchall()
    print(f"Total grievances: {len(rows)}\n")
    for r in rows:
        print(f"ID:{r['id']} | CitID:{r['citizen_id']} | Num:{r['grievance_number']} | Status:{r['status']}")
        print(f"   Created:{r['created_at']} | Updated:{r['updated_at']} | Resolved:{r['resolved_at']}")
        print(f"   Subject: {r['subject']}")
        print(f"   Desc: {r['description']}")
        print("-" * 60)

conn.close()
