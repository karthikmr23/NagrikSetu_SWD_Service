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

test_ids = [12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 34, 35]

with conn.cursor() as cursor:
    cursor.execute(f"SELECT * FROM grievances WHERE id IN ({','.join(map(str, test_ids))})")
    rows = cursor.fetchall()
    
    # Save backup as JSON
    # Convert datetimes to strings
    for r in rows:
        for k, v in r.items():
            if v is not None and hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
                
    with open('grievances_backup.json', 'w') as f:
        json.dump(rows, f, indent=2)
    print(f"Backed up {len(rows)} records to grievances_backup.json")

conn.close()
