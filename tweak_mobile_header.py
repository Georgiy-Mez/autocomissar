#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Доработка мобильной шапки komissar125:
 - короткое название «Скорая страховая помощь»
 - крупнее иконка машины
 - кнопка вызова красная/тревожная с пульсацией
Бампает версию стилей v5->v6. Идемпотентно. Запуск из корня репо."""
from pathlib import Path

root = Path(__file__).resolve().parent
html_files = [p for p in root.rglob("*.html") if "dist" not in p.parts]

CSS = '''

/* === Моб. шапка v2: короткое имя, крупная иконка, тревожная кнопка === */
@media (max-width: 768px) {
  .logo-name-mobile { font-size: 0.92rem !important; font-weight: 800 !important; line-height: 1.1 !important; }
  .logo-icon img { width: 58px !important; height: 58px !important; }
  .header-call { background: #e11d2a !important; box-shadow: 0 6px 18px rgba(225,29,42,.45); animation: hc-alarm 1.3s infinite; }
  .header-call:hover, .header-call:active { background: #c2161f !important; }
  .header-call .hc-num { font-size: 13.5px; }
}
@keyframes hc-alarm {
  0%   { transform: scale(1);    box-shadow: 0 6px 18px rgba(225,29,42,.45), 0 0 0 0 rgba(225,29,42,.55); }
  60%  { transform: scale(1.045);box-shadow: 0 6px 18px rgba(225,29,42,.45), 0 0 0 13px rgba(225,29,42,0); }
  100% { transform: scale(1);    box-shadow: 0 6px 18px rgba(225,29,42,.45), 0 0 0 0 rgba(225,29,42,0); }
}
'''

# 1) CSS один раз
css = root / "static" / "css" / "main.css"
c = css.read_text(encoding="utf-8")
if "Моб. шапка v2" not in c:
    css.write_text(c + CSS, encoding="utf-8")
    print("main.css: доработка добавлена")
else:
    print("main.css: уже доработано")

# 2) короткое имя в моб. логотипе + бамп версии
OLD = '<span class="logo-name-mobile">Служба аварийных комиссаров «Скорая страховая помощь»</span>'
NEW = '<span class="logo-name-mobile">«Скорая страховая помощь»</span>'
for f in html_files:
    s = f.read_text(encoding="utf-8")
    ch = False
    if OLD in s:
        s = s.replace(OLD, NEW); ch = True
    if "main.css?v=5" in s:
        s = s.replace("main.css?v=5", "main.css?v=6"); ch = True
    if ch:
        f.write_text(s, encoding="utf-8")
        print("  +", f.relative_to(root))
print("Готово.")
