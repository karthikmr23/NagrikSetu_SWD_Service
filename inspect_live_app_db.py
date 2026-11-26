import pymysql
import json
import os

# Read-only inspection of application SWD-APP-2026-5ACF54 and its related beneficiary/DBT records
conn = pymysql.connect(
    host=os.environ.get('DB_HOST', 'swd-mysql8'),
    port=int(os.environ.get('DB_PORT', 3306)),
    user=os.environ.get('DB_USER', 'swd_user'),
    password=os.environ.get('DB_PASSWORD', 'swd_secure_password_2026'),
    database=os.environ.get('DB_NAME', 'nagriksetu_swd'),
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    # 1. Inspect Application Record
    cursor.execute("SELECT id, application_number, scheme_id, citizen_id, citizen_name, status, admin_remarks, updated_at FROM scheme_applications WHERE application_number = 'SWD-APP-2026-5ACF54'")
    app = cursor.fetchone()
    print("1. Scheme Application Record:")
    print(json.dumps(app, default=str, indent=2))

    if app:
        app_id = app['id']
        citizen_id = app['citizen_id']

        # 2. Inspect Application History
        cursor.execute("SELECT id, from_status, to_status, action_type, changed_by, remarks, created_at FROM application_history WHERE application_id = %s ORDER BY id ASC", (app_id,))
        history = cursor.fetchall()
        print("\n2. Application History Entries:")
        print(json.dumps(history, default=str, indent=2))

        # 3. Inspect Beneficiary Record
        cursor.execute("SELECT id, beneficiary_code, scheme_id, citizen_id, citizen_name, sanctioned_amount, disbursement_mode, status, sanctioned_by, sanctioned_at FROM beneficiaries WHERE application_id = %s", (app_id,))
        bens = cursor.fetchall()
        print(f"\n3. Beneficiary Records for Application {app_id} (Count: {len(bens)}):")
        print(json.dumps(bens, default=str, indent=2))

        # 4. Check Duplicate Beneficiary Protection for same citizen and scheme
        cursor.execute("SELECT count(*) as cnt FROM beneficiaries WHERE citizen_id = %s AND scheme_id = %s AND status = 'ACTIVE'", (citizen_id, app['scheme_id']))
        cnt_row = cursor.fetchone()
        print(f"\n4. Active Beneficiaries for Citizen {citizen_id} on Scheme {app['scheme_id']}: {cnt_row['cnt']}")

        # 5. Inspect DBT Transactions
        cursor.execute("SELECT id, transaction_reference, beneficiary_id, amount, status, processed_at FROM dbt_transactions WHERE beneficiary_id IN (SELECT id FROM beneficiaries WHERE application_id = %s)", (app_id,))
        txs = cursor.fetchall()
        print(f"\n5. DBT Transactions for Application {app_id}:")
        print(json.dumps(txs, default=str, indent=2))

        # 6. Inspect Audit Logs
        cursor.execute("SELECT id, actor_id, actor_role, action, entity_type, entity_id, details, created_at FROM audit_logs WHERE entity_id = %s ORDER BY id DESC LIMIT 5", (str(app_id),))
        logs = cursor.fetchall()
        print("\n6. Recent Audit Logs:")
        print(json.dumps(logs, default=str, indent=2))

conn.close()
