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
    cursor.execute("""
        SELECT id, citizen_id, grievance_number, subject, description, status, created_at, officer_response, resolved_by, resolved_at 
        FROM grievances 
        WHERE citizen_id = 'CIT-KA-9901'
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    print(f"Total grievances for CIT-KA-9901: {len(rows)}\n")
    for r in rows:
        print(f"ID: {r['id']} | Num: {r['grievance_number']} | Status: {r['status']}")
        print(f"  Subject: {r['subject']}")
        print(f"  Desc: {r['description']}")
        print(f"  Created: {r['created_at']}")
        print(f"  Response: {r['officer_response']}")
        print("-" * 60)

conn.close()
