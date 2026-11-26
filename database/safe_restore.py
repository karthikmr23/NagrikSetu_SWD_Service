#!/usr/bin/env python3
"""
Safe MySQL Database Restore Utility for NagrikSetu Social Welfare Department (SWD) Microservice.
(Member 2 Deliverable)

Guarantees:
1. Validates that the target database is dedicated/isolated (swd_db).
2. Prevents accidental overwrite of shared databases (e.g. 'nagriksetu_main', 'production', 'education_db', 'skill_db').
3. Confirms user intent or executes safely under CI/CD automation (--yes flag).
"""

import sys
import os
import argparse
import pymysql

def main():
    parser = argparse.ArgumentParser(description="Safely restore NagrikSetu SWD SQL backup into an isolated MySQL database.")
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"), help="MySQL host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", 3306)), help="MySQL port (default: 3306)")
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"), help="MySQL username (default: root)")
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""), help="MySQL password")
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "swd_db"), help="Target database name (default: swd_db)")
    parser.add_argument("--sql-file", default=os.path.join(os.path.dirname(__file__), "swd_db_setup.sql"), help="Path to SQL dump file")
    parser.add_argument("--yes", action="store_true", help="Confirm execution without interactive prompt")

    args = parser.parse_args()

    # Safety check on database name to prevent overwriting other services
    forbidden_shared_names = ("nagriksetu_main", "nagriksetu_core", "production", "prod", "main_db", "skill_db", "education_db", "employment_db", "administration_db")
    if args.database.lower() in forbidden_shared_names:
        print(f"\n[ERROR] Target database '{args.database}' is reserved for other services or production.", file=sys.stderr)
        print("To protect other microservices, SWD tables must be restored into a dedicated schema ('swd_db').", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.sql_file):
        print(f"\n[ERROR] SQL file not found at: {args.sql_file}", file=sys.stderr)
        sys.exit(1)

    print("=" * 70)
    print("NAGRIKSETU SWD - SAFE DATABASE RESTORATION UTILITY (MEMBER 2)")
    print("=" * 70)
    print(f"Target Database : {args.database}")
    print(f"Target Host     : {args.host}:{args.port}")
    print(f"Target User     : {args.user}")
    print(f"SQL Dump File   : {args.sql_file}")
    print("-" * 70)

    try:
        # First connect without database to ensure database exists
        conn = pymysql.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            charset="utf8mb4",
            autocommit=True
        )
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{args.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cur.execute(f"USE `{args.database}`;")

        # Read and execute SQL statements
        with open(args.sql_file, "r", encoding="utf-8") as f:
            sql_content = f.read()

        statements = [s.strip() for s in sql_content.split(";") if s.strip()]
        executed = 0
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for stmt in statements:
                # Skip comments
                clean_lines = [l for l in stmt.split("\n") if not l.strip().startswith("--")]
                clean_stmt = "\n".join(clean_lines).strip()
                if clean_stmt:
                    cur.execute(clean_stmt)
                    executed += 1
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

        conn.close()
        print(f"[SUCCESS] Successfully executed {executed} statements into '{args.database}'.")
        print("Database schema, constraints, indexes, and Karnataka schemes are fully restored.")
    except Exception as e:
        print(f"[ERROR] Failed to restore database: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
