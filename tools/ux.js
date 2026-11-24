/* The Breathwork Way: comportamenti comuni (iniettato da tools/seo.py in fondo a ogni pagina) */
(function () {
  var IT = (document.documentElement.lang || '').slice(0, 2) === 'it';
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- sezioni a step che si fermano allo scroll ----------
     [data-tbw-pin=".step"]: la sezione resta ferma, ogni scroll accende lo step successivo,
     dopo l'ultimo la pagina riprende a scorrere. */
  function headerH() {
    var h = document.querySelector('#ast-mobile-header');
    if (!h || !h.offsetHeight) h = document.querySelector('#masthead .main-header-bar') || document.querySelector('#masthead');
    var r = h ? h.getBoundingClientRect() : null;
    return r && getComputedStyle(h).position !== 'static' && r.bottom > 0 ? Math.min(r.bottom, 120) : 0;
  }
  function unclip(el) {
    for (var p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      var o = getComputedStyle(p);
      if (/(hidden|auto|scroll)/.test(o.overflowY) || /(hidden|auto|scroll)/.test(o.overflowX)) p.style.overflow = 'clip';
    }
  }
  [].forEach.call(document.querySelectorAll('[data-tbw-pin]'), function (sec) {
    if (still) return;
    var steps = [].slice.call(sec.querySelectorAll(sec.getAttribute('data-tbw-pin')));
    var mode = sec.getAttribute('data-tbw-pin-mode') || '';
    var n = steps.length;
    if (n < 2) return;
    unclip(sec);
    var wrap = document.createElement('div');
    wrap.className = 'tbw-pin-wrap';
    sec.parentNode.insertBefore(wrap, sec);
    wrap.appendChild(sec);
    sec.classList.add('tbw-pin');
    var cur = -2, ticking = false;
    function layout() {
      var vh = window.innerHeight, top = headerH();
      sec.style.minHeight = (vh - top) + 'px';
      var h = sec.offsetHeight;
      var stick = h <= vh - top ? top : vh - h;  // sezione più alta dello schermo: si ferma quando il fondo arriva in basso
      sec.style.top = stick + 'px';
      var stepLen = Math.round(vh * 0.45);
      wrap.style.height = (h + stepLen * n) + 'px';
      wrap._stick = stick; wrap._len = stepLen * n;
    }
    function set(i, p) {
      if (mode === 'line') {
        var list = sec.querySelector('.tbw-steps');
        if (list) {
          var first = steps[0].offsetTop, last = steps[n - 1].offsetTop;
          list.style.setProperty('--lh', Math.max(1, last - first) + 'px');
          list.style.setProperty('--p', Math.min(1, Math.max(0, i / (n - 1))).toFixed(3));
        }
      }
      if (i === cur) return;
      cur = i;
      steps.forEach(function (s, k) {
        s.classList.toggle('on', k <= i);
        s.classList.toggle('now', k === i);
        s.classList.toggle('tbw-a', k <= i);
      });
      if (mode === 'hover') {
        var t = steps[Math.max(0, i)];
        if (i >= 0) t.dispatchEvent(new Event('mouseenter'));
      }
    }
    function update() {
      ticking = false;
      var r = wrap.getBoundingClientRect();
      var scrolled = wrap._stick - r.top;
      var p = Math.max(0, Math.min(1, scrolled / wrap._len));
      var i = r.top > wrap._stick + window.innerHeight * 0.25 ? 0 : Math.min(n - 1, Math.floor(p * n));
      set(i, p);
      sec.classList.toggle('tbw-pin-live', scrolled > 0 && p < 1);
      if (mode === 'hover' && (p >= 1 || r.bottom < 0)) steps[n - 1].dispatchEvent(new Event('mouseleave'));
    }
    function req() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    layout(); update();
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', function () { layout(); req(); });
    window.addEventListener('load', function () { layout(); req(); });
  });

  /* ---------- Offerings: su telefono la descrizione si apre sotto la scheda toccata ---------- */
  var bwo = document.getElementById('bwo-options');
  if (bwo) {
    var mq = window.matchMedia('(max-width: 767px)');
    var tabsBox = bwo.querySelector('.bwo-tabs');
    var tabs = [].slice.call(bwo.querySelectorAll('.bwo-tab'));
    var panels = [].slice.call(bwo.querySelectorAll('.bwo-panel'));
    function place() {
      if (mq.matches) {
        tabs.forEach(function (t, i) { t.after(panels[i]); });
        bwo.classList.add('tbw-acc');
      } else {
        panels.forEach(function (p) { bwo.appendChild(p); });
        bwo.classList.remove('tbw-acc');
        if (!tabs.some(function (t) { return t.classList.contains('is-on'); })) tabs[0].click();
      }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function (e) {
        if (!mq.matches) return;
        if (t.classList.contains('is-on')) {
          e.stopImmediatePropagation();
          t.classList.remove('is-on'); t.setAttribute('aria-selected', 'false');
          panels[i].classList.remove('is-on');
          return;
        }
        setTimeout(function () {
          var y = t.getBoundingClientRect().top + window.scrollY - headerH() - 12;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }, 30);
      }, true);
    });
    place();
    if (mq.addEventListener) mq.addEventListener('change', place);
  }

  /* ---------- finestra "Book this session" ---------- */
  var modal = document.getElementById('apply');
  if (modal) {
    var form = modal.querySelector('form');
    var last = null;
    function open() {
      last = document.activeElement;
      modal.hidden = false;
      document.documentElement.classList.add('tbw-modal-open');
      setTimeout(function () { var f = modal.querySelector('input[name="name"]'); if (f) f.focus(); }, 50);
    }
    function close() {
      modal.hidden = true;
      document.documentElement.classList.remove('tbw-modal-open');
      if (location.hash === '#apply') history.replaceState(null, '', location.pathname + location.search);
      if (last) last.focus();
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href="#apply"]');
      if (a) {
        e.preventDefault();
        var v = a.getAttribute('data-pick'), sel = modal.querySelector('select[name="option"]');
        if (v && sel) sel.value = v;
        open();
      }
    });
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target.closest('.tbw-modal-x')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
    if (location.hash === '#apply') open();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var sel = form.querySelector('select[name="option"]');
      form.querySelector('input[name="_subject"]').value = 'Book this session: ' + sel.options[sel.selectedIndex].text;
      btn.disabled = true;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw 0;
          form.querySelector('.tbw-apply-ok').hidden = false;
          form.querySelector('.tbw-apply-err').hidden = true;
          [].forEach.call(form.querySelectorAll('label, .tbw-modal-send'), function (x) { x.style.display = 'none'; });
        })
        .catch(function () { form.querySelector('.tbw-apply-err').hidden = false; btn.disabled = false; });
    });
  }

  /* ---------- immagini delle cipolle: anteprima subito, il disegno animato la sostituisce quando è pronto ---------- */
  [].forEach.call(document.querySelectorAll('canvas[data-tbw-preview]'), function (cv) {
    var img = new Image();
    img.src = cv.getAttribute('data-tbw-preview');
    img.alt = '';
    img.className = 'tbw-onion-pre';
    img.setAttribute('aria-hidden', 'true');
    var par = cv.parentNode;
    if (getComputedStyle(par).position === 'static') par.style.position = 'relative';
    par.insertBefore(img, cv.nextSibling);
    function fit() {
      img.style.left = cv.offsetLeft + 'px'; img.style.top = cv.offsetTop + 'px';
      img.style.width = cv.offsetWidth + 'px'; img.style.height = cv.offsetHeight + 'px';
    }
    fit(); window.addEventListener('resize', fit); img.onload = fit;
    var ctx;
    try { ctx = cv.getContext('2d'); } catch (e) { return; }
    var t = setInterval(function () {
      try {
        var d = ctx.getImageData(cv.width >> 1, cv.height >> 1, 1, 1).data;
        if (d[3] > 0) { clearInterval(t); img.classList.add('gone'); setTimeout(function () { img.remove(); }, 700); }
      } catch (e) { clearInterval(t); }
    }, 250);
  });
})();
