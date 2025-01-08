import os

import requests
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
from page_analyzer.utilities import Utilities

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


repo = PageRepository(DATABASE_URL)
utility = Utilities()


@app.route('/')
def index_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'pages/index.html',
        messages=messages
    )


@app.post('/urls')
def new_record():
    url = request.form.to_dict()
    error = utility.is_validate(url['url'])
    if error:
        flash(error['name'], "alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'pages/index.html',
            url=url['url'],
            messages=messages
            ), 422
    normalize_url = utility.normalized_url(url['url'])
    page_id = repo.get_id(normalize_url)
    if page_id:
        flash("Страница уже существует", "alert-info")
        return redirect(url_for('site_page', id=page_id), code=302)
    else:
        url['id'] = repo.add_url(normalize_url)
        flash("Страница успешно добавлена", "alert-success")
        return redirect(url_for('site_page', id=url['id']), code=302)


@app.route('/urls/<int:id>')
def site_page(id):
    page = repo.get_site(id)
    messages = get_flashed_messages(with_categories=True)
    checks = repo.check_url(id)
    return render_template(
        'pages/site_page.html',
        page=page,
        rows=checks,
        messages=messages
    )


@app.post('/urls/<id>/checks')
def check_page(id):
    url = repo.get_site(id)
    try:
        req = requests.get(url['name'])
        req.raise_for_status()
    except Exception:
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for('site_page', id=id), code=302)
    status_code = req.status_code
    seo = utility.find_seo(url)
    repo.add_check(id, status_code, seo['title'], seo['h1'], seo['content'])
    flash("Страница успешно проверена", "alert-success")
    return redirect(url_for('site_page', id=id), code=302)


@app.route('/urls')
def all_pages():
    list_pages = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'pages/all_pages.html',
        messages=messages,
        rows=list_pages
    )
