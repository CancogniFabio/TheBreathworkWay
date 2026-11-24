"""Ritocchi di struttura richiesti da Fabio (nov 2026), sulle pagine inglesi. Si può rilanciare: non duplica nulla.

Uso: python3 tools/layout.py   (lo lancia tools/rebuild.sh prima di i18n)

- sezioni a step che si fermano allo scroll (data-tbw-pin, gestite da tools/ux.js):
  Home (framework), Offerings (tre step), Corporate (how it works)
- Offerings: finestra "Book this session" con modulo di richiesta (#apply)
- Retreats & Events: Desert Way con bottone verso Ritiri Itineranti
"""
import os, re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# moduli: invio tramite Formspree, come gli altri moduli del sito
BOOK_ACTION = 'https://formspree.io/f/xkjgawre'
RITIRI_DW = 'https://ritiriitineranti.it/marocco'

APPLY = '''<div id="apply" class="tbw-modal" role="dialog" aria-modal="true" aria-labelledby="tbw-apply-title" hidden>
<div class="tbw-modal-box">
<button type="button" class="tbw-modal-x" aria-label="Close">×</button>
<p class="tbw-modal-eye">Book this session</p>
<h2 id="tbw-apply-title" class="tbw-modal-title">Tell me a bit about you</h2>
<p class="tbw-modal-tx">Send your request and I'll get back to you within 48 hours to find a time that works.</p>
<form class="tbw-apply-form" action="%s" method="POST">
<input type="hidden" name="_subject" value="Book this session">
<label><span>Session</span><select name="option">
<option value="Calm my system">Calm my system</option>
<option value="Fix how I breathe">Fix how I breathe</option>
<option value="Go deeper">Go deeper</option>
<option value="6-week program">Make it last</option>
</select></label>
<label><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
<label><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
<label><span>Lisbon or online?</span><select name="where">
<option value="Lisbon">Lisbon</option>
<option value="Online">Online</option>
<option value="Not sure yet">Not sure yet</option>
</select></label>
<label><span>Anything you'd like me to know</span><textarea name="message" rows="4"></textarea></label>
<button type="submit" class="tbw-modal-send">Send request</button>
<p class="tbw-form-note">Your details are only used to reply to your request. <a href="../privacy-policy/">Privacy Policy</a></p>
<p class="tbw-apply-ok" hidden>Thank you, your request has been sent. I'll get back to you soon.</p>
<p class="tbw-apply-err" hidden>Something went wrong. Please write to hello@thebreathworkway.com</p>
</form>
</div>
</div>''' % BOOK_ACTION


def strip_script(soup, needle):
    for sc in soup.find_all('script'):
        if sc.string and needle in sc.string:
            sc.decompose()


def framework(soup):
    cv = soup.find('canvas')
    if cv:
        cv['data-tbw-preview'] = '../assets/media/onion-framework.webp'


def home(soup):
    # "and see exactly where you are" sempre su una riga
    w = soup.select_one('.elementor-element-6bb799d .elementor-widget-container')
    if w and not w.select_one('.tbw-nw'):
        br = w.find('br')
        if br and br.next_sibling and isinstance(br.next_sibling, str) and br.next_sibling.strip():
            txt = br.next_sibling
            sp = soup.new_tag('span', attrs={'class': 'tbw-nw'})
            sp.string = txt.strip()
            txt.replace_with(sp)
    fw = soup.find(id='tbw-fw')
    if fw:
        fw['data-tbw-pin'] = '.tbw-fw-col'
        strip_script(soup, "getElementById('tbw-fw')")


def offerings(soup):
    m = soup.find(id='bwm-method')
    if m and m.find('canvas'):
        m.find('canvas')['data-tbw-preview'] = '../assets/media/onion-offerings.webp'
    if m:
        m['data-tbw-pin'] = '.bwm-step'
        m['data-tbw-pin-mode'] = 'hover'
    # schede: via la lista Where / Length / You leave with, la durata va nel sottotitolo
    for panel in soup.select('#bwo-options .bwo-panel'):
        ul = panel.select_one('ul.bwo-facts')
        tech = panel.select_one('.bwo-tech')
        if ul and tech and not tech.get('data-tbw-len'):
            ln = None
            for li in ul.find_all('li'):
                sp = li.find_all('span')
                if len(sp) == 2 and sp[0].get_text(strip=True) == 'Length':
                    ln = sp[1].get_text(strip=True)
            if ln:
                tech.string = tech.get_text(strip=True) + ' · ' + ln
                tech['data-tbw-len'] = '1'
        if ul:
            ul.decompose()
        if tech and tech.get_text().endswith(' · 6 weeks'):  # già detto nel titolo
            tech.string = tech.get_text()[:-len(' · 6 weeks')]
    if not soup.find(id='apply'):
        frag = BeautifulSoup(APPLY, 'html.parser')
        soup.body.append(frag)


def corporate(soup):
    h = soup.find(id='tbw-how')
    if h:
        # si ferma tutta la sezione, titolo compreso
        for x in [h] + list(h.parents):
            if 'e-parent' in (x.get('class') or []):
                h = x
                break
        h['data-tbw-pin'] = '.tbw-step'
        h['data-tbw-pin-mode'] = 'line'
        strip_script(soup, "getElementById('tbw-how')")


