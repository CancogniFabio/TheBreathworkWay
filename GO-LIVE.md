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
- [ ] Copiare nel repo solo le immagini e i video usati davvero nelle pagine (niente libreria media intera)
- [ ] Rimettere i dati strutturati (JSON-LD di Rank Math) presi dal live
- [ ] Testo alternativo per le 13 immagini senza alt
- [ ] Scaricare la sitemap del live per trovare eventuali pagine o articoli non copiati e aggiungere i redirect

## Moduli (uno alla volta, decide Fabio)
Obiettivo: modulo normale che manda un'email a Fabio, poi eventualmente anche a Brevo.
- [ ] Contact: Fluent Forms (funziona solo dentro WordPress): da rifare
- [ ] Corporate Breathwork: richieste aziende, già su Formspree
- [ ] Retreats & Events: richieste (tbw-pr-form)
- [ ] Nervous System Test: modulo Brevo (sibforms)
- [ ] Newsletter MailerLite in quasi tutte le pagine: tenerla o passare a Brevo
- [ ] Anti spam su tutti i moduli

## Legale (da far controllare a un professionista)
- [ ] Traduzioni italiane di Privacy, Cookie, Termini e modulo di iscrizione: da rileggere
- [ ] Banner cookie con consenso prima di caricare YouTube, Vimeo, Calendly, MailerLite (Complianz è sparito con WordPress)
- [ ] Privacy Policy: togliere Complianz e Google Analytics se non più usati, aggiungere i servizi reali (Formspree, Brevo, MailerLite, Calendly, GreenGeeks)
- [ ] Cookie Policy: allinearla al nuovo banner
- [ ] Portogallo: link al Livro de Reclamações Eletrónico, informazioni sulla risoluzione alternativa delle controversie, dati aziendali (nome, NIF, indirizzo) nel footer o nei Termini
- [ ] Registration Form della cerimonia: contiene dati sanitari, serve consenso esplicito e conservazione sicura

## Il giorno del passaggio
- [ ] Email del dominio: non toccare i record MX quando si sposta il DNS
- [ ] SSL attivo su GreenGeeks prima di cambiare il DNS
- [ ] Caricare `dist/` in public_html, provare https://, www, 404 e qualche vecchio indirizzo
- [ ] Google Search Console: verificare il dominio, inviare sitemap.xml, controllare la copertura nelle settimane dopo
- [ ] Statistiche: scegliere cosa usare al posto di Google Analytics (con il banner cookie)
- [ ] Tenere WordPress acceso finché le immagini non sono tutte nel repo
