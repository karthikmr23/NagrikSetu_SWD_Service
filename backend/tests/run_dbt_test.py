import urllib.request, json

def run_test():
    # Admin Login
    login_req = urllib.request.Request(
        'http://127.0.0.1:8004/api/swd/auth/login',
        data=json.dumps({'email': 'admin@nagriksetu.local', 'password': 'AdminPass@2026'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(login_req) as r:
        admin_token = json.loads(r.read())['access_token']

    admin_headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}

    # Citizen Login
    cit_login = urllib.request.Request(
        'http://127.0.0.1:8004/api/swd/auth/login',
        data=json.dumps({'email': 'citizen@example.com', 'password': 'CitizenPass@2026'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(cit_login) as r:
        cit_token = json.loads(r.read())['access_token']

    cit_headers = {'Authorization': f'Bearer {cit_token}', 'Content-Type': 'application/json'}

    # Application 1 (use matched citizen_id: CIT-KA-9901)
    app1 = {
        'citizen_id': 'CIT-KA-9901', 'citizen_name': 'Ramesh Kumar Nayak', 'citizen_phone': '9845099999',
        'annual_income': 24000.0, 'caste_category': 'SC', 'residence_district': 'Bengaluru Urban',
        'bank_account_number': '112233445566', 'bank_ifsc': 'SBIN0001234'
    }
    r1 = urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8004/api/swd/schemes/2/applications', data=json.dumps(app1).encode('utf-8'), headers=cit_headers))
    app1_res = json.loads(r1.read())
    app1_id = app1_res['id']
    print('App 1 created, ID:', app1_id)

    dec1_url = f'http://127.0.0.1:8004/api/swd/admin/applications/{app1_id}/decision'
    urllib.request.urlopen(urllib.request.Request(dec1_url, data=json.dumps({'decision': 'APPROVED', 'sanctioned_amount': 12000.0, 'remarks': 'Senior pension approved'}).encode('utf-8'), headers=admin_headers))
    print('App 1 approved.')

    # Application 2 (Scheme 3)
    app2 = {
        'citizen_id': 'CIT-KA-9901', 'citizen_name': 'Ramesh Kumar Nayak', 'citizen_phone': '9845099999',
        'annual_income': 18000.0, 'caste_category': 'SC', 'residence_district': 'Bengaluru Urban',
        'bank_account_number': '998877665544', 'bank_ifsc': 'KARB0000123'
    }
    r2 = urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8004/api/swd/schemes/3/applications', data=json.dumps(app2).encode('utf-8'), headers=cit_headers))
    app2_res = json.loads(r2.read())
    app2_id = app2_res['id']
    print('App 2 created, ID:', app2_id)

    dec2_url = f'http://127.0.0.1:8004/api/swd/admin/applications/{app2_id}/decision'
    urllib.request.urlopen(urllib.request.Request(dec2_url, data=json.dumps({'decision': 'APPROVED', 'sanctioned_amount': 24000.0, 'remarks': 'Disability grant approved'}).encode('utf-8'), headers=admin_headers))
    print('App 2 approved.')

    # Beneficiaries list
    bens = json.loads(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8004/api/swd/beneficiaries', headers=admin_headers)).read())
    print(f'Total Beneficiaries: {len(bens)}')

    # Batch DBT with partial failure test
    target_ids = [bens[0]['id'], bens[1]['id']]
    fail_target = [bens[0]['id']] # simulate CBS bank rejection for 1

    batch_data = {
        'beneficiary_ids': target_ids,
        'remarks': 'Simulated Batch DBT Execution',
        'fail_beneficiary_ids': fail_target
    }
    batch_res = json.loads(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8004/api/swd/dbt/batch-process', data=json.dumps(batch_data).encode('utf-8'), headers=admin_headers)).read())

    print('\n=== BATCH DBT EXECUTION RESULT ===')
    print('Batch Reference:', batch_res['batch_reference'])
    print('Total Processed:', batch_res['total_processed'])
    print('Successful Count:', batch_res['successful_count'])
    print('Failed Count:', batch_res['failed_count'])
    print('Total Amount Disbursed: Rs.', batch_res['total_amount_disbursed'])
    print('Notice:', batch_res['notice'])
    for it in batch_res['results']:
        print(f' - {it["beneficiary_name"]}: {it["status"]} | Ref: {it["transaction_reference"]} | Remarks: {it["remarks"]}')

if __name__ == '__main__':
    run_test()
