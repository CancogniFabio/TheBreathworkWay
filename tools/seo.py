"""Sistemazioni SEO su tutte le pagine del mockup, senza cambiare l'aspetto.

Uso: python3 tools/seo.py   (lo lancia anche finalize.py alla fine)

- toglie il primo blocco di meta (descrizione/og/twitter) lasciato da un vecchio plugin:
  sul live ogni pagina ne ha due, vale quello di Rank Math che viene dopo <title>
- rimette il canonical con l'indirizzo definitivo
- titolo e descrizione giusti per le pagine legali (sul live erano copiati da Contact)
- un solo H1 per pagina: cambia solo il tag dei titoli elencati in HEADINGS.
  Lo stile resta identico: tools/seo_css.js misura cosa cambierebbe (di solito l'interlinea)
  e lo salva in tools/seo-css.json, che qui viene inserito come CSS della pagina.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://www.thebreathworkway.com/'

# (pagina, inizio del testo, tag attuale, tag nuovo)
HEADINGS = [
    # articoli e pagine legali: il titolo della pagina era H2 e mancava l'H1
    ('behind-the-guilt-of-slowing-down', 'Guilt of Slowing Down is not', 'h2', 'h1'),
    ('breathwork-for-stress-and-anxiety-science', 'Breathwork for Stress and Anxiety:', 'h2', 'h1'),
    ('breathwork-vs-meditation-for-executives', 'Breathwork vs Meditation:', 'h2', 'h1'),
    ('privacy-policy', 'Privacy Policy', 'h2', 'h1'),
    ('cookies-policy', 'Cookie Policy', 'h2', 'h1'),
    ('terms-conditions', 'Terms &amp; Conditions', 'h2', 'h1'),
    # Corporate Breathwork aveva 8 H1
    ('corporate-breathwork', 'Breathwork for Companies', 'h1', 'h2'),
    ('corporate-breathwork', 'SINGLE SESSION', 'h1', 'h3'),
    ('corporate-breathwork', 'DEEP IMMERSION', 'h1', 'h3'),
    ('corporate-breathwork', 'WEEKLY RESET PROGRAM', 'h1', 'h3'),
    ('corporate-breathwork', 'ONE DAY FORMAT', 'h1', 'h3'),
    ('corporate-breathwork', 'MULTI-DAY FORMAT', 'h1', 'h3'),
    ('corporate-breathwork', 'questions', 'h1', 'h2'),
    # due H1 nella stessa pagina
    ('breathwork-lisbon', 'The Breathwork Way Offerings', 'h1', 'h2'),
    ('retreats-events', 'FEATURED RETREAT - INNER TRAVELS', 'h1', 'h2'),
    # titoli degli articoli in Insights: erano H6 (salto di livelli)
    ('insights', 'The Guilt of Slowing Down', 'h6', 'h2'),
    ('insights', 'Breathwork for Stress and Anxiety', 'h6', 'h2'),
    ('insights', 'Breathwork vs Meditation', 'h6', 'h2'),
]

META = {
    'privacy-policy': ('Privacy Policy | The Breathwork Way',
                       'Privacy Policy of The Breathwork Way: what personal data is collected, how it is used and how it is protected.'),
    'cookies-policy': ('Cookie Policy | The Breathwork Way',
                       'Cookie Policy of The Breathwork Way: which cookies the website uses and how you can manage them.'),
    'terms-conditions': ('Terms & Conditions | The Breathwork Way',
                         'Terms and Conditions for using The Breathwork Way website, sessions, digital products and online courses.'),
}


def pages():
    yield 'home', os.path.join(ROOT, 'index.html')
    for d in sorted(os.listdir(ROOT)):
        f = os.path.join(ROOT, d, 'index.html')
        if os.path.isfile(f) and d not in ('assets', 'tools'):
            yield d, f


def fix_head(slug, t):
    hi = t.index('</head>')
    head, rest = t[:hi], t[hi:]
    ti = head.find('<title>')
    # blocco doppio prima di <title> (solo se dopo c'è quello buono di Rank Math)
    if ti > 0 and 'name="description"' in head[ti:]:
        pre = re.sub(r'<meta\b[^>]*(name="description"|property="og:[^"]*"|name="twitter:[^"]*")[^>]*>', '', head[:ti])
        head = pre + head[ti:]
    # canonical
    head = re.sub(r'<link rel="canonical"[^>]*>', '', head)
    url = LIVE if slug == 'home' else LIVE + slug + '/'
    head = head.replace('</title>', '</title><link rel="canonical" href="%s">' % url, 1)
    if slug in META:
        title, desc = META[slug]
        te, de = html.escape(title, quote=True), html.escape(desc, quote=True)
        head = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % te, head, count=1)
        head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + de, head)
        head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', r'\g<1>' + te, head)
        head = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*', r'\g<1>' + de, head)
    return head + rest


def fix_headings(slug, t):
    n = 0
    for pg, txt, old, new in HEADINGS:
        if pg != slug:
            continue
        n += 1
        cls = 'tbw-hfix-%d' % n
        if cls in t:
            continue
        m = None
        for m in re.finditer(r'<%s\b([^>]*)>(.*?)</%s>' % (old, old), t, re.S):
            text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
            if text.startswith(txt):
                break
        else:
            raise SystemExit('titolo non trovato: %s %s' % (slug, txt))
        attrs = m.group(1)
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="%s ' % cls, 1)
        else:
            attrs += ' class="%s"' % cls
        attrs += ' data-tbw-orig="%s"' % old
        t = t[:m.start()] + '<%s%s>%s</%s>' % (new, attrs, m.group(2), new) + t[m.end():]
    return t


def fix_css(slug, t):
    t = re.sub(r'<style id="tbw-seo-css">.*?</style>', '', t, flags=re.S)
    f = os.path.join(ROOT, 'tools', 'seo-css.json')
    css = json.load(open(f)).get(slug, '') if os.path.exists(f) else ''
    if css:
        t = t.replace('</head>', '<style id="tbw-seo-css">%s</style></head>' % css, 1)
    return t


for slug, f in pages():
    t = open(f, encoding='utf-8').read()
    t = fix_head(slug, t)
    t = fix_headings(slug, t)
    t = fix_css(slug, t)
    open(f, 'w', encoding='utf-8').write(t)
print('seo ok')
