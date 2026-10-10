#!/usr/bin/env python3
"""Build index.html from src/index.src.html.

{{中文||English}} expands into a pair of spans for the language toggle;
data/numbers.json (written by analysis/chlorophyll_1010.py) is inlined.
"""
import json, pathlib, re

root = pathlib.Path(__file__).parent
src = (root / "src" / "index.src.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "numbers.json").read_text(encoding="utf-8"))
html = re.sub(r"\{\{(.*?)\|\|(.*?)\}\}",
              lambda m: f'<span class="zh">{m.group(1)}</span><span class="en">{m.group(2)}</span>',
              src, flags=re.S)
html = html.replace("/*DATA*/null", json.dumps(data, separators=(",", ":")))
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html) // 1024, "KB,", html.count('class="zh"'), "bilingual strings")
