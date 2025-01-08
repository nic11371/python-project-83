from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup


class Utilities():
    def normalized_url(self, url):
        parsed_url = urlparse(url)
        normalized_parsed_url = parsed_url._replace(
            path="", params="", query="", fragment="").geturl()
        return normalized_parsed_url.lower()

    def is_validate(self, url):
        errors = {}
        is_valid = validators.url(url)
        if not is_valid:
            errors['name'] = "Некорректный URL"
        if len(url) > 255:
            errors['name'] = "Слишком длинный адрес"
        return errors

    def find_seo(self, url):
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
