#!/bin/sh
# Rigenera tutte le pagine dopo una modifica a quality.css, ux.js, testi o traduzioni
set -e
cd "$(dirname "$0")/.."
python3 tools/seo.py
python3 tools/footer.py
python3 tools/fixes.py
python3 tools/make_404.py
python3 tools/layout.py
python3 tools/i18n.py extract
python3 tools/i18n.py build
