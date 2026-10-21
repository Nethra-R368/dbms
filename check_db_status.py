import psycopg2

try:
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='Nark@1231',
        dbname='smarthostel'
    )
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'department';")
    print('department columns:', cur.fetchall())
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'employee';")
    print('employee columns:', cur.fetchall())
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    tables = [r[0] for r in cur.fetchall()]
    print('--- TABLE ROW COUNTS ---')
    for t in sorted(tables):
        cur.execute(f'SELECT count(*) FROM "{t}";')
        print(f'{t}: {cur.fetchone()[0]} rows')
except Exception as e:
    print('Error:', e)
