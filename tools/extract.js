// Estrazione di una pagina di thebreathworkway.com per il mockup statico.
// Uso: eseguire con il javascript_tool di Claude in Chrome sulla pagina live,
// dopo aver impostato window.__TBW_FILE = 'tbw-<slug>.txt'.
// Scarica un unico file .txt: HTML pulito con dentro tutto il CSS utile.
(async () => {
  const FILE = window.__TBW_FILE || 'tbw-page.txt';
  const abs = u => { try { return new URL(u, location.href).href } catch (e) { return u } };

  // 1. scorre tutta la pagina per attivare lazy load e animazioni
  for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)) }
  window.scrollTo(0, 0);

  // 2. CSS: tiene le regole che toccano elementi presenti (anche stati come .on, .active)
  const toks = new Set();
  document.querySelectorAll('*').forEach(e => { if (e.id) toks.add('#' + e.id); e.classList.forEach(c => toks.add('.' + c)) });
  const fams = new Set();
  document.querySelectorAll('*').forEach(e => getComputedStyle(e).fontFamily.split(',').forEach(f => fams.add(f.trim().replace(/["']/g, '').toLowerCase())));
  const kfUsed = new Set();
  const generic = /^\.(elementor|e-con|e-|ast-|wp-|has-|is-|menu|site|page|post|entry|main|container|woocommerce|hfe|cmplz)/;
  function ok(sel) {
    if (sel.split(',').some(s => { s = s.replace(/::?[a-z-]+(\([^)]*\))?/g, '').trim() || '*'; try { return !!document.querySelector(s) } catch (e) { return false } })) return true;
    const t = sel.match(/[.#][A-Za-z0-9_-]+/g) || [];
    return t.some(x => toks.has(x) && !generic.test(x));
  }
  function walk(rules) {
    let out = '';
    for (const r of rules) {
      if (r.type === 1) { if (ok(r.selectorText)) { out += r.cssText + '\n'; (r.style.animationName || r.style.animation || '').split(/[\s,]+/).forEach(x => kfUsed.add(x)) } }
      else if (r.type === 4 || r.type === 12) { const inner = walk(r.cssRules); if (inner) out += (r.type === 4 ? '@media ' : '@supports ') + r.conditionText + '{' + inner + '}\n' }
      else if (r.type === 5) { const f = r.style.getPropertyValue('font-family').replace(/["']/g, '').toLowerCase().trim(); if (fams.has(f)) out += r.cssText + '\n' }
      else if (r.type === 7) { out += '@@KF@@' + r.name + '@@' + r.cssText.replace(/\n/g, ' ') + '\n' }
      else if (r.type !== 3) { out += r.cssText + '\n' }
    }
    return out;
  }
  let css = '';
  for (const s of document.styleSheets) { try { css += walk(s.cssRules) } catch (e) { } }
  css = css.split('\n').map(l => { return l.replace(/@@KF@@([^@]+)@@(.*)$/, (x, n, k) => kfUsed.has(n) ? k : '') }).join('\n');
  css = css.replace(/url\((['"]?)([^'")]+)\1\)/g, (m, q, u) => u.startsWith('data:') ? m : 'url("' + abs(u) + '")');
  css += '\n.elementor-invisible{visibility:visible!important}\n';

  // 3. HTML pulito
  const doc = document.documentElement.cloneNode(true);
  doc.querySelectorAll('link[rel="stylesheet"],style,link[rel="preload"],link[rel="prefetch"],link[rel="dns-prefetch"],link[rel="preconnect"],link[rel="modulepreload"],noscript').forEach(e => e.remove());
  doc.querySelectorAll('script[src]').forEach(e => e.remove());
  doc.querySelectorAll('script:not([src])').forEach(s => { const t = s.textContent; if (s.hasAttribute('data-optimized') || s.hasAttribute('data-cfasync') || /litespeed|wp\.i18n|elementorFrontend|Config\s*=|cmplz|complianz|gtag|dataLayer|wp-emoji|mailerlite|WCPAY|_wca|_stq|trident|woocommerce-no-js/i.test(t) || s.type === 'application/ld+json' || s.type === 'speculationrules') s.remove() });
  // attenzione: non toccare <body>, che ha classi cmplz
  doc.querySelectorAll('body *').forEach(e => { if (e.id && e.id.startsWith('cmplz')) e.remove(); else if (typeof e.className === 'string' && /(^|\s)cmplz-(cookiebanner|manage-consent|soft-cookiewall)/.test(e.className)) e.remove() });
  doc.querySelectorAll('.elementor-invisible').forEach(e => e.classList.remove('elementor-invisible'));
  doc.querySelectorAll('[data-settings]').forEach(e => { try { const s = JSON.parse(e.getAttribute('data-settings')); delete s.animation; delete s._animation; e.setAttribute('data-settings', JSON.stringify(s)) } catch (x) { } });
  doc.querySelectorAll('img').forEach(i => {
    const real = i.getAttribute('data-src') || i.getAttribute('data-lazy-src'); if (real) i.setAttribute('src', real);
    const ss = i.getAttribute('data-srcset') || i.getAttribute('srcset'); i.removeAttribute('data-src'); i.removeAttribute('data-srcset');
    if (ss) i.setAttribute('srcset', ss.split(',').map(p => { p = p.trim().split(' '); p[0] = abs(p[0]); return p.join(' ') }).join(', '));
    i.setAttribute('src', abs(i.getAttribute('src') || '')); i.classList.remove('litespeed-loading'); i.removeAttribute('loading');
  });
  doc.querySelectorAll('[style*="url("]').forEach(e => e.setAttribute('style', e.getAttribute('style').replace(/url\((['"]?)([^'")]+)\1\)/g, (m, q, u) => 'url("' + abs(u) + '")')));
  const head = doc.querySelector('head');
  const meta = document.createElement('meta'); meta.name = 'robots'; meta.content = 'noindex, nofollow'; head.prepend(meta);
  const st = document.createElement('style'); st.id = 'tbw-used-css'; st.textContent = css; head.appendChild(st);
  const out = '<!DOCTYPE html>\n' + doc.outerHTML;

  // 4. download come .txt (Chrome blocca i download .html generati dalla pagina)
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([out], { type: 'text/plain' })); a.download = FILE;
  document.body.appendChild(a); a.click(); a.remove();
  window.__TBW_RESULT = { bytes: out.length, body: !!doc.querySelector('body') };
})();
