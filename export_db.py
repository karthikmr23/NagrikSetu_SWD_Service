import pymysql
import os
import datetime

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'swd_app'
DB_PASS = 'swd-secure-pass-2026'
DB_NAME = 'nagriksetu_swd'

out_dir = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\database'
os.makedirs(out_dir, exist_ok=True)
dump_file = os.path.join(out_dir, 'swd_migration_backup_20261124.sql')

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    charset='utf8mb4'
)
cursor = conn.cursor()

cursor.execute('SHOW TABLES;')
tables = [row[0] for row in cursor.fetchall()]

with open(dump_file, 'w', encoding='utf-8') as f:
    f.write('-- NagrikSetu SWD Full Backup\n')
    f.write(f'-- Export Date: {datetime.datetime.now().isoformat()}\n')
    f.write('SET FOREIGN_KEY_CHECKS=0;\n')
    f.write('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";\n\n')

    for table in tables:
        f.write(f'DROP TABLE IF EXISTS `{table}`;\n')
        cursor.execute(f'SHOW CREATE TABLE `{table}`;')
        create_sql = cursor.fetchone()[1]
        f.write(f'{create_sql};\n\n')

        cursor.execute(f'SELECT * FROM `{table}`;')
        rows = cursor.fetchall()
        if rows:
            cursor.execute(f'SHOW COLUMNS FROM `{table}`;')
            cols = [f'`{c[0]}`' for c in cursor.fetchall()]
            cols_str = ', '.join(cols)
            f.write(f'INSERT INTO `{table}` ({cols_str}) VALUES\n')
            vals = []
            for r in rows:
                row_vals = []
                for v in r:
                    if v is None:
                        row_vals.append('NULL')
                    elif isinstance(v, (int, float)):
                        row_vals.append(str(v))
                    elif isinstance(v, (datetime.datetime, datetime.date)):
                        row_vals.append(f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'")
                    elif isinstance(v, bytes):
                        row_vals.append(f"X'{v.hex()}'")
                    else:
                        val_escaped = str(v).replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
                        row_vals.append(f"'{val_escaped}'")
                vals.append(f"({', '.join(row_vals)})")
            f.write(',\n'.join(vals) + ';\n\n')

    f.write('SET FOREIGN_KEY_CHECKS=1;\n')

cursor.close()
conn.close()
size = os.path.getsize(dump_file)
print(f'Backup completed successfully: {dump_file} ({size} bytes, {len(tables)} tables)')
