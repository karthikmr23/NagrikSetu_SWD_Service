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
    cursor.execute("SELECT id, citizen_id, citizen_name, grievance_number, category, subject, description, status, created_at, officer_response, resolved_by FROM grievances ORDER BY id ASC")
    rows = cursor.fetchall()
    print(f"Total grievances: {len(rows)}")
    for r in rows:
        print(f"ID:{r['id']} | CitID:{r['citizen_id']} | Num:{r['grievance_number']} | Status:{r['status']} | Created:{r['created_at']} | Subj:{r['subject']}")
conn.close()
