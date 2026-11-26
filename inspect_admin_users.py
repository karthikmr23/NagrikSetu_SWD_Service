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
        SELECT id, citizen_id, email, full_name, role, phone, is_active, created_at 
        FROM users 
        WHERE role != 'CITIZEN' OR email LIKE '%admin%' OR email LIKE '%officer%' OR email LIKE '%welfare%' OR full_name LIKE '%Admin%'
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    print(f"Total administrative users found: {len(rows)}\n")
    for r in rows:
        print(f"ID: {r['id']} | CitizenID: {r['citizen_id']} | Email: {r['email']} | Role: {r['role']} | Name: {r['full_name']} | Active: {r['is_active']}")

conn.close()
