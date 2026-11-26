import pymysql
import bcrypt
from datetime import datetime

conn = pymysql.connect(host="127.0.0.1", user="swd_app", password="swd-secure-pass-2026", database="nagriksetu_swd", port=3306)
cursor = conn.cursor(pymysql.cursors.DictCursor)

# Passwords
platform_pass = "Platform@123"
welfare_pass = "Welfare@123"

# Hash using bcrypt (12 rounds)
platform_hash = bcrypt.hashpw(platform_pass.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
welfare_hash = bcrypt.hashpw(welfare_pass.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

now = datetime.utcnow()

# Insert or Update Account 1: Platform Admin
cursor.execute("""
    SELECT id, citizen_id, email, role FROM users 
    WHERE email = 'platformadmin@example.com' OR citizen_id = 'platformadmin'
""")
existing_platform = cursor.fetchone()

if existing_platform:
    cursor.execute("""
        UPDATE users SET 
            citizen_id = 'platformadmin',
            email = 'platformadmin@example.com',
            password_hash = %s,
            full_name = 'Platform Administrator',
            role = 'PLATFORM_ADMIN',
            is_active = 1,
            updated_at = %s
        WHERE id = %s
    """, (platform_hash, now, existing_platform["id"]))
    print(f"Updated existing Platform Admin user ID {existing_platform['id']}")
else:
    cursor.execute("""
        INSERT INTO users (
            citizen_id, email, password_hash, full_name, role, is_active, created_at, updated_at
        ) VALUES (
            'platformadmin', 'platformadmin@example.com', %s, 'Platform Administrator', 'PLATFORM_ADMIN', 1, %s, %s
        )
    """, (platform_hash, now, now))
    print(f"Inserted new Platform Admin user ID {cursor.lastrowid}")

# Insert or Update Account 2: Government Welfare Admin
cursor.execute("""
    SELECT id, citizen_id, email, role FROM users 
    WHERE email = 'welfareadmin@example.com' OR citizen_id = 'welfareadmin'
""")
existing_welfare = cursor.fetchone()

if existing_welfare:
    cursor.execute("""
        UPDATE users SET 
            citizen_id = 'welfareadmin',
            email = 'welfareadmin@example.com',
            password_hash = %s,
            full_name = 'Government Welfare Administrator',
            role = 'GOVERNMENT_WELFARE_ADMIN',
            is_active = 1,
            updated_at = %s
        WHERE id = %s
    """, (welfare_hash, now, existing_welfare["id"]))
    print(f"Updated existing Government Welfare Admin user ID {existing_welfare['id']}")
else:
    cursor.execute("""
        INSERT INTO users (
            citizen_id, email, password_hash, full_name, role, is_active, created_at, updated_at
        ) VALUES (
            'welfareadmin', 'welfareadmin@example.com', %s, 'Government Welfare Administrator', 'GOVERNMENT_WELFARE_ADMIN', 1, %s, %s
        )
    """, (welfare_hash, now, now))
    print(f"Inserted new Government Welfare Admin user ID {cursor.lastrowid}")

conn.commit()

# Query and print both records
cursor.execute("""
    SELECT id, citizen_id, email, role, full_name, is_active, password_hash 
    FROM users 
    WHERE citizen_id IN ('platformadmin', 'welfareadmin')
""")
for u in cursor.fetchall():
    print(f"User: {u['citizen_id']} | Email: {u['email']} | Role: {u['role']} | Active: {u['is_active']} | Hash: {u['password_hash'][:25]}...")

conn.close()
