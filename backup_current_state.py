import pymysql
import json

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM grievances ORDER BY id ASC")
    all_g = cursor.fetchall()
    for r in all_g:
        for k, v in r.items():
            if v is not None and hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
    with open('grievances_full_pre_cleanup_backup.json', 'w') as f:
        json.dump(all_g, f, indent=2)
    print(f"Total grievances currently in MySQL: {len(all_g)}")

    cursor.execute("SELECT * FROM notifications ORDER BY id ASC")
    all_n = cursor.fetchall()
    for r in all_n:
        for k, v in r.items():
            if v is not None and hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
    with open('notifications_full_pre_cleanup_backup.json', 'w') as f:
        json.dump(all_n, f, indent=2)
    print(f"Total notifications currently in MySQL: {len(all_n)}")

conn.close()
