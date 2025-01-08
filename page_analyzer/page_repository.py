from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor


class PageRepository():
    def __init__(self, db_url):
        self.db_url = db_url
        self.pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=db_url)

    def get_connection(self):
        return self.pool.getconn()

    def get_content(self):
        conn = self.get_connection()
        curr = conn.cursor(cursor_factory=RealDictCursor)
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
        self.pool.putconn(conn)
        return result

    def add_url(self, url):
        conn = self.get_connection()
        curr = conn.cursor()
        curr.execute(
            """
            INSERT INTO urls (name) VALUES (%s) RETURNING id;
            """,
            (url,)
        )
        result = curr.fetchone()[0]
        conn.commit()
        self.pool.putconn(conn)
        return result

    def get_site(self, id):
        conn = self.get_connection()
        curr = conn.cursor(cursor_factory=RealDictCursor)
        curr.execute(
            """
            SELECT * FROM urls WHERE id = %s
            ORDER BY created_at DESC, name ASC;""",
            (id,)
        )
        result = curr.fetchone()
        self.pool.putconn(conn)
        return result

    def get_id(self, data):
        conn = self.get_connection()
        curr = conn.cursor()
        curr.execute(
            "SELECT * FROM urls WHERE name = %s;",
            (data,)
        )
        if curr.rowcount > 0:
            result = curr.fetchone()[0]
            self.pool.putconn(conn)
            return result
        return None

    def add_check(self, url_id, status_code, title, h1, content):
        conn = self.get_connection()
        curr = conn.cursor()
        curr.execute(
                """
            INSERT INTO url_checks (
                url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s);
                """,
                (url_id, status_code, h1, title, content)
            )
        conn.commit()
        self.pool.putconn(conn)

    def check_url(self, id):
        conn = self.get_connection()
        curr = conn.cursor(cursor_factory=RealDictCursor)
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
        self.pool.putconn(conn)
        return result
