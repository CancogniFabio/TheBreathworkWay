"""Un solo footer per tutto il sito: quello della Home (newsletter "Breathe on Sunday").

Alcune pagine avevano ancora il footer vecchio ("Stay Informed") e /retreats/ non ne aveva.
Qui il footer della Home sostituisce gli altri, con il suo CSS e i link resi relativi.
Uso: python3 tools/footer.py   (lo lancia seo.py)
"""
import os, re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Breathwork and nervous system regulation in Lisbon'


def css_rules(css):
    """divide il CSS in (prefisso @media o '', selettore, regola completa)"""
    out, i, n = [], 0, len(css)

    def block_end(j):
        depth = 0
        while j < n:
            if css[j] == '{':
                depth += 1
            elif css[j] == '}':
                depth -= 1
                if depth == 0:
                    return j
            j += 1
        return n - 1
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        head = css[i:j].strip()
        e = block_end(j)
        if head.startswith('@media') or head.startswith('@supports'):
            inner = css[j + 1:e]
            for _, sel, rule in css_rules(inner):
                out.append((head, sel, rule))
        elif not head.startswith('@'):
            out.append(('', head, css[i:e + 1].strip()))
        i = e + 1
    return out


def footer_block(soup):
    """il blocco footer: l'ultima sezione corta col marchio, più le sezioni che la seguono"""
    secs = soup.select('.e-con.e-parent')
    cand = [s for s in secs[-7:] if BRAND in s.get_text(' ', strip=True) and len(s.get_text(' ', strip=True)) < 900]
    if not cand:
        return None
    s = cand[-1]
    return [s] + list(s.find_next_siblings())


def tokens(nodes):
    t = set()
    for n in nodes:
        for el in [n] + n.find_all(True):
            if el.get('id'):
                t.add('#' + el['id'])
            for c in el.get('class') or []:
                t.add('.' + c)
    return t


def main():
    home = BeautifulSoup(open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read(), 'html.parser')
    hb = footer_block(home)
    home_css = home.find('style', id='tbw-used-css').string or ''
    rules = css_rules(home_css)
    block_html = ''.join(str(x) for x in hb)
    btok = tokens(hb)
    done = []
    for d in sorted(os.listdir(ROOT)):
        f = os.path.join(ROOT, d, 'index.html')
        if d in ('it', 'dist', 'assets', 'tools') or not os.path.isfile(f):
            continue
        t = open(f, encoding='utf-8').read()
        soup = BeautifulSoup(t, 'html.parser')
        old = footer_block(soup)
        page_tok = tokens([soup.body]) - (tokens(old) if old else set())
        # link relativi: la Home è alla radice, questa pagina un livello sotto
        frag = BeautifulSoup(block_html, 'html.parser')
        for a in frag.find_all(href=True):
            h = a['href']
            if not re.match(r'^(https?:|mailto:|tel:|#|\.\./|/)', h):
                a['href'] = '../' + (h if h != './' else '')
        if old:
            anchor = old[0]
            for x in old[1:]:
                x.decompose()
        else:
            last = [x for x in soup.select('.e-con.e-parent') if not x.find_parent(class_='e-parent')][-1]
            anchor = soup.new_tag('div')
            last.insert_after(anchor)
        first = frag.find(True)
        anchor.replace_with(frag)
        # CSS degli elementi del footer che la pagina non ha
        need = btok
        css = []
        for media, sel, rule in rules:
            toks = set(re.findall(r'[.#][A-Za-z0-9_-]+', sel))
            if toks & need and not (toks & {'.elementor-kit-47'}):
                css.append('%s{%s}' % (media, rule) if media else rule)
        # le regole della Home sono legate al suo contenitore (.elementor-<id>): uso quello di questa pagina
        hid = home.find(attrs={'data-elementor-type': 'wp-page'})['data-elementor-id']
        wrap = first.find_parent(attrs={'data-elementor-id': True})
        if wrap:
            css = [re.sub(r'\.elementor-%s(?![\w-])' % hid, '.elementor-%s' % wrap['data-elementor-id'], c) for c in css]
        # se la pagina non ha altri moduli MailerLite, tolgo le sue regole MailerLite (restano quelle della Home)
        others = [e for e in soup.select('[id^=mlb2-], .ml-form-embedContainer') if not e.find_parent(attrs={'data-id': hb[0].get('data-id')})]
        used = soup.find('style', id='tbw-used-css')
        if not others and used and used.string:
            keep = []
            for media, sel, rule in css_rules(used.string):
                if re.search(r'(\.ml-|#mlb2-|\.ml_)', sel):
                    continue
                keep.append('%s{%s}' % (media, rule) if media else rule)
            # le regole non-regola (@font-face, @keyframes) restano: le ricopio in testa
            extra = re.findall(r'@(?:font-face|keyframes)[^{]*\{(?:[^{}]|\{[^{}]*\})*\}', used.string)
            used.string = '\n'.join(extra + keep)
        st = soup.find('style', id='tbw-footer-css')
        if st:
            st.decompose()
        st = soup.new_tag('style', attrs={'id': 'tbw-footer-css'})
        st.string = '\n'.join(css)
        soup.find('style', id='tbw-used-css').insert_after(st)
        open(f, 'w', encoding='utf-8').write(str(soup))
        done.append(d)
    print('footer unificato in:', ', '.join(done) or 'nessuna pagina')


if __name__ == '__main__':
    main()
