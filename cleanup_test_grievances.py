import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd',
    cursorclass=pymysql.cursors.DictCursor
)

test_ids = [12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 34, 35]

with conn.cursor() as cursor:
    # Delete test grievances
    cursor.execute(f"DELETE FROM grievances WHERE id IN ({','.join(map(str, test_ids))}) AND citizen_id = 'CIT-KA-9901'")
    deleted_count = cursor.rowcount
    conn.commit()
    print(f"Successfully deleted {deleted_count} confirmed automated test records from CIT-KA-9901.")

    # Re-verify remaining grievances for CIT-KA-9901
    cursor.execute("SELECT id, grievance_number, subject, status, created_at FROM grievances WHERE citizen_id = 'CIT-KA-9901' ORDER BY id ASC")
    remaining = cursor.fetchall()
    print(f"Remaining grievances for CIT-KA-9901: {len(remaining)}")
    for r in remaining:
        print(f"  ID:{r['id']} | Num:{r['grievance_number']} | Status:{r['status']} | Subj:{r['subject']}")

conn.close()
