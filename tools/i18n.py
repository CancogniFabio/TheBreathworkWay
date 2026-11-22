"""Versione italiana del sito: /it/... con gli stessi file, testi tradotti.

Uso:
  python3 tools/i18n.py extract   -> tools/i18n/en.json (tutti i testi da tradurre, senza doppioni)
  python3 tools/i18n.py build     -> crea it/..., aggiunge il pulsante EN/IT e gli hreflang
Le traduzioni stanno in tools/i18n/it.json ({testo inglese: testo italiano}).
Un testo senza traduzione resta in inglese e viene segnalato.
"""
import json, os, re, sys, copy
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://www.thebreathworkway.com/'
DIR = os.path.join(ROOT, 'tools', 'i18n')
INLINE = {'a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'em', 'i', 'kbd', 'mark', 'q', 's', 'small',
          'span', 'strong', 'sub', 'sup', 'u', 'wbr', 'time', 'font'}
SKIP = {'script', 'style', 'noscript', 'svg', 'template', 'head', 'iframe', 'video', 'audio', 'canvas', 'math'}
ATTRS = ('alt', 'title', 'placeholder', 'aria-label', 'data-label', 'data-placeholder')
META = ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description', 'og:image:alt')
# script con testi da tradurre (quiz, messaggi dei moduli); le altre stringhe JS restano com'erano
JS_MIN = re.compile(r'[A-Za-zÀ-ÿ]{2,}')
JS_BAD = re.compile(r'[{}<>]|\.(querySelector|style)|^[.#\[]|https?:|\$\{|^[a-z]+(-[a-z0-9]+)+$|^(btn|nav|build-row|svg|Layer)\b|^\(prefers|px |^[a-z_]+$|;|=')
NOT_TEXT = re.compile(r'^[\s\d.,:;·•|/\\\-–—+*#@%&()\[\]→←↓↑✓✔×€$"\'’“”…!?]*$')


# pagine a sé, senza versione italiana
NO_IT = {'sandys-retreat'}


