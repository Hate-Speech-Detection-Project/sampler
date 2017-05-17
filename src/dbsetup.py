import psycopg2
import sys

try:
    conn = psycopg2.connect("dbname='hatespeech' user='postgres' host='localhost' password='admin'")
except:
    print("Cannot connect to database.")
    sys.exit(0)


cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE comments(cid INTEGER, pid INTEGER, uid INTEGER, moderated INTEGER,
                      subject VARCHAR, comment VARCHAR, created INTEGER, url VARCHAR);
    """
)




