import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
app = Flask(__name__)
app.secret_key = 'super secret key' 
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def root():
    record = {'url': ''}
    return render_template(
        'pages/index.html',
        record=record
    )


@app.post('/')
def add_record():
    cursor = conn.cursor()
    record = request.form.to_dict()
    errors = validate(record)
    if errors:
        return render_template(
            'pages/index.html',
            record=record,
            errors=errors
        )
    query = "INSERT INTO urls (name) VALUES (%s) RETURNING id"
    cursor.execute(query, (record['url'],))
    conn.commit()
    record['id'] = cursor.fetchone()[0]
    flash("Страница успешно добавлена")
    return redirect(url_for('show_page', id=record['id']), code=302)


@app.route('/urls/<id>')
def show_page(id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM urls WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    page = cursor.fetchone()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'pages/show_page.html',
        page=page,
        messages=messages
    )


@app.route('/urls')
def get_pages():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM urls ORDER BY id DESC"
    cursor.execute(query)
    list_pages = cursor.fetchall()
    return render_template(
        'pages/get_pages.html',
        rows=list_pages
    )


def validate(url):
    errors = {}
    parsed_url = urlparse(url['url'])
    if not parsed_url.scheme and not parsed_url.netloc:
        errors['name'] = "Некорректный URL"
    if url is None:
        errors['name'] = "Введите URL адрес"
    if len(url) > 255:
        errors['name'] = "Слишком длинный адрес"

    return errors
