import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='swd_app', password='swd-secure-pass-2026', database='nagriksetu_swd')
with conn.cursor() as cur:
    cur.execute("DELETE FROM grievances WHERE subject = 'Timezone Check Ticket'")
    conn.commit()
    print('Deleted check ticket:', cur.rowcount)
conn.close()
