import psycopg2
from psycopg2.extras import RealDictCursor


class PageRepository():
    def __init__(self, db_url):
        self.conn = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)
