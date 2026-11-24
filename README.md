# The Breathwork Way, mockup statico

Copia 1:1 di thebreathworkway.com, ricostruita una pagina al giorno. Anteprima con noindex.

## Stato
- [x] Home (19 nov 2026)
- [x] Framework (20 nov 2026)
- [x] Offerings (21 nov 2026)
- [x] Corporate Breathwork (21 nov 2026)
- [x] Retreats & Events (21 nov 2026)
- [x] About Me (21 nov 2026)
- [x] Insights (21 nov 2026)
- [x] Contact (21 nov 2026)
- [x] Nervous System Test (21 nov 2026)
- [x] Pagine legali: /cookie-policy-copy/, /terms-conditions-2/, /contact-copy/ (21 nov 2026)
- [x] Coherent Breathing /coherent-breathing/ (ha audio: audio copiati; non nel menu) (22 nov 2026)
- [x] Box Breathing /box-breathing/ (ha audio; non nel menu) (22 nov 2026)
- [x] Centering Process /centering-process/ (ha audio; non nel menu) (22 nov 2026)
- [x] Sandy's Retreat /sandys-retreat/ (non nel menu) (22 nov 2026)
- [x] Extra trovate nei link: 3 articoli di Insights, /retreats/, /breathwork-ceremony/, /registration-form-bw-ceremony/ (21 nov 2026)

## Messa online
Vedi GO-LIVE.md (cosa è pronto e cosa resta). `python3 tools/golive.py` crea dist/ per GreenGeeks.
Pagine rinominate nella copia: /privacy-policy/ (era /cookie-policy-copy/), /cookies-policy/ (era /contact-copy/), /terms-conditions/ (era /terms-conditions-2/), /behind-the-guilt-of-slowing-down/ (era guild). finalize.py le gestisce da sé.

## Qualità e coerenza (dopo la copia)
Per rigenerare tutto dopo una modifica: `./tools/rebuild.sh` (seo, footer, fixes, 404, layout, italiano).
Impaginazione iPad/telefono in tools/responsive.css, comportamenti in tools/ux.js, ritocchi HTML in tools/layout.py. Elenco richieste: CAMBI-IPAD.md.
Pipeline di finalize.py: seo.py (titoli, H1, font, CSS di qualità) -> footer.py (footer unico della Home) -> fixes.py (correzioni testi inglesi, tools/fixes/text-en.json) -> i18n.py (pagine /it/).
Ritocchi di stile in tools/quality.css (header e menu mobile, margini su tablet e telefono, Contatti, newsletter).

## Italiano
Pagine italiane in /it/ generate da tools/i18n.py (traduzioni in tools/i18n/it.json, chiave = testo inglese). finalize.py le rigenera da solo: se una pagina inglese cambia, i testi nuovi restano in inglese finché non si aggiungono a it.json (lo script li elenca).

## Da ricordare
- Moduli (newsletter, contatti, prenotazioni) da collegare
- Offerings: "Book this session" apre un modulo di richiesta che invia a Formspree (xkjgawre, lo stesso delle richieste ritiri)
- Framework: modulo newsletter (MailerLite) da collegare
- Offerings: modulo newsletter (MailerLite) da collegare
- Corporate Breathwork: modulo richieste aziende (invia a Formspree come il live) da collegare
- Corporate Breathwork: modulo newsletter (MailerLite) da collegare
- Retreats & Events: modulo richieste (tbw-pr-form) da collegare
- Retreats & Events: modulo newsletter (MailerLite) da collegare
- About Me: modulo newsletter (MailerLite) da collegare
- Insights: modulo newsletter (MailerLite) da collegare
- Contact: modulo contatti rifatto (tools/layout.py), invia a Formspree xkjgawre come Book this session
- Nervous System Test: modulo Brevo (sibforms) da collegare
- Newsletter MailerLite presente anche in Contact, Nervous System Test, pagine legali, articoli, Retreats, Breathwork Ceremony, Registration Form: da collegare
- Sul live /privacy-policy/ e /cookies-policy/ danno 404 (footer di articoli e pagine legali): nella copia sono gli indirizzi giusti
- /offerings/ sul live dà 404: nella copia i link vanno a /breathwork-lisbon/
- Font: solo Antonio e Archivo in assets/fonts; tutti gli altri diventano Archivo (tools/seo.py)
- Immagini ancora collegate al sito WordPress: sostituire con la cartella foto