def retreats(soup):
    for sp in soup.select('.tbw-dw-more span'):  # niente freccia
        sp.decompose()
    col = soup.select_one('.elementor-element-5c95f5f')
    if col and not col.select_one('.tbw-dw-more'):
        a = soup.new_tag('a', attrs={'class': 'tbw-dw-more', 'href': RITIRI_DW, 'target': '_blank', 'rel': 'noopener'})
        a.string = 'Explore more'
        wrap = soup.new_tag('div', attrs={'class': 'tbw-dw-cta'})
        wrap.append(a)
        col.append(wrap)


CONTACT_FORM = """<form class="tbw-contact-form" action="%s" method="POST" novalidate>
<input type="hidden" name="_subject" value="Contact form">
<label><span>Full name</span><input type="text" name="name" autocomplete="name" required></label>
<label><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
<label><span>I'm interested in</span><select name="interest" required>
<option value="">Choose one</option>
<option value="1-1">A one-to-one session or programme</option>
<option value="group">Group breathwork and events in Lisbon</option>
<option value="retreat">Joining a retreat</option>
<option value="corporate">Corporate breathwork for my team</option>
<option value="collab">A collaboration</option>
<option value="other">Something else</option>
</select></label>
<div class="tbw-sub" data-for="1-1"><label><span>Which session?</span><select name="session">
<option value="Calm my system">Calm my system · Nervous system regulation</option>
<option value="Fix how I breathe">Fix how I breathe · Breathing mechanics</option>
<option value="Go deeper">Go deeper · Conscious Connected Breathwork</option>
<option value="Make it last">Make it last · 6-week programme</option>
<option value="Not sure yet">Not sure yet, help me choose</option>
</select></label>
<label><span>Lisbon or online?</span><select name="where">
<option value="Lisbon">Lisbon</option><option value="Online">Online</option><option value="Not sure yet">Not sure yet</option>
</select></label></div>
<div class="tbw-sub" data-for="group"><label><span>Which one?</span><select name="event">
<option value="Weekly Breathwork">Weekly Breathwork</option>
<option value="Breathwork Ceremony">Breathwork Ceremony</option>
<option value="Breathwork and Ocean Dip">Breathwork and Ocean Dip</option>
</select></label></div>
<div class="tbw-sub" data-for="retreat"><label><span>Which retreat?</span><select name="retreat">
<option value="The Desert Way, Morocco, 21-27 April 2027">The Desert Way · Morocco, 21-27 April 2027</option>
<option value="Private retreat for my group">A private retreat for my group</option>
</select></label></div>
<div class="tbw-sub" data-for="corporate"><label><span>Company</span><input type="text" name="company" autocomplete="organization"></label>
<label><span>Which format?</span><select name="format">
<option value="Single session">Single session · 60-90 min</option>
<option value="Deep immersion">Deep immersion · 2-3 h</option>
<option value="Weekly reset programme">Weekly reset programme</option>
<option value="Corporate retreat">Corporate retreat · one or more days</option>
<option value="Not sure yet">Not sure yet, let's talk</option>
</select></label>
<label><span>How many people?</span><input type="text" name="team_size" inputmode="numeric"></label></div>
<div class="tbw-sub" data-for="collab"><label><span>What kind of collaboration?</span><select name="collaboration">
<option value="Retreat">I organise retreats</option>
<option value="Event or conference">Event, festival or conference</option>
<option value="Wellness venue or studio">Wellness venue or studio</option>
<option value="Content or media">Content, podcast or media</option>
<option value="Other">Something else</option>
</select></label></div>
<label><span>Your message</span><textarea name="message" rows="5"></textarea></label>
<button type="submit" class="tbw-modal-send">Send message</button>
<p class="tbw-form-note">Your details are only used to reply to your message. <a href="../privacy-policy/">Privacy Policy</a></p>
<p class="tbw-apply-ok" hidden>Thank you, your message has been sent. I'll get back to you within 48 hours.</p>
<p class="tbw-apply-err" hidden>Something went wrong. Please write to hello@thebreathworkway.com</p>
</form>""" % BOOK_ACTION


def contact(soup):
    w = soup.select_one('.elementor-element-78e9bec')
    if w and not w.select_one('.tbw-contact-form'):
        box = w.select_one('.elementor-widget-container') or w
        box.clear()
        box.append(BeautifulSoup(CONTACT_FORM, 'html.parser'))
        w['data-widget_type'] = 'html.default'
        w['class'] = [c for c in w.get('class', []) if c != 'elementor-widget-shortcode'] + ['elementor-widget-html']
    # stili e script di Fluent Forms non servono più
    for el in soup.select('link[href*="fluentform"], link[id*="fluent"], style[id*="fluent"], script[src*="fluentform"], script[id*="fluent"]'):
        el.decompose()


PAGES = {'contact/index.html': contact, 'index.html': home, 'framework/index.html': framework, 'breathwork-lisbon/index.html': offerings,
         'corporate-breathwork/index.html': corporate, 'retreats-events/index.html': retreats}

for f, fn in PAGES.items():
    p = os.path.join(ROOT, f)
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    fn(soup)
    open(p, 'w', encoding='utf-8').write(str(soup))
print('layout ok')
