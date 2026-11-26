import pymysql
import os

DB_HOST = '127.0.0.1'
DB_PORT = 3307
DB_USER = 'swd_app'
DB_PASS = 'swd-secure-pass-2026'
DB_NAME = 'nagriksetu_swd'

dump_file = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\database\swd_migration_backup_20261124.sql'

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    charset='utf8mb4'
)
cursor = conn.cursor()

print("Reading dump file...")
with open(dump_file, 'r', encoding='utf-8') as f:
    sql_text = f.read()

statements = []
cur_stmt = []
in_string = False
escape = False

for line in sql_text.splitlines(keepends=True):
    if line.startswith('--') or not line.strip():
        continue
    cur_stmt.append(line)
    if line.strip().endswith(';'):
        statements.append(''.join(cur_stmt))
        cur_stmt = []

if cur_stmt:
    statements.append(''.join(cur_stmt))

print(f"Executing {len(statements)} SQL statements on 127.0.0.1:3307...")
for stmt in statements:
    s = stmt.strip()
    if s:
        try:
            cursor.execute(s)
        except Exception as e:
            print(f"Error executing: {s[:100]}... -> {e}")
            raise e

conn.commit()
print("Restoration executed successfully!")

# Reconcile counts
cursor.execute("SHOW TABLES;")
dest_tables = sorted([r[0] for r in cursor.fetchall()])
print(f"Tables found in destination: {len(dest_tables)}")

dest_counts = {}
for t in dest_tables:
    cursor.execute(f"SELECT COUNT(*) FROM `{t}`;")
    dest_counts[t] = cursor.fetchone()[0]

cursor.close()
conn.close()

# Now compare with source
conn_src = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd',
    charset='utf8mb4'
)
cur_src = conn_src.cursor()
src_counts = {}
for t in dest_tables:
    cur_src.execute(f"SELECT COUNT(*) FROM `{t}`;")
    src_counts[t] = cur_src.fetchone()[0]
cur_src.close()
conn_src.close()

print("\n=== TABLE COUNT RECONCILIATION ===")
all_match = True
for t in dest_tables:
    sc = src_counts[t]
    dc = dest_counts[t]
    match = (sc == dc)
    if not match:
        all_match = False
    print(f"{t}: Source(3306)={sc} | Dest(3307)={dc} | {'MATCH [OK]' if match else 'MISMATCH [FAIL]'}")

print(f"\nOverall Reconciliation Result: {'ALL TABLES MATCH 100%' if all_match else 'DISCREPANCY FOUND'}")
