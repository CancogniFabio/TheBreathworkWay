"""Correzioni dei testi inglesi (refusi, coerenza) applicate a tutte le pagine.

Le correzioni stanno in tools/fixes/text-en.json ({testo originale: testo corretto}),
con le stesse chiavi di tools/i18n/en.json. Se una pagina viene ricopiata dal live,
finalize.py le riapplica. Aggiorna anche le chiavi di tools/i18n/it.json.
Uso: python3 tools/fixes.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs4 import BeautifulSoup, NavigableString
import i18n

ROOT = i18n.ROOT
FIX = json.load(open(os.path.join(ROOT, 'tools', 'fixes', 'text-en.json')))

itf = os.path.join(i18n.DIR, 'it.json')
it = json.load(open(itf))
for old, new in FIX.items():
    if old in it and new not in it:
        it[new] = it[old]
json.dump(it, open(itf, 'w'), ensure_ascii=False, indent=0)

ALT = json.load(open(os.path.join(ROOT, 'tools', 'fixes', 'alt-en.json')))

n = 0
for slug, f in i18n.page_files():
    p = os.path.join(ROOT, f)
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    changed = False
    for node, k in i18n.units(soup.body):
        if k in FIX:
            v = FIX[k]
            if isinstance(node, NavigableString):
                a, b = i18n.lead_trail(str(node))
                node.replace_with(NavigableString(a + BeautifulSoup(v, 'html.parser').get_text() + b))
            else:
                i18n.fill(node, v)
            changed = True; n += 1
    # frammento di script rotto (resto di un header che si nascondeva allo scroll): dava errore in console
    for sc in soup.find_all('script'):
        if sc.string and sc.string.lstrip().startswith('if(currentScroll>lastScroll'):
            sc.decompose(); changed = True
    # emoji di WordPress (immagini da s.w.org) -> emoji normali
    for img in soup.select('img.emoji'):
        img.replace_with(NavigableString(img.get('alt', ''))); changed = True
    for img in soup.find_all('img'):
        if not (img.get('alt') or '').strip():
            name = (img.get('src') or '').rsplit('/', 1)[-1]
            if name in ALT:
                img['alt'] = ALT[name]; changed = True
    head = soup.head
    if head.title and head.title.string and i18n.norm(head.title.string) in FIX:
        head.title.string = FIX[i18n.norm(head.title.string)]; changed = True
    for m in head.find_all('meta'):
        c = m.get('content')
        if c and i18n.norm(c) in FIX:
            m['content'] = BeautifulSoup(FIX[i18n.norm(c)], 'html.parser').get_text(); changed = True
    for el in soup.find_all(True):
        for a in i18n.ATTRS:
            v = el.get(a)
            if isinstance(v, str) and i18n.norm(v) in FIX:
                el[a] = BeautifulSoup(FIX[i18n.norm(v)], 'html.parser').get_text(); changed = True
    for s in soup.find_all('script'):
        if s.get('src') or not s.string:
            continue
        js = s.string
        for k, v in FIX.items():
            if k.startswith('js:'):
                o, w = k[3:], v[3:]
                js = js.replace("'%s'" % o, "'%s'" % w.replace("'", "\\'")).replace('"%s"' % o, '"%s"' % w)
        if js != s.string:
            s.string = js; changed = True
    if changed:
        open(p, 'w', encoding='utf-8').write(str(soup))
print('correzioni applicate:', n)
