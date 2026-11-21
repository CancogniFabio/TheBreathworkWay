"""Crea 404.html partendo dalla pagina Terms & Conditions (stesso header, footer e stile).
I link sono assoluti dalla radice (/...) perché la 404 viene mostrata a qualsiasi indirizzo.
Uso: python3 tools/make_404.py
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(ROOT, 'terms-conditions', 'index.html'), encoding='utf-8').read()
t = t.replace('>Terms &amp; Conditions</h1>', '>Page not found</h1>', 1)
a = t.index('elementor-element-cb94a80')
s = t.index('<div class="elementor-widget-container">', a) + len('<div class="elementor-widget-container">')
e = t.index('</div></div></div></div>', s)
body = ('<p>The page you are looking for does not exist or has moved.</p>'
        '<p><a href="/">Back to the home page</a> &middot; <a href="/breathwork-lisbon/">Offerings</a> &middot; '
        '<a href="/insights/">Insights</a> &middot; <a href="/contact/">Contact</a></p>')
t = t[:s] + body + t[e:]
t = re.sub(r'<title>[^<]*</title>', '<title>Page not found | The Breathwork Way</title>', t, count=1)
t = re.sub(r'<link rel="canonical"[^>]*>', '', t)
t = re.sub(r'<meta[^>]*(name="description"|property="og:[^"]*"|name="twitter:[^"]*")[^>]*>', '', t)
t = re.sub(r'<meta name="robots" content="follow, index[^"]*">', '', t)
t = t.replace('href="../"', 'href="/"').replace('href="../', 'href="/').replace('url("../assets/', 'url("/assets/').replace('src="../', 'src="/')
open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(t)
print('404.html ok')