def page_files():
    out = [('home', 'index.html')]
    for d in sorted(os.listdir(ROOT)):
        if d in ('it', 'dist', 'assets', 'tools', 'golive'):
            continue
        if os.path.isfile(os.path.join(ROOT, d, 'index.html')):
            out.append((d, d + '/index.html'))
    return out


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def bare(el):
    """contenuto dell'elemento con i tag ma senza attributi (quello che vede chi traduce)"""
    parts = []
    for c in el.children:
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            parts.append(str(c).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        elif isinstance(c, Tag):
            if c.name in ('br', 'wbr'):
                parts.append('<%s>' % c.name)
            else:
                parts.append('<%s>%s</%s>' % (c.name, bare(c), c.name))
    return ''.join(parts)


def is_inline_only(el):
    for d in el.descendants:
        if isinstance(d, Tag) and (d.name not in INLINE or d.name in SKIP):
            return False
    return True


def has_text(el):
    return any(isinstance(d, NavigableString) and not isinstance(d, Comment) and d.strip() for d in el.descendants)


def units(body):
    """(nodo, chiave): elementi con solo testo e tag in linea, oppure testi sciolti"""
    out = []

    def walk(el):
        for c in list(el.children):
            if isinstance(c, Comment):
                continue
            if isinstance(c, NavigableString):
                if c.strip() and not NOT_TEXT.match(str(c)):
                    out.append((c, norm(str(c)).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')))
                continue
            if not isinstance(c, Tag) or c.name in SKIP:
                continue
            if c.name in ('textarea',):
                continue
            if has_text(c) and is_inline_only(c) and c.name not in ('br',):
                k = norm(bare(c))
                if not NOT_TEXT.match(re.sub(r'<[^>]+>', '', k)):
                    out.append((c, k))
                continue
            walk(c)
    walk(body)
    return out


def js_strings(soup):
    found = []
    for s in soup.find_all('script'):
        if s.get('src') or (s.get('type') and s['type'] != 'text/javascript'):
            continue
        js = s.string or ''
        for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"", js):
            v = m.group(1) if m.group(1) is not None else m.group(2)
            vt = re.sub(r'</?(em|strong|b|i|br|span)>', '', v) if v else v
            if v and JS_MIN.search(vt) and not JS_BAD.search(vt):
                found.append(v)
    return found


def attr_texts(soup):
    out = []
    for el in soup.find_all(True):
        if el.name in SKIP:
            continue
        for a in ATTRS:
            v = el.get(a)
            if isinstance(v, str) and JS_MIN.search(v) and not v.startswith(('http', '/', '.')):
                out.append(norm(v))
        if el.name == 'input' and el.get('type') in ('submit', 'button') and el.get('value'):
            out.append(norm(el['value']))
    head = soup.head
    if head:
        if head.title and head.title.string:
            out.append(norm(head.title.string))
        for m in head.find_all('meta'):
            if (m.get('name') or m.get('property')) in META and m.get('content'):
                out.append(norm(m['content']))
    return out


def extract():
    keys = {}
    for slug, f in page_files():
        if slug in NO_IT:
            continue
        soup = BeautifulSoup(open(os.path.join(ROOT, f), encoding='utf-8').read(), 'html.parser')
        for old in soup.select('.tbw-lang'):
            old.decompose()
        for _, k in units(soup.body):
            keys.setdefault(k, []).append(slug)
        for k in attr_texts(soup):
            keys.setdefault(k, []).append(slug)
        for k in js_strings(soup):
            keys.setdefault('js:' + k, []).append(slug)
    os.makedirs(DIR, exist_ok=True)
    data = {k: sorted(set(v)) for k, v in keys.items()}
    json.dump(data, open(os.path.join(DIR, 'en.json'), 'w'), ensure_ascii=False, indent=0)
    itf = os.path.join(DIR, 'it.json')
    it = json.load(open(itf)) if os.path.exists(itf) else {}
    print(len(data), 'testi;', sum(1 for k in data if k not in it), 'da tradurre')


# ---------- build ----------

def fill(el, it_html):
    """mette la traduzione nell'elemento, ridando ai tag gli attributi originali (in ordine)"""
    pool = {}
    for d in el.find_all(True):
        pool.setdefault(d.name, []).append(d.attrs)
    frag = BeautifulSoup(it_html, 'html.parser')
    for d in frag.find_all(True):
        q = pool.get(d.name)
        if q:
            d.attrs = copy.deepcopy(q.pop(0))
    el.clear()
    for c in list(frag.contents):
        el.append(c)


def lead_trail(s):
    m = re.match(r'^(\s*).*?(\s*)$', s, re.S)
    return m.group(1), m.group(2)


TOGGLE_CSS = ('.tbw-lang>a.menu-link{font-size:.8em;letter-spacing:.08em;opacity:.75}'
              '.tbw-lang>a.menu-link:hover{opacity:1}'
              '.tbw-lang .tbw-lang-on{font-weight:700}')
MENU_JS = ("(function(){var b=document.querySelector('#ast-mobile-header .menu-toggle');if(!b)return;"
           "b.addEventListener('click',function(){var o=!document.body.classList.contains('ast-main-header-nav-open');"
           "document.body.classList.toggle('ast-main-header-nav-open',o);document.body.classList.toggle('ast-header-break-point',o);"
           "b.classList.toggle('toggled',o);b.setAttribute('aria-expanded',o?'true':'false');});})();")


def add_common(soup, slug, lang):
    """pulsante EN/IT nei due menu, hreflang, menu mobile funzionante"""
    for old in soup.select('.tbw-lang, link[hreflang], #tbw-lang-css, #tbw-menu-js'):
        old.decompose()
    path = '' if slug == 'home' else slug + '/'
    if lang == 'en':
        target = ('it/' if slug == 'home' else '../it/' + path)
    else:
        target = ('../' if slug == 'home' else '../../' + path)
    label_on, label_off = ('EN', 'IT') if lang == 'en' else ('IT', 'EN')
    for ul in soup.select('#ast-hf-menu-1, #ast-hf-mobile-menu'):
        li = soup.new_tag('li', attrs={'class': 'menu-item tbw-lang'})
        a = soup.new_tag('a', attrs={'class': 'menu-link', 'href': target, 'hreflang': 'it' if lang == 'en' else 'en',
                                     'lang': 'it' if lang == 'en' else 'en',
                                     'aria-label': 'Versione italiana' if lang == 'en' else 'English version'})
        a.string = label_off
        li.append(a)
        ul.append(li)
    head = soup.head
    for hl, url in (('en', LIVE + path), ('it', LIVE + 'it/' + path), ('x-default', LIVE + path)):
        head.append(soup.new_tag('link', attrs={'rel': 'alternate', 'hreflang': hl, 'href': url}))
    st = soup.new_tag('style', attrs={'id': 'tbw-lang-css'})
    st.string = TOGGLE_CSS
    head.append(st)
    sc = soup.new_tag('script', attrs={'id': 'tbw-menu-js'})
    sc.string = MENU_JS
    soup.body.append(sc)


def build():
    it = json.load(open(os.path.join(DIR, 'it.json')))
    missing = {}
    for slug, f in page_files():
        if slug in NO_IT:
            continue
        src = os.path.join(ROOT, f)
        raw = open(src, encoding='utf-8').read()
        # pagina inglese: solo pulsante + hreflang + menu mobile
        soup = BeautifulSoup(raw, 'html.parser')
        add_common(soup, slug, 'en')
        open(src, 'w', encoding='utf-8').write(str(soup))
        # pagina italiana
        soup = BeautifulSoup(raw, 'html.parser')
        for old in soup.select('.tbw-lang'):
            old.decompose()
        for node, k in units(soup.body):
            v = it.get(k)
            if v is None:
                missing.setdefault(k, slug)
                continue
            if isinstance(node, NavigableString):
                a, b = lead_trail(str(node))
                node.replace_with(NavigableString(a + BeautifulSoup(v, 'html.parser').get_text() + b))
            else:
                fill(node, v)
        for el in soup.find_all(True):
            for a in ATTRS:
                v = el.get(a)
                if isinstance(v, str) and norm(v) in it:
                    el[a] = BeautifulSoup(it[norm(v)], 'html.parser').get_text()
            if el.name == 'input' and el.get('type') in ('submit', 'button') and el.get('value') and norm(el['value']) in it:
                el['value'] = BeautifulSoup(it[norm(el['value'])], 'html.parser').get_text()
        head = soup.head
        if head.title and head.title.string and norm(head.title.string) in it:
            head.title.string = BeautifulSoup(it[norm(head.title.string)], 'html.parser').get_text()
        for m in head.find_all('meta'):
            key = m.get('name') or m.get('property')
            if key in META and m.get('content') and norm(m['content']) in it:
                m['content'] = BeautifulSoup(it[norm(m['content'])], 'html.parser').get_text()
            if key == 'og:locale':
                m['content'] = 'it_IT'
            if key == 'og:url' and m.get('content', '').startswith(LIVE):
                m['content'] = LIVE + 'it/' + m['content'][len(LIVE):]
        for s in soup.find_all('script'):
            if s.get('src') or not s.string:
                continue
            js = s.string
            for k, v in it.items():
                if k.startswith('js:') and k[3:] in js:
                    o = k[3:]
                    vv = v.replace("'", "\\'") if True else v
                    js = js.replace("'%s'" % o, "'%s'" % vv).replace('"%s"' % o, '"%s"' % v.replace('"', '\\"'))
            s.string = js
        ld = soup.find('script', id='tbw-ld')
        if ld and ld.string:
            path_ = '' if slug == 'home' else slug + '/'
            enu, itu = LIVE + path_, LIVE + 'it/' + path_
            j = json.loads(ld.string.replace('<\\/', '</'))
            def walk(o):
                if isinstance(o, dict):
                    for k2, v2 in list(o.items()):
                        if isinstance(v2, str):
                            if k2 in ('@id', 'url') and (v2 == enu or v2.startswith(enu + '#')) and o.get('@type') not in ('WebSite',):
                                o[k2] = itu + v2[len(enu):]
                            elif k2 == 'inLanguage':
                                o[k2] = 'it-IT'
                            elif k2 in ('name', 'headline', 'description') and norm(v2) in it:
                                o[k2] = BeautifulSoup(it[norm(v2)], 'html.parser').get_text()
                        else:
                            walk(v2)
                elif isinstance(o, list):
                    for x in o:
                        walk(x)
            for n in j.get('@graph', []):
                if n.get('@type') in ('WebPage', 'BlogPosting', 'Article', 'BreadcrumbList', 'Service', 'FAQPage'):
                    walk(n)
            ld.string = json.dumps(j, ensure_ascii=False).replace('</', '<\\/')
        if soup.html:
            soup.html['lang'] = 'it-IT'
        can = soup.find('link', rel='canonical')
        path = '' if slug == 'home' else slug + '/'
        if can:
            can['href'] = LIVE + 'it/' + path
        add_common(soup, slug, 'it')
        out = str(soup)
        # un livello più in profondità: assets e font
        if slug == 'home':
            out = re.sub(r'(?<![\w./-])assets/', '../assets/', out)
        else:
            out = re.sub(r'(?<![\w./-])\.\./assets/', '../../assets/', out)
        dest = os.path.join(ROOT, 'it', f)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(out)
    print('it ok;', len(missing), 'testi senza traduzione')
    for k, s in list(missing.items())[:30]:
        print('  manca', s, k[:80])


if __name__ == '__main__':
    {'extract': extract, 'build': build}[sys.argv[1]]()
