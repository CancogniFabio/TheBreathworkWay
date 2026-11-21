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
- [x] Extra trovate nei link: 3 articoli di Insights, /retreats/, /breathwork-ceremony/, /registration-form-bw-ceremony/ (21 nov 2026)

## Messa online
Vedi GO-LIVE.md (cosa è pronto e cosa resta). `python3 tools/golive.py` crea dist/ per GreenGeeks.
Pagine rinominate nella copia: /privacy-policy/ (era /cookie-policy-copy/), /cookies-policy/ (era /contact-copy/), /terms-conditions/ (era /terms-conditions-2/), /behind-the-guilt-of-slowing-down/ (era guild). finalize.py le gestisce da sé.

## Da ricordare
- Moduli (newsletter, contatti, prenotazioni) da collegare
- Framework: modulo newsletter (MailerLite) da collegare
- Offerings: modulo newsletter (MailerLite) da collegare
- Corporate Breathwork: modulo richieste aziende (invia a Formspree come il live) da collegare
- Corporate Breathwork: modulo newsletter (MailerLite) da collegare
- Retreats & Events: modulo richieste (tbw-pr-form) da collegare
- Retreats & Events: modulo newsletter (MailerLite) da collegare
- About Me: modulo newsletter (MailerLite) da collegare
- Insights: modulo newsletter (MailerLite) da collegare
- Contact: modulo contatti (Fluent Forms, WordPress) da collegare
- Nervous System Test: modulo Brevo (sibforms) da collegare
- Newsletter MailerLite presente anche in Contact, Nervous System Test, pagine legali, articoli, Retreats, Breathwork Ceremony, Registration Form: da collegare
- Sul live /privacy-policy/ e /cookies-policy/ danno 404 (footer di articoli e pagine legali): nella copia sono gli indirizzi giusti
- /offerings/ sul live dà 404: nella copia i link vanno a /breathwork-lisbon/
- Font Lora e Assistant copiati in assets/bcf-fonts (il server live li blocca per altri domini)
- Menu in alto ancora in Inter (dal tema Astra): portarlo ad Archivo
- Immagini ancora collegate al sito WordPress: sostituire con la cartella foto
