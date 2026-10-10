# Chlorophyll 10/10 — BoPep4 and ACC deaminase under salt stress

Bilingual (中文 / English) analysis page for the two chlorophyll data sets collected on 2026-10-10 by the ReLeaf iGEM team.

- Live: https://timmy97-tw.github.io/chlorophyll-1010/
- `src/index.src.html` — page source; `{{中文||English}}` marks bilingual strings
- `build.py` — expands the bilingual strings and inlines `data/numbers.json` into `index.html`
- `analysis/chlorophyll_1010.py <workbook.xlsx> data/numbers.json` — recomputes every value from the raw absorbances (Arnon, V = 4 mL, blank 0.037)
