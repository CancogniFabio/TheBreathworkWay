"""Pulisce un file estratto e lo salva nel mockup.

Uso: python3 tools/finalize.py <file_estratto.txt> <slug>
slug "home" -> index.html; altrimenti <slug>/index.html.
Poi riscrive in TUTTE le pagine del mockup i link alle pagine già copiate,
così puntano alla copia invece che al sito live.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://www.thebreathworkway.com/'
# indirizzi del live che nella copia hanno un nome più chiaro (sul nuovo hosting: redirect 301 in .htaccess)
RENAMED = {
    'cookie-policy-copy': 'privacy-policy',      # contiene la Privacy Policy
    'contact-copy': 'cookies-policy',            # contiene la Cookie Policy
    'terms-conditions-2': 'terms-conditions',
    'behind-the-guild-of-slowing-down': 'behind-the-guilt-of-slowing-down',
    'offerings': 'breathwork-lisbon',            # /offerings/ sul live dà 404, la pagina Offerings è questa
}

src, slug = sys.argv[1], sys.argv[2]
slug = RENAMED.get(slug, slug)
s = open(src, encoding='utf-8').read()
s = re.sub(r'<link\b[^>]*rel="(alternate|EditURI|https://api\.w\.org/|shortlink|canonical|pingback)"[^>]*>', '', s)
s = re.sub(r'<meta\b[^>]*name="generator"[^>]*>', '', s)
dest = os.path.join(ROOT, 'index.html') if slug == 'home' else os.path.join(ROOT, slug, 'index.html')
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, 'w', encoding='utf-8').write(s)


def fix_css(t):
    # ripara i resti delle @keyframes non usate (blocchi orfani che rompono il CSS successivo)
    if 'id="tbw-used-css">' not in t:
        return t
    a = t.index('id="tbw-used-css">') + 18
    b = t.index('</style>', a)
    css = re.sub(r'@@KF@@[^@]+@@', '', t[a:b])
    css = re.sub(r'\n\n(?:[ \t]+[^\n]*\{[^\n]*\}[ \t]*\n)+\}', '\n', css)
    return t[:a] + css + t[b:]

# pagine già copiate = cartelle con index.html
copied = [d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, 'index.html')) and d not in ('it', 'dist')]
pages = [os.path.join(ROOT, 'index.html')] + [os.path.join(ROOT, d, 'index.html') for d in copied]
for p in pages:
    depth = 0 if os.path.dirname(p) == ROOT else 1
    up = '../' * depth
    t = fix_css(open(p, encoding='utf-8').read())
    # sul live lo script di Elementor aggiunge e-lazyloaded quando la sezione entra nello schermo;
    # senza script le immagini di sfondo restano nascoste (su telefono il testo bianco finisce su fondo chiaro)
    t = re.sub(r'class="([^"]*\be-parent\b)(?![^"]*e-lazyloaded)([^"]*)"', r'class="\1\2 e-lazyloaded"', t)
    # font Lora e Assistant: il server live non li concede ad altri domini, quindi stanno nel repo
    t = t.replace(LIVE + 'wp-content/bcf-fonts/', up + 'assets/bcf-fonts/')
    t = t.replace('href="./"', 'href="%s"' % (up or './'))
    t = t.replace('href="%s"' % LIVE, 'href="%s"' % (up or './'))
    if depth:
        t = t.replace('href="./"', 'href="../"')
    for a, b in RENAMED.items():
        t = t.replace('href="%s%s/"' % (LIVE, a), 'href="%s%s/"' % (up, b))
        t = re.sub(r'href="((?:\.\./)?)%s/"' % re.escape(a), r'href="\1%s/"' % b, t)
        t = t.replace('content="%s%s/"' % (LIVE, a), 'content="%s%s/"' % (LIVE, b))
    for d in copied:
        t = t.replace('href="%s%s/"' % (LIVE, d), 'href="%s%s/"' % (up, d))
    open(p, 'w', encoding='utf-8').write(t)
print('ok', dest, 'pagine copiate:', ['home'] + sorted(copied))

# sistemazioni SEO (titoli, H1/H2, canonical) senza cambiare l'aspetto
import subprocess
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'seo.py')], check=True)
# footer unico (quello della Home)
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'footer.py')], check=True)
# correzioni dei testi inglesi
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'fixes.py')], check=True)
# pagina 404 (dalla pagina Termini)
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'make_404.py')], check=True)
# versione italiana (/it/) e pulsante EN/IT
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'i18n.py'), 'extract'], check=True)
subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'i18n.py'), 'build'], check=True)
