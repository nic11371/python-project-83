import os
import validators
import requests
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
from page_analyzer.page_repository import PageRepository


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.secret_key = 'super secret key'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


repo = PageRepository(DATABASE_URL)


@app.route('/')
def root():
    record = {'url': ''}
    return render_template(
        'pages/index.html',
        record=record
    )


@app.post('/')
def add_record():
    record = request.form.to_dict()
    validate = is_validate(record['url'])
    if validate:
        return render_template(
            'pages/index.html',
            record=record,
            errors=validate
        )
    normalized_record = normalize_url(record['url'])
    page_id = repo.get_id(normalized_record)
    if page_id:
        flash("Страница уже существует", "alert-info")
        return redirect(url_for('show_page', id=page_id), code=302)
    else:
        record['id'] = repo.insert_row(normalized_record)
        flash("Страница успешно добавлена", "alert-success")
        return redirect(url_for('show_page', id=record['id']), code=302)


@app.route('/urls/<int:id>')
def show_page(id):
    page = repo.cart_page(id)
    messages = get_flashed_messages(with_categories=True)
    checks = repo.check_row(id)
    return render_template(
        'pages/show_page.html',
        page=page,
        checks=checks,
        messages=messages
    )


@app.post('/urls/<id>/checks')
def check_url(id):
    try:
        req = request_to_site(id)
    except Exception:
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for('show_page', id=id), code=302)
    if req.status_code != 200:
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for('show_page', id=id), code=302)
    status_code = req.status_code
    repo.insert_check(id, status_code)
    flash("Страница успешно проверена", "alert-success")
    return redirect(url_for('show_page', id=id), code=302)


@app.route('/urls')
def get_pages():
    list_pages = repo.get_content()
    return render_template(
        'pages/get_pages.html',
        rows=list_pages
    )


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_parsed_url = parsed_url._replace(
        path="", params="", query="", fragment="").geturl()
    return normalized_parsed_url.lower()


def is_validate(url):
    errors = {}
    is_valid = validators.url(url)
    if not is_valid:
        errors['name'] = "Некорректный URL"
    if len(url) > 255:
        errors['name'] = "Слишком длинный адрес"
    return errors


def request_to_site(id):
    url = repo.cart_page(id)
    return requests.get(url['name'])
