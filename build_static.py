#!/usr/bin/env python3
"""Заморозка Django-сайта АварКомиссар в статику для GitHub Pages."""
import os, re, shutil, django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

DOMAIN = 'komissar125.ru'           # прод-домен для canonical/sitemap
DIST = Path('dist')

# (URL-путь Django, файл назначения, глубина вложенности)
PAGES = [
    ('/',                                 'index.html',                                  0),
    ('/uslugi/avariyny-komissar/',        'uslugi/avariyny-komissar/index.html',         2),
    ('/uslugi/avtostrakhovanie/',         'uslugi/avtostrakhovanie/index.html',          2),
    ('/uslugi/nezavisimaya-ekspertiza/',  'uslugi/nezavisimaya-ekspertiza/index.html',   2),
    ('/uslugi/soprovozhdeniye/',          'uslugi/soprovozhdeniye/index.html',           2),
    ('/kontakty/',                        'kontakty/index.html',                         1),
    ('/o-kompanii/',                      'o-kompanii/index.html',                       1),
    ('/politika-konfidencialnosti/',      'politika-konfidencialnosti/index.html',       1),
    ('/polzovatelskoe-soglashenie/',      'polzovatelskoe-soglashenie/index.html',       1),
    ('/intellektualnaya-sobstvennost/',   'intellektualnaya-sobstvennost/index.html',    1),
    ('/soglasie-na-obrabotku-pd/',        'soglasie-na-obrabotku-pd/index.html',         1),
]

CSRF_RE = re.compile(r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*>\s*')
# href/src="/что-то" но не "//" (протокол-относительные) и не пустые
ATTR_RE = re.compile(r'(href|src)=(["\'])/(?!/)([^"\']*)\2')

def relativize(html: str, depth: int) -> str:
    prefix = '../' * depth if depth else './'
    def repl(m):
        attr, q, path = m.group(1), m.group(2), m.group(3)
        return f'{attr}={q}{prefix}{path}{q}'
    html = ATTR_RE.sub(repl, html)
    html = CSRF_RE.sub('', html)          # csrf не нужен в статике
    return html

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    client = Client()

    for url, out, depth in PAGES:
        resp = client.get(url, secure=True, HTTP_HOST=DOMAIN)
        assert resp.status_code == 200, f'{url} -> HTTP {resp.status_code}'
        html = resp.content.decode('utf-8')
        html = relativize(html, depth)
        dest = DIST / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding='utf-8')
        print(f'  {url:42s} -> {out}')

    # копируем только публичную статику (без cms.css админки)
    shutil.copytree('static/css', DIST / 'static/css')
    shutil.copytree('static/js',  DIST / 'static/js')
    shutil.copytree('static/img', DIST / 'static/img')
    # подчищаем админский css если попал
    cms = DIST / 'static/cms'
    if cms.exists():
        shutil.rmtree(cms)
    print('  static/ -> dist/static/')

if __name__ == '__main__':
    main()
