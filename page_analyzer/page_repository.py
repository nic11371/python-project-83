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
                curr.execute("""SELECT urls.id,
                            urls.name,
                            url_checks.status_code,
                            url_checks.created_at
                            FROM urls
                            INNER JOIN url_checks
                            ON urls.id = url_checks.url_id
                            ORDER BY id DESC""")
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
                    """SELECT * FROM urls WHERE id = %s
                    ORDER BY created_at DESC, name ASC;""",
                    (id,)
                )
                return curr.fetchone()

    def get_id(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM urls WHERE name = %s;",
                    (data,)
                )
                if curr.rowcount > 0:
                    return curr.fetchone()[0]
        return None

    def insert_check(self, url_id, status_code, title, h1, content):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    """
                INSERT INTO url_checks (
                    url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s);
                    """,
                    (url_id, status_code, h1, title, content)
                )

    def check_row(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(
                    """SELECT url_checks.id,
                        url_checks.status_code,
                        url_checks.h1,
                        url_checks.title,
                        url_checks.description,
                        url_checks.created_at
                    FROM url_checks
                    INNER JOIN urls
                    ON urls.id = url_checks.url_id
                    WHERE urls.id = %s
                    ORDER BY url_checks.id DESC;""",
                    (id,)
                )
                return curr.fetchall()
