from contextlib import contextmanager

from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool


class PageRepository():
    def __init__(self, db_url):
        self.db_url = db_url
        self.pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=db_url)

    @contextmanager
    def get_connection(self):
        connection = self.pool.getconn()

        try:
            yield connection
        finally:
            connection.commit()
            self.pool.putconn(connection)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute("""
                    DROP VIEW IF EXISTS filter;

                    CREATE VIEW filter AS
                    SELECT url_id, MAX(id) AS max_id FROM url_checks
                    GROUP BY url_id;

                    SELECT urls.id,
                        name,
                        max_id,
                        status_code,
                        url_checks.created_at
                    FROM urls
                    LEFT JOIN filter
                    ON urls.id = filter.url_id
                    LEFT JOIN url_checks
                    ON url_checks.id = filter.max_id
                    ORDER BY url_checks.created_at DESC, name;""")
                result = curr.fetchall()
                return result

    def add_url(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    """
                    INSERT INTO urls (name) VALUES (%s) RETURNING id;
                    """,
                    (url,)
                )
                result = curr.fetchone()[0]
                return result

    def get_site(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(
                    """
                    SELECT * FROM urls WHERE id = %s
                    ORDER BY created_at DESC, name ASC;""",
                    (id,)
                )
                result = curr.fetchone()
                return result

    def get_id(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM urls WHERE name = %s;",
                    (data,)
                )
                if curr.rowcount > 0:
                    result = curr.fetchone()[0]
                    return result
                return None

    def add_check(self, url_id, status_code, title, h1, content):
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

    def check_url(self, id):
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
                result = curr.fetchall()
                return result
