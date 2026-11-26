import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd',
    cursorclass=pymysql.cursors.DictCursor
)

dbt_numbers = [
    'GRV-SWD-2026-007CC6',
    'GRV-SWD-2026-F38230',
    'GRV-SWD-2026-CB849F',
    'GRV-SWD-2026-B0E6C0',
    'GRV-SWD-2026-656428',
    'GRV-SWD-2026-3A98E3'
]

bonafide_numbers = [
    'GRV-SWD-2026-CD6EDB',
    'GRV-SWD-2026-B1540B',
    'GRV-SWD-2026-75C7C9',
    'GRV-SWD-2026-B58C66',
    'GRV-SWD-2026-D8CCD8',
    'GRV-SWD-2026-227749',
    'GRV-SWD-2026-FB5C29',
    'GRV-SWD-2026-DB197F',
    'GRV-SWD-2026-686251',
    'GRV-SWD-2026-6849E3',
    'GRV-SWD-2026-53EE4E'
]

with conn.cursor() as cursor:
    print("=== DBT COMPLAINTS ===")
    cursor.execute(f"SELECT * FROM grievances WHERE grievance_number IN ({','.join(['%s']*len(dbt_numbers))}) ORDER BY id ASC", dbt_numbers)
    for r in cursor.fetchall():
        print(f"ID:{r['id']} | Num:{r['grievance_number']} | Created:{r['created_at']} | Status:{r['status']}")
        print(f"  Resp:{r['officer_response']} by {r['resolved_by']}")

    print("\n=== BONAFIDE CERTIFICATE COMPLAINTS ===")
    cursor.execute(f"SELECT * FROM grievances WHERE grievance_number IN ({','.join(['%s']*len(bonafide_numbers))}) ORDER BY id ASC", bonafide_numbers)
    for r in cursor.fetchall():
        print(f"ID:{r['id']} | Num:{r['grievance_number']} | Created:{r['created_at']} | Status:{r['status']}")
        print(f"  Resp:{r['officer_response']} by {r['resolved_by']}")

conn.close()
