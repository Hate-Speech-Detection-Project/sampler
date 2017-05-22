import psycopg2
import sys


class DBInterface:
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='hatespeech' user='postgres' host='localhost' password='admin'")
        except:
            print("Cannot connect to database.")
            sys.exit(0)

    def insert_article(self, article):
        cur = self.conn.cursor()
        query = """ INSERT INTO articles (id,heading,body,ressort) VALUES (%s, %s, %s,%s) """
        data = (article.get_id(), article.get_heading(), article.get_body(), article.get_ressort())
        cur.execute(query, data)

    def article_table_already_exists(self):
        cur = self.conn.cursor()

        cur.execute(
            """
                 SELECT EXISTS(SELECT 1 FROM information_schema.tables
                    WHERE table_catalog = 'hatespeech' AND table_schema = 'public'
                    AND table_name = 'articles');
            """
        )
        return bool(cur.fetchone()[0])

    def create_articles_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
                  CREATE TABLE articles (
                        id INTEGER PRIMARY KEY,
                        heading TEXT,
                        body TEXT NOT NULL,
                        ressort TEXT NOT NULL
                    )
            """
        )
        self.conn.commit()

    def commit_queries(self):
        self.conn.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
