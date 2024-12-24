import os
from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.page_repository import PageRepository

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


repo = PageRepository(DATABASE_URL)


@app.route('/')
def root_page():
    record = {'url': ''}
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'pages/index.html',
        record=record,
        messages=messages
    )


@app.post('/urls')
def new_record():
    input_url = request.form.to_dict()
    error_validate = is_validate(input_url['url'])
    if error_validate:
        flash(error_validate['name'], "alert-danger")
        message = get_flashed_messages(with_categories=True)
        return render_template(
            'pages/index.html',
            input_url=input_url['url'],
            messages=message
            ), 422
    normalized_url = normalize_url(input_url['url'])
    page_id = repo.get_id(normalized_url)
    if page_id:
        flash("Страница уже существует", "alert-info")
        return redirect(url_for('show_page', id=page_id), code=302)
    else:
        input_url['id'] = repo.insert_row(normalized_url)
        flash("Страница успешно добавлена", "alert-success")
        return redirect(url_for('show_page', id=input_url['id']), code=302)


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
    url = repo.cart_page(id)
    try:
        req = requests.get(url['name'])
        req.raise_for_status()
    except Exception:
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for('show_page', id=id), code=302)
    status_code = req.status_code
    seo = find_seo(url)
    repo.insert_check(id, status_code, seo['title'], seo['h1'], seo['content'])
    flash("Страница успешно проверена", "alert-success")
    return redirect(url_for('show_page', id=id), code=302)


@app.route('/urls')
def get_pages():
    list_pages = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'pages/get_pages.html',
        messages=messages,
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


def find_seo(url):
    text = requests.get(url['name']).text
    soup = BeautifulSoup(text, 'lxml')
    h1 = None
    title = None
    meta = None
    try:
        h1 = soup.h1.text
    except Exception:
        pass
    try:
        title = soup.title.text
    except Exception:
        pass
    meta = soup.select('meta[name="description"]')
    for attr in meta:
        content = attr.get('content')
    return {
        'title': title,
        'h1': h1,
        'content': content
    }
