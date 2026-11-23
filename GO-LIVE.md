# Messa online su GreenGeeks: cosa resta

Aggiornato il 21 nov 2026.

## Già pronto nel repo
- [x] Un solo H1 per pagina (articoli, pagine legali, Corporate, Offerings, Retreats & Events, Insights). Cambiato solo il tag: aspetto identico, verificato al pixel su 18 pagine a 3 larghezze (`tools/seo.py`, `tools/seo_css.js --check`)
- [x] Tolto il doppio blocco di meta description/og/twitter (vale quello di Rank Math)
- [x] Canonical con l'indirizzo definitivo su ogni pagina
- [x] Titolo e descrizione giusti per Privacy, Cookie e Termini (sul live erano quelli di Contact)
- [x] Indirizzi chiari: /privacy-policy/, /cookies-policy/, /terms-conditions/, /behind-the-guilt-of-slowing-down/ (con redirect 301 dai vecchi)
- [x] Link a /offerings/ (404 sul live) portati a /breathwork-lisbon/
- [x] Pagina 404 con header e footer del sito (`404.html`)
- [x] `golive/.htaccess`: https + www, redirect 301, resti di WordPress, intestazioni di sicurezza, cache e compressione
- [x] `golive/robots.txt` definitivo e sitemap.xml generata
- [x] `python3 tools/golive.py` crea `dist/`, la cartella da caricare in public_html (senza noindex)

- [x] Solo due font, Antonio e Archivo, ospitati nel repo (assets/fonts, 6 file, 192 KB). Lora, Cormorant, Assistant, Inter e gli altri vecchi stili ora usano Archivo
- [x] Versione italiana completa in /it/ con pulsante EN/IT nel menu (desktop e mobile), hreflang e sitemap con le due lingue
- [x] Menu mobile funzionante (senza gli script di WordPress non si apriva)

## Da fare (Claude, quando il computer di Fabio è acceso)
- [x] Solo le immagini usate davvero, nel repo (assets/media, 185 file, 24 MB). Nessun riferimento al vecchio WordPress
- [x] Dati strutturati (JSON-LD di Rank Math) ripuliti: indirizzi nuovi, immagini locali, profili social, versione italiana
- [x] Testo alternativo per le 12 immagini che non l'avevano (inglese e italiano)
- [x] Emoji di WordPress sostituite da emoji normali

## Pagine del live non copiate (decide Fabio: copiarle, reindirizzarle o lasciarle sparire)
Copiate (fuori dal menu, con i loro audio): /coherent-breathing/, /box-breathing/, /centering-process/, /sandys-retreat/ (privata: noindex e fuori dalla sitemap).
Ancora da decidere: /daily-breathwork/, /breathwork-session/, /online-breathwork/, /free-gift/, /health-questionnaire-faro/, /desert-way-form/, /desert-way-feedback-form/, /evaluacion-del-sistema-nervioso-elevare88/, /respiracion-cuadrada/, /respiracion-coherente-2/, negozio WooCommerce (/shop/, /product/daily-breathing-practice/, /cart/, /checkout-2/, /my-account/)

## Moduli (uno alla volta, decide Fabio)
Obiettivo: modulo normale che manda un'email a Fabio, poi eventualmente anche a Brevo.
- [ ] Contact: Fluent Forms (funziona solo dentro WordPress): da rifare
- [ ] Corporate Breathwork: richieste aziende, già su Formspree
- [ ] Retreats & Events: richieste (tbw-pr-form)
- [ ] Nervous System Test: modulo Brevo (sibforms)
- [ ] Newsletter MailerLite in quasi tutte le pagine: tenerla o passare a Brevo
- [ ] Anti spam su tutti i moduli

## Legale (da far controllare a un professionista)
- [x] Termini riscritti (23 nov 2026): recesso 14 giorni, prodotti digitali, responsabilità conforme al diritto dei consumatori. Politica di cancellazione (24 ore sessioni, 48 ore eventi) da confermare con Fabio
- [x] Note privacy su newsletter (footer), Contatti, Corporate (tolto il consenso SMS obbligatorio), Test del sistema nervoso
- [ ] Test del sistema nervoso: newsletter facoltativa con casella separata (va impostata nel modulo Brevo e nello scenario Make)
- [ ] Traduzioni italiane di Privacy, Cookie, Termini e modulo di iscrizione: da rileggere
- [x] Banner cookie non serve: il sito non carica nulla da terzi (verificato, tranne le 6 foto di /sandys-retreat/ prese da riadassouel.com e squarespace). Se si aggiungono video, mappe o statistiche serve il banner
- [x] Privacy Policy riscritta (23 nov 2026): moduli, dati sanitari, MailerLite, Brevo, Formspree, Make, Calendly, GreenGeeks, trasferimenti, conservazione, reclamo a Garante o CNPD
- [x] Cookie Policy riscritta: solo cookie tecnici, nessun banner
- [ ] Portogallo: link al Livro de Reclamações Eletrónico, informazioni sulla risoluzione alternativa delle controversie, dati aziendali (nome, NIF, indirizzo) nel footer o nei Termini
- [ ] Registration Form della cerimonia: contiene dati sanitari, serve consenso esplicito e conservazione sicura

## Il giorno del passaggio
- [ ] Email del dominio: non toccare i record MX quando si sposta il DNS
- [ ] SSL attivo su GreenGeeks prima di cambiare il DNS
- [ ] Caricare `dist/` in public_html, provare https://, www, 404 e qualche vecchio indirizzo
- [ ] Google Search Console: verificare il dominio, inviare sitemap.xml, controllare la copertura nelle settimane dopo
- [ ] Statistiche: scegliere cosa usare al posto di Google Analytics (con il banner cookie)
- [ ] Tenere WordPress acceso finché le immagini non sono tutte nel repo
