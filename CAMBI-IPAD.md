# Cambi richiesti da Fabio (24 nov 2026, visti da iPad verticale)

Fatti il 24 nov 2026. Dove stanno: tools/responsive.css (impaginazione), tools/ux.js (scroll a step, schede Offerings su telefono, finestra Book this session, anteprima cipolle), tools/layout.py (ritocchi HTML), testi in tools/fixes/text-en.json e tools/i18n/it.json. Dopo ogni modifica: ./tools/rebuild.sh

Regola generale: su iPad verticale (e dove serve anche sul telefono) i testi sono troppo incolonnati e i margini laterali troppo grandi. Allargare le colonne. Nelle sezioni foto + testo a due colonne la foto diventa minuscola: ingrandirla o cambiare struttura (foto grande sopra, testo largo sotto). Mai parole spezzate a metà (Breathwork, companies): piuttosto testo leggermente più piccolo.
Sezioni a step (1, 2, 3): lo scroll si deve fermare sulla sezione, ogni scroll passa allo step successivo e solo dopo l'ultimo la pagina continua.

## Home
- [x] Foto in bianco e nero accanto a "What is your body saying": più grande, meno spazio tra le due colonne
- [x] "Take the Nervous System Assessment / and see exactly where you are": sistemare l'andata a capo (iPad e telefono)
- [x] Framework: il numero 03 di Release è grigio, deve essere bianco come gli altri
- [x] Framework: blocco dello scroll sui 3 step
- [x] Versione italiana: tradurre i 3 step (Regulate, Reveal, Release)
- [x] "Who is this for": foto più grande o alternativa che renda bene
- [x] Testimonial "What clients say": più largo, l'immagine si ripete con un taglio
- [x] Footer: "The Breathwork Way", la K va a capo; Breathwork resta una parola intera (ridurre un po' il testo). Vale per tutto il sito

## Foto mancanti (anche da computer)
- [x] Framework senza foto
- [x] Offerings senza foto
- [x] Retreats senza foto
- [x] About Me: la foto c'è ma è piccola, ingrandire

## Contact
- [x] Tutto a sinistra: centrare e risistemare l'impaginazione
- [x] Email, Location, Instagram scritti con un font che non è il nostro: usare i font del sito

## Framework
- [x] Immagine della cipolla arriva troppo tardi: deve esserci subito all'apertura della pagina
- [x] Versione italiana: 3 step in italiano
- [x] "Different approaches to breathwork": griglia 2x2 (Activating, Calming, Trauma informed, Integrative) e un po' più larga; su iPad ora sono colonne strette
- [x] "A Beautiful Journey of Awareness and Release": margini laterali troppo grandi
- [x] "Safety first": troppo stretto e lungo
- [x] "Start with one layer": togliere l'ombra sotto

## Offerings
- [x] Telefono: le 4 tab (Calm my system, Fix how I breathe, ...) aprono la descrizione sotto tutte le tab e non si vede. Su telefono: tab chiuse di base (o solo la prima aperta), la descrizione si apre subito sotto la tab cliccata. iPad va bene così
- [x] Manca il link "Book this session": deciso, apre un modulo di richiesta (nome, email, messaggio). Il collegamento dell'invio resta da fare come gli altri moduli
- [x] Sezione dei 3 step: blocco dello scroll
- [x] "Hey I'm Fabio": foto più grande, testo meno incolonnato
- [x] "What clients say": l'immagine si ripete 2 volte su iPad
- [x] "Retreats and collaborations": troppo lungo su iPad, si può cambiare impaginazione
- [x] Live practices, Downloadable e Breathwork Fundamentals Course: uno accanto all'altro

## Corporate Breathwork
- [x] Parole spezzate (Breathwork, companies): allargare
- [x] "Who is this for" e "Teams / Leadership groups": su iPad verticale (e telefono) i blocchi Teams e Leadership vanno sotto al titolo
- [x] Numeri (77%, ecc.): su una riga anche su iPad verticale, o centrati / con animazione leggibile
- [x] "What changes": allargare For your team e For leaders
- [x] "How it works": blocco dello scroll su step 1, 2, 3
- [x] "Choose your format": foto più grande, colonne più larghe
- [x] "What happens during a breathwork session": stessa cosa
- [x] FAQ "What I get asked the most": in verticale (iPad e telefono) titolo sopra e domande sotto, una colonna sola

## Retreats & Events
- [x] Foto sotto "Save the date" (Fabio a bordo piscina): effetto sfondo fisso che scorre (parallax) come la foto Himalaya di Ritiri Itineranti / Inner Travels
- [x] "Desert Way": ristrutturare, ritiro immersivo, niente due colonne
- [x] Non più Inner Travels ma Ritiri Itineranti: bottone "Esplora di più" che porta al sito italiano di Ritiri Itineranti
- [ ] Locandina da Ritiri Itineranti: per ora foto del sito Ritiri Itineranti (assets/media/ritiri/desert-way.jpg), Fabio manda la locandina

## Retreats & Events (seguito)
- [x] "Chi sono" (About, dopo i ritiri): due colonne troppo strette
- [x] "Pronto a lavorare col tuo respiro" (Ready to work with your breath): togliere l'ombra dietro il testo

## Insights
- [x] Nome: è un blog, "Approfondimenti" non va. Cambiare nome (proposta: Blog / Journal)
- [x] Colonne più larghe, testo impaginato meglio

## Lingua EN/IT
- [x] Telefono: il pulsante lingua deve stare fuori dal menu, sempre visibile
- [x] Computer: pulsante con un riquadro, che risalti un po' (senza esagerare)

## Da decidere / in attesa
- Book this session invia allo stesso Formspree delle richieste ritiri (xkjgawre), con oggetto "Book this session: ...". Se serve, creare un modulo Formspree a parte
- Bug sistemato: footer.py copiava nelle altre pagine lo sfondo dell'hero della Home (per questo Framework, Offerings e Retreats non avevano la foto)
- Locandina Desert Way
