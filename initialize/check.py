import os
import psycopg2
import time

ok = False

while not ok:
    time.sleep(5)
    print("Starting *****************************************************************************")
    with psycopg2.connect("dbname='shipment_db' user='postgresuser' host='postgres' port='5432' password='postgrespw'") as conn:
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('orders',))
        ok = bool(cur.rowcount)
        print(ok)
        if ok:
            os.system('curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://connect:8083/connectors/ -d @/initialize/source.json')
            time.sleep(15)
            os.system('curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://connect:8083/connectors/ -d @/initialize/sink.json')
            time.sleep(15)
            os.system('uvicorn app.main:app --host 0.0.0.0')


