import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='Nark@1231',
        dbname='smarthostel'
    )
    conn.close()
    print("SUCCESS: Connected to PostgreSQL database smarthostel!")
except Exception as e:
    print("FAILED:", e)
