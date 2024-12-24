DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER,
    status_code VARCHAR(255),
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at DATE DEFAULT CURRENT_DATE
);
