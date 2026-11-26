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
    cursor.execute("SELECT DATABASE() as db, VERSION() as version")
    info = cursor.fetchone()
    print(f"Connected to DB: {info['db']} | Version: {info['version']}")
    
    cursor.execute("SHOW TABLES")
    tables = [list(r.values())[0] for r in cursor.fetchall()]
    print(f"\nFound {len(tables)} tables in {info['db']}:")
    
    table_counts = {}
    for t in sorted(tables):
        cursor.execute(f"SELECT COUNT(*) as cnt FROM `{t}`")
        cnt = cursor.fetchone()['cnt']
        table_counts[t] = cnt
        print(f"  - {t}: {cnt} rows")

conn.close()
