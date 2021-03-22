DB_HOST = "localhost"
DB_NAME = "HYPERION"
DB_USER = "postgres"
DB_PASS = "postgres"


import psycopg2

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS)


cur = conn.cursor()

cur.execute("SELECT * FROM logging_event WHERE event_identifier = 12464")

logs = cur.fetchall()


cur.close()
conn.close()




for log in logs:

    a = memoryview(log[6]).tobytes()
    print(a)