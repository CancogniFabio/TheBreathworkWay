// Misura cosa cambierebbe nello stile dei titoli a cui seo.py ha cambiato il tag (h2 -> h1 ecc.)
// e scrive in tools/seo-css.json il CSS che riporta tutto com'era, per ogni larghezza di schermo.
// Uso: node tools/seo_css.js            (calcola e scrive)
//      node tools/seo_css.js --check    (verifica: nessuna differenza rimasta)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const CHECK = process.argv.includes('--check');
// larghezze ai due lati di ogni punto di rottura usato dal tema e da Elementor
const W = [320, 360, 399, 400, 425, 426, 544, 545, 600, 767, 768, 769, 800, 900, 901, 921, 922, 1024, 1025, 1200, 1366, 1536, 1920];
const SKIP = /^(height|block-size|width|inline-size|perspective-origin|transform-origin|min-block-size|min-inline-size)$/;

function pagesWithFixes() {
  const out = [];
  const add = (slug, f) => { if (fs.readFileSync(f, 'utf8').includes('tbw-hfix-')) out.push([slug, f]); };
  add('home', path.join(ROOT, 'index.html'));
  for (const d of fs.readdirSync(ROOT)) { const f = path.join(ROOT, d, 'index.html'); if (fs.existsSync(f)) add(d, f); }
  return out;
}

(async () => {
  const b = await chromium.launch();
  const result = {}; let problems = 0;
  for (const [slug, file] of pagesWithFixes()) {
    const per = {}; // cls -> prop -> {w: value}
    for (const w of W) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      await p.route('**/*', r => r.request().url().startsWith('file:') ? r.continue() : r.abort());
      await p.goto('file://' + file, { waitUntil: 'domcontentloaded' });
      const d = await p.evaluate(([CHECK, skip]) => {
        const SK = new RegExp(skip);
        if (!CHECK) { const s = document.getElementById('tbw-seo-css'); if (s) s.remove(); }
        const snap = root => [root, ...root.querySelectorAll('*')].map(e => { const c = getComputedStyle(e); const o = {}; for (const k of c) o[k] = c.getPropertyValue(k); return o; });
        const res = {};
        for (const el of [...document.querySelectorAll('[data-tbw-orig]')]) {
          const cls = [...el.classList].find(c => c.startsWith('tbw-hfix-'));
          const now = snap(el);
          const o = document.createElement(el.dataset.tbwOrig);
          for (const a of el.attributes) o.setAttribute(a.name, a.value);
          while (el.firstChild) o.appendChild(el.firstChild);
          el.replaceWith(o);
          const before = snap(o);
          const diff = {};
          before.forEach((x, i) => { for (const k in x) if (!SK.test(k) && x[k] !== now[i][k]) diff[i + '|' + k] = x[k]; });
          res[cls] = { tag: o.tagName.toLowerCase() === el.tagName.toLowerCase() ? '' : el.tagName.toLowerCase(), diff };
        }
        return res;
      }, [CHECK, SKIP.source]);
      for (const cls in d) {
        per[cls] = per[cls] || { tag: d[cls].tag, props: {} };
        for (const k in d[cls].diff) { (per[cls].props[k] = per[cls].props[k] || {})[w] = d[cls].diff[k]; }
      }
      await p.close();
    }
    if (CHECK) {
      for (const cls in per) for (const k in per[cls].props) { problems++; console.log('DIFF', slug, cls, k, JSON.stringify(per[cls].props[k])); }
      continue;
    }
    // costruisce il CSS: per ogni proprietà, gruppi di larghezze con lo stesso valore
    let css = '';
    for (const cls in per) {
      for (const key in per[cls].props) {
        const [idx, prop] = key.split('|');
        if (idx !== '0') { console.log('NOTA discendente', slug, cls, key); continue; }
        const vals = per[cls].props[key];
        let groups = [];
        for (const w of W) {
          const v = vals[w];
          const g = groups[groups.length - 1];
          if (g && g.v === v) g.hi = w; else groups.push({ v, lo: w, hi: w });
        }
        groups.forEach((g, i) => {
          if (g.v === undefined) return;
          const q = [];
          if (i > 0) q.push('(min-width: ' + (groups[i - 1].hi + 1) + 'px)');
          if (i < groups.length - 1) q.push('(max-width: ' + g.hi + 'px)');
          const sel = '.' + cls + '.' + cls;
          const rule = sel + '{' + prop + ':' + g.v + ' !important}';
          css += q.length ? '@media ' + q.join(' and ') + '{' + rule + '}' : rule;
        });
      }
    }
    result[slug] = css;
    console.log(slug, Object.keys(per).length, 'titoli,', css.length, 'caratteri di CSS');
  }
  await b.close();
  if (CHECK) { console.log(problems ? problems + ' differenze' : 'nessuna differenza'); process.exit(problems ? 1 : 0); }
  fs.writeFileSync(path.join(__dirname, 'seo-css.json'), JSON.stringify(result, null, 1));
})();
