"""Prepara la cartella dist/ da caricare su GreenGeeks (public_html).

Uso: python3 tools/golive.py
- copia pagine, assets e 404.html
- toglie il blocco "noindex" dell'anteprima (resta il "follow, index" di Rank Math)
- mette robots.txt e .htaccess definitivi (da golive/) e crea sitemap.xml
Il repo e l'anteprima GitHub restano con noindex: si cambia solo dist/.
"""
import os, re, shutil, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://www.thebreathworkway.com/'
DIST = os.path.join(ROOT, 'dist')
NOT_IN_SITEMAP = {'registration-form-bw-ceremony'}

shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)
slugs = sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, 'index.html')) and d not in ('dist', 'it'))
for f in ['index.html', '404.html'] + [s + '/index.html' for s in slugs] + ['it/index.html'] + ['it/' + s + '/index.html' for s in slugs]:
    t = open(os.path.join(ROOT, f), encoding='utf-8').read()
    t = t.replace('<meta name="robots" content="noindex, nofollow">', '', 1) if f != '404.html' else t
    os.makedirs(os.path.dirname(os.path.join(DIST, f)) or DIST, exist_ok=True)
    open(os.path.join(DIST, f), 'w', encoding='utf-8').write(t)
if os.path.isdir(os.path.join(ROOT, 'assets')):
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(DIST, 'assets'))
for f in ('robots.txt', '.htaccess'):
    shutil.copy(os.path.join(ROOT, 'golive', f), os.path.join(DIST, f))
today = datetime.date.today().isoformat()
urls = [LIVE] + [LIVE + s + '/' for s in slugs if s not in NOT_IN_SITEMAP and s != 'assets']
urls += [u.replace(LIVE, LIVE + 'it/', 1) for u in urls]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, today) for u in urls) + '</urlset>\n'
open(os.path.join(DIST, 'sitemap.xml'), 'w').write(xml)
left = sum(open(os.path.join(DIST, f), encoding='utf-8').read().count('thebreathworkway.com/wp-content') for f in ['index.html'] + [s + '/index.html' for s in slugs if s != 'assets'])
print('dist pronta:', len(urls), 'pagine nella sitemap; link ancora al vecchio WordPress:', left)
