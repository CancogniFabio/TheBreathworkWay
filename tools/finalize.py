"""Pulisce un file estratto e lo salva nel mockup.

Uso: python3 tools/finalize.py <file_estratto.txt> <slug>
slug "home" -> index.html; altrimenti <slug>/index.html.
Poi riscrive in TUTTE le pagine del mockup i link alle pagine già copiate,
così puntano alla copia invece che al sito live.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://www.thebreathworkway.com/'

src, slug = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
s = re.sub(r'<link\b[^>]*rel="(alternate|EditURI|https://api\.w\.org/|shortlink|canonical|pingback)"[^>]*>', '', s)
s = re.sub(r'<meta\b[^>]*name="generator"[^>]*>', '', s)
dest = os.path.join(ROOT, 'index.html') if slug == 'home' else os.path.join(ROOT, slug, 'index.html')
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, 'w', encoding='utf-8').write(s)

# pagine già copiate = cartelle con index.html
copied = [d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, 'index.html'))]
pages = [os.path.join(ROOT, 'index.html')] + [os.path.join(ROOT, d, 'index.html') for d in copied]
for p in pages:
    depth = 0 if os.path.dirname(p) == ROOT else 1
    up = '../' * depth
    t = open(p, encoding='utf-8').read()
    t = t.replace('href="./"', 'href="%s"' % (up or './'))
    t = t.replace('href="%s"' % LIVE, 'href="%s"' % (up or './'))
    if depth:
        t = t.replace('href="./"', 'href="../"')
    for d in copied:
        t = t.replace('href="%s%s/"' % (LIVE, d), 'href="%s%s/"' % (up, d))
    open(p, 'w', encoding='utf-8').write(t)
print('ok', dest, 'pagine copiate:', ['home'] + sorted(copied))
