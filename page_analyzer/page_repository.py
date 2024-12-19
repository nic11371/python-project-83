from psycopg2.extras import RealDictCursor
import psycopg2


class PageRepository():
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute("SELECT * FROM urls ORDER BY id DESC")
                return curr.fetchall()

    def insert_row(self, normalized_record):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    """
                    INSERT INTO urls (name) VALUES (%s) RETURNING id;
                    """,
                    (normalized_record,)
                )
                return curr.fetchone()[0]

    def cart_page(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(
                    "SELECT * FROM urls WHERE id = %s",
                    (id,)
                )
                return curr.fetchone()

    def get_id(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM urls WHERE name = %s",
                    (data,)
                )
                if curr.rowcount > 0:
                    return curr.fetchone()[0]
        return None
