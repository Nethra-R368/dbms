import psycopg2

hosts = ['127.0.0.1', 'localhost', '::1']
for h in hosts:
    try:
        conn = psycopg2.connect(
            host=h,
            user='postgres',
            password='Nark@1231',
            dbname='smarthostel',
            connect_timeout=3
        )
        conn.close()
        print(f"SUCCESS: Connected with host='{h}'")
    except Exception as e:
        err = str(e).strip().split('\n')[0]
        print(f"FAILED: Connection with host='{h}' failed: {err}")
